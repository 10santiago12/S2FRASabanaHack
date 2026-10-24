// Edge Function: lets an admin register a user (auth account + persons row).
// Runs server-side, so the service role key never reaches the browser.
import { createClient } from 'npm:@supabase/supabase-js@2';

const EMAIL_DOMAIN = 'nclub.local'; // must match EMAIL_DOMAIN in index.html
const CATEGORIES = ['member_regular', 'member_vip', 'guest', 'staff', 'contractor'];

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
};

const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { ...corsHeaders, 'Content-Type': 'application/json' },
  });

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: corsHeaders });
  if (req.method !== 'POST') return json({ error: 'Método no permitido.' }, 405);

  const admin = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!,
  );

  // 1. Who is calling? Verify the JWT in code.
  const token = req.headers.get('Authorization')?.replace('Bearer ', '');
  if (!token) return json({ error: 'No autorizado.' }, 401);
  const { data: caller, error: callerError } = await admin.auth.getUser(token);
  if (callerError || !caller.user) return json({ error: 'No autorizado.' }, 401);

  // 2. Is the caller an admin?
  const { data: adminRow } = await admin
    .from('admins')
    .select('user_id')
    .eq('user_id', caller.user.id)
    .maybeSingle();
  if (!adminRow) return json({ error: 'Esta cuenta no es de administrador.' }, 403);

  // 3. Validate the input.
  const input = await req.json().catch(() => null);
  const firstName = String(input?.first_name ?? '').trim();
  const lastName = String(input?.last_name ?? '').trim();
  const document = String(input?.document ?? '').trim();
  const password = String(input?.password ?? '');
  const category = String(input?.category ?? '');
  const destination = String(input?.destination ?? '').trim() || null;

  if (!firstName || !lastName) return json({ error: 'Nombre y apellido son obligatorios.' }, 400);
  if (!/^[A-Za-z0-9]+$/.test(document)) {
    return json({ error: 'El documento solo puede tener letras y números.' }, 400);
  }
  if (password.length < 6) return json({ error: 'La contraseña debe tener al menos 6 caracteres.' }, 400);
  if (!CATEGORIES.includes(category)) return json({ error: 'Rol no válido.' }, 400);

  // 4. Create the auth user, then its persons row; undo the user if the row fails.
  const { data: created, error: createError } = await admin.auth.admin.createUser({
    email: `${document}@${EMAIL_DOMAIN}`,
    password,
    email_confirm: true,
  });
  if (createError || !created.user) {
    return json({ error: createError?.message ?? 'No se pudo crear el usuario.' }, 400);
  }

  const { error: personError } = await admin.from('persons').insert({
    person_id: created.user.id,
    first_name: firstName,
    last_name: lastName,
    category,
    destination,
  });
  if (personError) {
    await admin.auth.admin.deleteUser(created.user.id);
    return json({ error: 'No se pudo guardar el perfil.' }, 500);
  }

  return json({ person_id: created.user.id }, 201);
});
