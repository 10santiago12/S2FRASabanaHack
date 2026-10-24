# Ficha Técnica del Proyecto — PIBOT

## Nombre del proyecto

PIBOT: recepción robótica para N Club (robot AgiBot X2 Ultra).

## Descripción breve

N Club es un club privado de membresía cuya entrada depende hoy del personal de recepción. Su reconocimiento facial solo distingue entre miembros y no miembros, pero a la puerta llegan cinco tipos de visitante: miembro VIP, miembro regular, invitado, personal del club y trabajador externo. Cada uno necesita una orientación distinta.

PIBOT no vende un robot ni una aplicación: es el framework que permite a cualquier lugar diseñar cómo su robot recibe a las personas, y que el robot lo ejecute por su cuenta. La solución sigue cuatro movimientos:

1. **Ver:** la cámara del robot entrega una señal, un rostro.
2. **Confirmar:** PIBOT añade una segunda señal (lista, carné, código o nombre). Nunca el rostro solo.
3. **Vivirlo:** el flujo decide qué dice el robot, qué muestra, qué reserva y hacia dónde camina.
4. **Hacerlo propio:** el club construye y cambia el flujo sin programar.

El patrón es el mismo para los cinco visitantes: reconocer, confirmar, interactuar y guiar. Si la verificación falla, el robot lo explica y llama a recepción: nunca asume una categoría.

## ¿Qué es PIBOT? — Plataforma de flujos y presencia del robot

PIBOT es un editor visual de flujos, similar a n8n, que convierte la recepción de un club en un flujo sin código que el robot ejecuta solo. La lógica del lugar vive en el flujo y en los datos del club (sus lugares, listas y eventos), no en el código. Tiene tres vistas: Diseñar, En vivo y Visitas.

Un club lo construye con tres preguntas: quién llega (las categorías salen de sus propias listas), qué hace el robot con cada uno (con una vista previa de cómo sonará el saludo) y una revisión en lenguaje sencillo que avisa si algún camino dejaría al robot callado o perdido. Cada salida del flujo tiene un "+" para elegir qué hace el robot después, sin arrastrar flechas.

El robot AgiBot X2 Ultra es la "cara" del producto: saluda, habla, se desplaza y acompaña al visitante. La pestaña Visitas registra cada llegada (categoría, cómo se confirmó, resultado y duración) para que el club vea qué resolvió el robot y qué pasó a una persona.

## Los cinco flujos

| Visitante | Cómo se confirma | Qué hace el robot |
| --- | --- | --- |
| Miembro VIP | El rostro coincide con la lista de membresías. | Lo saluda por su nombre, conoce sus hábitos, gestiona sus reservas y lo lleva a su destino. |
| Miembro regular | Mismo reconocimiento. | Ofrece otro menú de lugares, más corto que el del VIP. |
| Invitado | La cámara indica "no miembro", así que el robot pregunta el motivo y comprueba la lista de invitados y el código del evento: nombre y código deben coincidir. | Lo orienta hacia su evento o las zonas permitidas. |
| Personal del club | Carné, agenda y turno. | Le da el resumen del día. |
| Trabajador externo | Nombre, área de trabajo y código del trabajo, los tres. | Lo dirige a su área, por la entrada de servicio. |

Si la información no alcanza o se contradice (por ejemplo, un código de un evento ya terminado), el robot no elige un lado: explica el motivo y llama a una persona.

## Nivel de desarrollo

Estado: prototipo funcional, repartido en cuatro repositorios que se conectan entre sí.

Implementado hasta el momento:

- Editor PIBOT con asistente de tres preguntas, motor de flujos, listas, códigos de eventos, reservas, agenda y registro de visitas, con cinco flujos de ejemplo.
- Aplicación web móvil con inicio de sesión por documento y contraseña, y una sección de administrador para registrar usuarios (nombre, apellido, documento, contraseña, rol y lugar).
- Captura guiada de tres fotos (frente, izquierda y derecha), con detección de rostro en el navegador: la foto se toma sola cuando la pose se mantiene.
- Servidor de validación en Python que revisa cada foto y las tres en conjunto antes de guardar. Si algo falla, no se guarda nada y se pide repetir solo las poses rechazadas.
- Base de datos en Supabase con las tablas `persons` y `face_templates` (tres embeddings de 128 valores por persona), almacenamiento privado de fotos y políticas de seguridad.
- Motor de reconocimiento facial propio (YuNet y SFace), con registro de tres plantillas, comparación y calibración.
- Capa del robot: servicio de reconocimiento que lee Supabase, robot X2 en MuJoCo con el controlador de movimiento oficial, voz y modelo de lenguaje local.
- Prueba en el X2 real, el 24 de octubre de 2026: reconoció a 3 personas con la cámara de la cabeza, habló con su propia voz, saludó con la mano, entendió una respuesta hablada (Whisper, en el robot) y se controló en vivo desde PIBOT.

Aún no funciona en el robot real:

