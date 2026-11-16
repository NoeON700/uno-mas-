# Plantillas NNA Technology

Plantillas reutilizables para crear la solución de un cliente cambiando solo su configuración.

## Plantilla "negocio" (v1)

Un solo archivo (`negocio/index.html`) con módulos que se encienden o apagan:

| Módulo | Qué incluye | Productos del catálogo que cubre |
|---|---|---|
| `pagina` | Portada, servicios con precios, ubicación, horario, botón de WhatsApp | Página profesional |
| `menu` | Menú o catálogo por categorías con precios | Menú digital con QR |
| `registro` | Formulario con campos a la medida, guardado en Supabase, boleto o gafete en PDF con QR individual y folio | Formulario de registro con QR, registro con boleto PDF, formulario de primera consulta, formulario de cotización |

Además, toda página trae su propio **código QR descargable** (enlace "Código QR de esta página" al pie).

## Crear un cliente nuevo

1. Copia un ejemplo de `clientes/` y cambia nombre, textos, colores, servicios y campos.
2. Ejecuta `python3 crear_cliente.py clientes/mi-cliente.json`.
3. En `salida/mi-cliente/` quedan:
   - `index.html`: la página lista (se puede publicar en cualquier hosting).
   - `supabase.sql`: la base de datos del formulario.
   - `PROMPT-LOVABLE.txt`: el mensaje para pegar en un proyecto nuevo de Lovable.
4. Si usa formulario: en el Supabase del cliente abre **SQL Editor**, pega `supabase.sql` y ejecútalo.
   Luego pon en la configuración la **Project URL** y la clave **publishable** (nunca la `secret` ni `service_role`) y repite el paso 2.
5. Los registros se ven en Supabase → **Table Editor → registros** (se pueden descargar en CSV).

Sin `supabase.url` la página queda en **modo demostración**: muestra todo, pero no guarda.

## Qué se puede personalizar

- `tema`: color primario, fondo, texto, tipografías de Google Fonts y redondeo.
- `negocio`: nombre, lema, descripción, logo, imagen de portada, WhatsApp, dirección, horario.
- `registro.campos`: tipos `texto`, `telefono`, `correo`, `numero`, `fecha`, `parrafo`, `opcion` (lista), `opciones` (varias casillas) y `casilla` (aceptación).
  Los campos con id `nombre`, `telefono` y `email` se guardan en columnas propias; los demás, en `datos`.
- `registro.boleto`: título, subtítulo, pie y hasta 4 campos a mostrar.

## Seguridad

- El público solo puede **enviar** registros; no puede leerlos, cambiarlos ni borrarlos (probado con el rol público).
- El QR del boleto contiene un identificador al azar, sin datos personales.
- Para consultorios y datos delicados: usa siempre una base propia del cliente y su aviso de privacidad.

## Pendiente (aún no incluido)

Check-in escaneando el QR, panel del cliente con inicio de sesión, citas, lealtad, encuestas con gráficas y asistentes de IA.
