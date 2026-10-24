-- Run in the Supabase SQL editor.

create extension if not exists vector with schema extensions;

create type person_category as enum (
  'member_regular',
  'member_vip',
  'guest',
  'staff',
  'contractor'
);

create table persons (
  person_id uuid primary key references auth.users (id) on delete cascade,
  first_name text not null,
  last_name text not null,
  category person_category not null,
  destination text
);

-- Written only by the backend (service role) with the rows returned by
-- face_lite FaceEngine.enroll: three rows per person, 128-dim L2-normalized embeddings.
create table face_templates (
  template_id uuid primary key,
  person_id uuid not null references persons (person_id) on delete cascade,
  embedding extensions.vector(128) not null,
  model_version text not null
);

-- Accounts allowed to register users (see the create-user Edge Function).
create table admins (
  user_id uuid primary key references auth.users (id) on delete cascade
);

alter table persons enable row level security;
alter table face_templates enable row level security;
alter table admins enable row level security;

create policy "read own admin row" on admins
  for select using (auth.uid() = user_id);

-- Any signed-in account can read every persons / face_templates row (the robot included).
-- Writes happen only through the backend and the Edge Function (service role).
create policy "authenticated read all persons" on persons
  for select to authenticated using (true);

create policy "authenticated read all face templates" on face_templates
  for select to authenticated using (true);

-- Private bucket for the photos (<person_id>/front.jpg, left.jpg, right.jpg).
-- Each user only touches the folder named after their id; the backend reads them with the service role.
insert into storage.buckets (id, name, public) values ('faces', 'faces', false);

create policy "read own face photos" on storage.objects
  for select using (bucket_id = 'faces' and (storage.foldername(name))[1] = auth.uid()::text);

create policy "upload own face photos" on storage.objects
  for insert with check (bucket_id = 'faces' and (storage.foldername(name))[1] = auth.uid()::text);

create policy "replace own face photos" on storage.objects
  for update using (bucket_id = 'faces' and (storage.foldername(name))[1] = auth.uid()::text);

insert into persons (person_id, first_name, last_name, category, destination)
values ('42b3e9c3-8e23-4197-bf4e-428303086ce9', 'Ana', 'Pérez', 'member_vip', 'Salón VIP');