- Guiar a un visitante caminando. El primer intento fue en dirección equivocada porque el sensor está montado de lado; la fórmula ya se corrigió, los frenos de seguridad respondieron y falta afinar el giro. En simulación sí funciona.
- La transcripción de voz es lenta en la CPU del robot, y el micrófono captura pocas frases.

## Video de presentación

🔗 Enlace al video/demo: https://youtu.be/WKdRD9Tq7c4

## Modelo de negocio (hipótesis por validar)

No vendemos un robot ni una aplicación: vendemos el ajuste. Todo lugar con una puerta atendida tiene el mismo trabajo y se diferencia en todo lo demás: lugares, reglas, categorías, tono e incluso el robot.

| Flujo de ingresos | Qué incluye |
| --- | --- |
| Puesta en marcha (pago único) | Configurar el flujo del club, mapear sus lugares, conectar sus listas y ajustar la voz. |
| Plataforma (suscripción mensual por sede) | El editor, el programa que corre en el robot, las actualizaciones, el soporte y el panel de visitas. |
| Complementos | Integraciones con sistemas de membresías o control de acceso, pasos a medida e idiomas adicionales. |

- **El robot es una elección del lugar:** lo compra o lo arrienda con un aliado de hardware. No fabricamos robots, así que el producto no depende de uno en concreto: un modelo nuevo es un adaptador, y los flujos y datos del club no cambian.
- **Dónde está la permanencia:** en los flujos, los datos y las integraciones de cada lugar, y en la biblioteca de pasos, que crece con cada despliegue.
- **Segmentos:** primero clubes privados, porque N Club es exactamente ese caso; después hoteles, clínicas, oficinas, espacios de coworking y edificios residenciales.

| Bloque | Hipótesis | Cómo se prueba |
| --- | --- | --- |
| Cliente | Lugares con una puerta atendida y varios tipos de visitante. | Hablar con 5 a 10 encargados de recepción y preguntar qué es rutina. |
| Valor | Tiempo de recepción liberado para casos que exigen criterio, primera impresión consistente, reglas de acceso aplicadas igual siempre y un registro que muestra si funciona. | Piloto: llegadas atendidas sin persona, escalamientos y tiempo por visita. |
| Ingresos | Puesta en marcha, plataforma y complementos. | Precio según el esfuerzo real en N Club y lo que digan los pilotos. |
| Permanencia | Flujos, datos e integraciones viven en PIBOT. | Contar los flujos e integraciones que construye un piloto. |
| Riesgos | Caminata guiada aún no resuelta en el X2 real, normas sobre datos biométricos, reconocimiento facial sin validar a escala, lugares que prefieran un producto cerrado. | Hitos: caminar en el X2, validar con fotos propias y revisión legal. |

Este modelo es nuevo y no se ha validado con ningún cliente. No se ha vendido nada ni desplegado en una segunda sede.

## Ventajas o fortalezas

1. Pasa de "miembro o no miembro" a la categoría exacta. Combina el reconocimiento facial con una segunda señal, de modo que el robot ofrece una orientación distinta para cada uno de los cinco tipos de visitante.
2. El robot no adivina. Cuando la información falta o se contradice, explica el motivo y una persona decide.
3. Flujos editables sin programar. La lógica del club vive en el flujo y en sus datos, así que el lugar puede cambiar categorías, eventos o reglas por su cuenta.
4. Funciona con el estado real del club. Las reservas de un visitante las ve el siguiente, y el robot ofrece solo lo que está libre.
5. Independiente del robot. Un robot nuevo se conecta con un adaptador, sin tocar flujos ni datos.
6. Registro validado antes de guardar. El mismo motor que usa el robot revisa las fotos al registrarlas, así que las plantillas que llegan a la base de datos ya son utilizables.
7. Medición integrada. La pestaña Visitas muestra qué resolvió el robot y qué pasó a una persona, y se puede exportar.
8. Bajo consumo. El motor facial corre en CPU, con unos 10 ms por foto en un portátil.

## Desventajas o debilidades

1. Precisión sin validar con datos propios. En un conjunto público de cinco personas identificó correctamente el 85 % de los conocidos, sin confundir a dos personas y sin aceptar ninguno de 100 rostros desconocidos. La meta era 95 %, y falta probar con fotos de teléfono y de robot en sesiones distintas. Mientras tanto, si duda, el robot pregunta.
2. Sin detección de presencia real. Una foto impresa podría ser aceptada, y el sistema no sirve como control de acceso.
3. Datos biométricos sensibles. Requieren consentimiento, acceso restringido y eliminación según una política. El robot trabaja solo con las plantillas de 128 números, de las que no se puede reconstruir la foto, pero la aplicación de registro conserva las fotos en un almacenamiento privado. En el prototipo, cualquier cuenta con sesión puede leer todas las plantillas para que el robot las consulte; un sistema real necesita un rol de solo lectura dedicado.
4. Parte del robot es simulada o está pendiente. La voz, los gestos y la pantalla se ven en simulación, y la caminata guiada no funciona todavía en el robot real.
5. Fuente de la categoría por acordar. En el robot real, la categoría podría salir de la lista de membresías del club o de la base de datos, y esa decisión sigue pendiente.
6. Modelo de negocio sin validar y sin segunda sede. Todo lo anterior son hipótesis.
7. Infraestructura de demostración frágil. El acceso desde el celular usa un túnel temporal sin garantía de disponibilidad, y el inicio de sesión no incluye recuperación de contraseña.

