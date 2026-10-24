# Ficha Técnica del Proyecto — Recepción robótica para N Club

## Nombre del proyecto

Recepción robótica para N Club (plataforma de flujos PIBOT, robot AgiBot X2 Ultra).

## Descripción breve

N Club es un club privado de membresía cuya entrada depende hoy del personal de recepción. Su reconocimiento facial solo distingue entre miembros y no miembros, pero a la puerta llegan cinco tipos de visitante: miembro VIP, miembro regular, invitado, personal del club y trabajador externo. Cada uno necesita una orientación distinta.

Este proyecto es un prototipo que pasa de una identificación parcial a una orientación correcta. Una aplicación web móvil registra a cada persona con su categoría y con tres fotos del rostro (frente, izquierda y derecha), que se validan antes de guardarse. Un robot recibe al visitante, lo reconoce a partir de esos datos, confirma su categoría y lo guía con un flujo diferente para cada una.

## ¿Qué es PIBOT? — Plataforma de flujos y presencia del robot

PIBOT es un editor visual de flujos, similar a n8n, que define cómo el robot recibe y guía a cada visitante: qué pregunta, a quién deja pasar y hacia qué lugar lo dirige. La lógica del lugar vive en archivos de flujo y de datos, no en el código, de modo que un recepcionista puede ajustarla sin programar. Tiene tres vistas: Diseñar, En vivo y Visitas.

El robot AgiBot X2 Ultra es la "cara" del producto: saluda, habla, se desplaza y acompaña al visitante hacia su destino. En esta edición se demuestra en simulación (MuJoCo) y con pruebas preparadas para el robot real.

## Nivel de desarrollo

Estado: prototipo funcional, repartido en cuatro repositorios que se conectan entre sí.

Implementado hasta el momento:

- Aplicación web móvil con inicio de sesión por documento y contraseña, y una sección de administrador para registrar usuarios (nombre, apellido, documento, contraseña, rol y lugar).
- Captura guiada de tres fotos con detección de rostro en el navegador: la foto se toma sola cuando la pose se mantiene, con mensajes de ayuda en cada paso.
- Servidor de validación en Python que revisa cada foto y las tres en conjunto antes de guardar. Si algo falla, no se guarda nada y se pide repetir solo las poses rechazadas.
- Base de datos en Supabase con las tablas `persons` y `face_templates` (tres embeddings de 128 valores por persona), almacenamiento privado de fotos y políticas de seguridad.
- Motor de reconocimiento facial propio (YuNet y SFace), con registro de tres plantillas, comparación y calibración.
- Capa del robot en simulación: servicio de reconocimiento que lee Supabase, robot X2 en MuJoCo, voz y modelo de lenguaje local.
- Editor de flujos PIBOT con cinco flujos de ejemplo, identificación por cámara, código, documento y nombre, y registro de visitas.

## Video de presentación

🔗 Enlace al video/demo: (pendiente — insertar URL aquí)

## Ventajas o fortalezas

1. Pasa de "miembro o no miembro" a la categoría exacta. Combina el reconocimiento facial con los datos registrados de cada persona, de modo que el robot puede ofrecer una orientación distinta para cada uno de los cinco tipos de visitante.
2. Registro validado antes de guardar. El mismo motor que usa el robot revisa las fotos al registrarlas, así que las plantillas que llegan a la base de datos ya son utilizables y no hay que limpiar registros defectuosos.
3. Flujos editables sin programar. PIBOT separa la lógica del club del código, lo que permite adaptar la recepción a otros lugares o a cambios de política.
4. Bajo consumo y sin dependencia de la nube para reconocer. El motor corre en CPU y la comparación se hace sobre una galería local. Solo la sincronización de plantillas necesita red.
5. Privacidad por diseño parcial. El robot trabaja con embeddings, no con las fotos, y los embeddings no permiten reconstruir la imagen original.
6. Experiencia clara para el visitante. Registro móvil guiado, con poses indicadas y retroalimentación inmediata.

## Desventajas o debilidades

1. Precisión sin validar en condiciones reales. El motor acierta entre 85 % y 90 % de los conocidos en el conjunto público AT&T/ORL, frente a una meta de 95 %, y no se ha probado con fotos de teléfono y de robot en sesiones distintas. Los umbrales del robot son ajustes manuales.
2. Sin detección de presencia real. Una foto impresa podría ser aceptada. El sistema no sirve como control de acceso.
3. Datos biométricos sensibles. Fotos y embeddings requieren consentimiento, acceso restringido y eliminación según una política. En el prototipo, cualquier cuenta con sesión puede leer todos los embeddings para que el robot pueda consultarlos; un sistema real necesita un rol de solo lectura dedicado.
4. Parte del robot es simulada. La voz, los gestos y la pantalla se muestran en simulación, y el desplazamiento guiado en el robot real no está resuelto.
5. Fuente de la categoría por acordar. En el robot real, la categoría podría salir de la lista de membresías del club o de la base de datos, y esa decisión sigue pendiente.
6. Infraestructura de demostración frágil. El acceso desde el celular usa un túnel temporal sin garantía de disponibilidad, y el inicio de sesión no incluye recuperación de contraseña.

## Detalles técnicos

### Lenguajes / frameworks:

- Python 3.11 (servidor de validación y motor facial)
- JavaScript, HTML y CSS (aplicación web y PIBOT)
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

- Registro de personas y de tres fotos del rostro, con validación previa y almacenamiento de embeddings.
- Reconocimiento facial real en la capa del robot, con confirmación de la categoría a partir de los datos registrados y, cuando la cámara no resuelve, por código, documento o nombre.
- Cinco flujos de orientación diferenciados en PIBOT, uno por tipo de visitante.
- Simulado: la voz, los gestos y la pantalla del robot, y los visitantes de prueba del editor. Real: el registro, la validación, el reconocimiento facial y el movimiento en la física de MuJoCo.
- Supuestos del club: los lugares y permisos de cada categoría (Recepción, Salón VIP, Zona social, Terraza, Restaurante, Gimnasio, Spa, Acceso de servicio y Vestier de personal) son supuestos del equipo, declarados en la presentación.

## Presupuesto estimado (orientativo):

- Prototipo mínimo viable (desarrollo y pruebas internas, sin el robot físico): USD 3.000 – 8.000.

- Piloto en el club, con captura de datos reales, calibración, rol de lectura dedicado, servidor propio y revisión de privacidad: USD 15.000 – 40.000.

- Nota: rangos orientativos, no calculados en detalle. No incluyen la compra o el alquiler del robot. Requieren una estimación según el alcance final, el alojamiento, las licencias y la política de tratamiento de datos biométricos.

🔹 Repositorios del proyecto

📁 Registro y validación de rostros (este repositorio): https://github.com/10santiago12/S2FRASabanaHack

📁 Capa del robot y simulación: https://github.com/rafaelsava/nclub-x2-simulation

📁 Editor de flujos PIBOT: https://github.com/santiagoguti17/PIBOT

📁 Motor de reconocimiento facial: https://github.com/FerminEscalona/FaceRecognition_lite

## Contacto / Autores

- Repositorio: https://github.com/10santiago12/S2FRASabanaHack

- Equipo / Autores: [Santiago Gutiérrez](https://github.com/santiagoguti17), [Fermín Escalona](https://github.com/FerminEscalona), [Santiago Urrego](https://github.com/10santiago12), [Rafael Salcedo](https://github.com/rafaelsava) y [Adriana Galbán](https://github.com/ananabananag).
