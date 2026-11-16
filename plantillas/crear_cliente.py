#!/usr/bin/env python3
"""Crea la página de un cliente a partir de su archivo de configuración.

Uso:  python3 crear_cliente.py clientes/barberia-lopez.json
Deja en salida/<cliente>/:
  index.html          la página lista para publicar (un solo archivo)
  supabase.sql        la base de datos del formulario (si usa registro)
  PROMPT-LOVABLE.txt  el mensaje para pegar en un proyecto nuevo de Lovable
"""
import json, re, shutil, sys, unicodedata
from pathlib import Path

AQUI = Path(__file__).resolve().parent

def slug(t):
    t = unicodedata.normalize("NFD", t).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-") or "cliente"

def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    cfg_path = Path(sys.argv[1])
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    nombre = cfg.get("negocio", {}).get("nombre")
    if not nombre:
        sys.exit("Falta negocio.nombre en la configuración.")
    sb = cfg.get("supabase", {})
    if "service_role" in json.dumps(sb) or str(sb.get("clave", "")).startswith("sb_secret_"):
        sys.exit("ALTO: en 'supabase.clave' va solo la clave pública (publishable/anon), nunca una secreta.")
    plantilla = (AQUI / "negocio" / "index.html").read_text(encoding="utf-8")
    bloque = "/*CONFIG-INICIO*/\nwindow.CONFIG = " + json.dumps(cfg, ensure_ascii=False, indent=2).replace("</", "<\\/") + ";\n/*CONFIG-FIN*/"
    html, n = re.subn(r"/\*CONFIG-INICIO\*/.*?/\*CONFIG-FIN\*/", lambda m: bloque, plantilla, count=1, flags=re.S)
    if n != 1:
        sys.exit("No encontré el bloque CONFIG en la plantilla.")
    html = html.replace("<title>Negocio</title>", "<title>" + nombre.replace("<", "") + "</title>", 1)
    out = AQUI / "salida" / slug(nombre)
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(html, encoding="utf-8")
    usa_registro = cfg.get("modulos", {}).get("registro")
    if usa_registro:
        shutil.copy(AQUI / "negocio" / "supabase.sql", out / "supabase.sql")
    prompt = (
        "Convierte EXACTAMENTE este archivo HTML en la página de inicio de este proyecto, conservando "
        "diseño, textos, colores y todo el JavaScript tal cual (incluido el generador de QR y el de PDF). "
        "No uses Lovable Cloud ni agregues backend: el formulario ya guarda en un Supabase externo con la "
        "URL y la clave pública que vienen en CONFIG. No agregues ni quites funciones. Idioma: español.\n\n"
        "```html\n" + html + "\n```\n"
    )
    (out / "PROMPT-LOVABLE.txt").write_text(prompt, encoding="utf-8")
    print("Listo:", out)
    if usa_registro and not sb.get("url"):
        print("Aviso: sin supabase.url la página queda en modo demostración (no guarda).")

if __name__ == "__main__":
    main()