## Detalles técnicos

### Lenguajes / frameworks:

- JavaScript, HTML y CSS (PIBOT y aplicación web)
- Python 3.11 (servidor de validación, motor facial y servicios del robot)
- TypeScript sobre Deno (función de servidor en Supabase)
- FastAPI (servidor de validación)
- ROS 2 Humble y MuJoCo (capa del robot)

### Librerías:

- OpenCV con YuNet (detección) y SFace (embeddings de 128 valores)
- NumPy, Pillow, psutil
- supabase-py, uvicorn, python-multipart
- Supabase JS v2 (interfaz web)
- MediaPipe Face Detector (guía de captura en el navegador)
- Whisper y Piper (voz), Qwen2.5 3B (modelo de lenguaje local)
- Bodoni Moda y Hanken Grotesk (tipografías)

### Herramientas y plataformas:

- Supabase: autenticación, Postgres con pgvector, almacenamiento privado y funciones Edge
- Docker y AimDK (AgiBot) para el robot
- Cloudflare Tunnel (acceso desde el celular en la demostración)
- Git/GitHub

## Alcance del prototipo:

- Un flujo diferenciado para cada uno de los cinco tipos de visitante, con confirmación de la categoría por una segunda señal.
- Registro de personas y de tres fotos del rostro, con validación previa y almacenamiento de embeddings.
- Reconocimiento facial real con la cámara de un portátil o la del robot.

| Funciona de verdad | Simulado en la demostración |
| --- | --- |
| PIBOT: editor, asistente, motor de flujos, listas, eventos y códigos, reservas, agenda y registro de visitas. | Las cámaras de los visitantes de prueba (`data/people.json`). |
| Reconocimiento facial (FaceRecognition Lite con Supabase). | Las respuestas de recepción y del supervisor (un clic). |
| El AgiBot X2 en MuJoCo, caminando con el controlador de movimiento oficial. | La voz, la pantalla y los gestos dentro de MuJoCo (aparecen en la página). |
| En el X2 real (24 de octubre de 2026): reconocimiento con la cámara de la cabeza, voz propia, saludo y escucha. | |

Supuestos del club, declarados en la presentación:

- **Membresías:** una lista con el nivel de cada miembro y, para algunos, un hábito.
- **Personal:** una nómina con código de carné, un área y, para algunos, una agenda.
- **Eventos y trabajos:** un lugar, una lista de invitados o trabajadores y un código compartido. Un evento terminado ya no deja entrar a nadie, y un trabajo puede exigir que el área coincida.
- **Reservas:** las canchas y la piscina tienen cupos del día, bloqueos por mantenimiento y reservas. El robot dice que una reserva es de "un miembro VIP", nunca de quién.
- **Lugares y permisos:** el VIP accede a seis lugares y el regular a cuatro. Los invitados, a su evento, la zona social o el restaurante; los trabajadores, a la entrada de servicio; y el personal, a su reunión o al vestier.
- **Inventado para la demostración:** el reloj fijo, los cupos, el resumen del día y los nombres de los visitantes.

## Presupuesto estimado (orientativo):

No incluimos cifras a propósito: no hay una fuente para sustentarlas. Se calcularán con el esfuerzo real de poner en marcha N Club y con lo que indiquen los pilotos.

| Concepto | De qué depende |
| --- | --- |
| Puesta en marcha por lugar | Número de categorías, lugares, listas e integraciones. |
| Plataforma | Alojamiento, soporte y número de sedes y robots. |
| Robot | Compra o arriendo con un aliado de hardware. Queda fuera del producto. |
| Validación con datos propios | Capturas de teléfono y robot en sesiones distintas, y calibración. |
| Tratamiento de datos biométricos | Consentimiento, política de eliminación y revisión legal. |

🔹 Repositorios del proyecto

📁 Registro y validación de rostros (este repositorio): https://github.com/10santiago12/S2FRASabanaHack

📁 Capa del robot y simulación: https://github.com/rafaelsava/nclub-x2-simulation

📁 Editor de flujos PIBOT: https://github.com/santiagoguti17/PIBOT

📁 Motor de reconocimiento facial: https://github.com/FerminEscalona/FaceRecognition_lite

## Contacto / Autores

- Repositorio: https://github.com/10santiago12/S2FRASabanaHack

- Equipo / Autores: [Santiago Gutiérrez](https://github.com/santiagoguti17), [Fermín Escalona](https://github.com/FerminEscalona), [Santiago Urrego](https://github.com/10santiago12), [Rafael Salcedo](https://github.com/rafaelsava) y [Adriana Galbán](https://github.com/ananabananag).
