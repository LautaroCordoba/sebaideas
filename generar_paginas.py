import os
import re
import html

# --- Configuración de rutas ---
base_path = "ideas"  # Carpeta que contiene todas las carpetas de ideas
index_file = "index.html"
indigenas_file = "indigenas_liwres_autonomos.html"
links_list = []

# --- Función para extraer número de carpeta ---
def obtener_numero(carpeta):
    match = re.match(r"(\d+)", carpeta)
    return int(match.group(1)) if match else 9999

# --- Cabecera HTML común para todas las páginas ---
def generar_header(rel_path_to_root="."):
    index_rel = os.path.relpath(index_file, start=rel_path_to_root)
    indigenas_rel = os.path.relpath(indigenas_file, start=rel_path_to_root)
    return f"""
<header id="mainHeader">
    <div><a href="{index_rel}" style="color: inherit; text-decoration:none;">ideas de seba</a></div>
    <div><a href="{indigenas_rel}" style="color: inherit; text-decoration:none;">indígenas libres autónomos</a></div>
</header>
"""

# --- Generamos páginas individuales de cada idea ---
for folder in sorted(os.listdir(base_path), key=obtener_numero):
    folder_path = os.path.join(base_path, folder)
    if not os.path.isdir(folder_path):
        continue

    try:
        # Extraer nombre de la idea desde TXT
        txt_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".txt")]
        if txt_files:
            txt_file = os.path.join(folder_path, txt_files[0])
            with open(txt_file, "r", encoding="utf-8") as f:
                idea_name = f.read().strip()
        else:
            idea_name = folder

        idea_name_html = html.escape(idea_name)

        # Número y nombre sin número
        match = re.match(r"^(\d+)\s", idea_name)
        if match:
            numero = match.group(1)
            nombre_sin_num = idea_name[len(match.group(0)):]
        else:
            numero = str(obtener_numero(folder))
            nombre_sin_num = idea_name

        # Lista de imágenes válidas
        images = sorted([f for f in os.listdir(folder_path) if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp", ".gif", ".jfif"))])

        # Crear HTML de la idea
        header_html = generar_header(rel_path_to_root=folder_path)
        output_file = os.path.join(folder_path, f"{numero}.html")
        link_rel = os.path.relpath(output_file, start=os.path.dirname(index_file))
        links_list.append((int(numero), link_rel, nombre_sin_num))

        html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>{idea_name_html}</title>
<style>
html, body {{
    margin: 0;
    padding: 0;
}}
body {{
    font-family: "Consolas", monospace;
    background: #f4f4f4;
}}
header {{
    position: fixed;
    top: 0;
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 20px;
    background-color: white;
    color: black;
    font-size: 24px;
    font-weight: bold;
    z-index: 1000;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    box-sizing: border-box;
    text-transform: lowercase;
}}
header a {{ color: inherit; text-decoration: none; }}
header a:hover {{ color: #007BFF; }}
.content-wrapper {{
    padding: 80px 20px 20px 20px;
    text-align: center;
}}
h1 {{
    font-size: 28px;
    text-align: center;
}}
.numero {{
    color: #800080;
    font-weight: bold;
}}
.gallery {{
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 15px;
    margin-top: 20px;
}}
.gallery img {{
    max-width: 300px;
    height: auto;
    border: 2px solid #333;
    border-radius: 5px;
}}
</style>
</head>
<body>
{header_html}
<div class="content-wrapper">
<h1><span class="numero">{numero}</span> {html.escape(nombre_sin_num)}</h1>
<div class="gallery">
"""
        for img in images:
            html_content += f'  <img src="{img}" alt="{idea_name_html}">\n'
        html_content += "</div>\n</div>\n</body>\n</html>"

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html_content)

    except Exception as e:
        print(f"Error en la carpeta {folder}: {e}")
        continue

# --- index.html ---
header_html_index = generar_header(rel_path_to_root=os.path.dirname(index_file))
index_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Index de Ideas</title>
<style>
html, body {{
    margin: 0;
    padding: 0;
}}
body {{
    font-family: "Consolas", monospace;
    background: #f0f0f0;
}}
header {{
    position: fixed;
    top: 0;
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 20px;
    background-color: white;
    color: black;
    font-size: 24px;
    font-weight: bold;
    z-index: 1000;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    box-sizing: border-box;
    text-transform: lowercase;
}}
header a {{
    color: inherit;
    text-decoration: none;
}}
header a:hover {{ color: #007BFF; }}
.content-wrapper {{
    padding: 80px 20px 20px 20px;
    text-align: center;
}}
.div_link {{
    margin: 25px 0;
    font-size: 20px;
}}
.numero {{
    color: #800080;
    font-weight: bold;
}}
a.divlink {{
    color: black;
    text-decoration: none;
}}
a.divlink:hover {{
    color: #007BFF;
}}
hr {{
    border: none;
    border-top: 1px solid #ccc;
    margin: 10px auto;
    width: 50%;
}}
</style>
</head>
<body>
{header_html_index}
<div class="content-wrapper">
"""

for num, link, name in sorted(links_list):
    index_content += f'<div class="div_link"><a class="divlink" href="{link}"><span class="numero">{num}</span> {html.escape(name)}</a></div>\n<hr>\n'

index_content += "</div></body></html>"

with open(index_file, "w", encoding="utf-8") as f:
    f.write(index_content)

# --- Página indígenas ---
header_html_indigenas = generar_header(rel_path_to_root=os.path.dirname(indigenas_file))
imagen_indi_path = os.path.relpath(os.path.join(base_path, "indi.png"), start=os.path.dirname(indigenas_file))

indigenas_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Indígenas Libres Autónomos</title>
<style>
html, body {{
    margin: 0;
    padding: 0;
}}
body {{
    font-family: "Consolas", monospace;
    background: #f4f4f4;
}}
header {{
    position: fixed;
    top: 0;
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 20px;
    background-color: white;
    color: black;
    font-size: 24px;
    font-weight: bold;
    z-index: 1000;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    box-sizing: border-box;
    text-transform: lowercase;
}}
header a {{ color: inherit; text-decoration: none; }}
header a:hover {{ color: #007BFF; }}
.content-wrapper {{
    padding: 80px 20px 20px 20px;
}}
h1 {{
    font-size: 28px;
    font-weight: bold;
    color: #FF69B4;
    margin-bottom: 20px;
    text-align: center;
    text-transform: lowercase;
}}
.intro {{
    text-align: left;
    font-weight: bold;
    margin-bottom: 20px;
}}
.img_indi {{
    display: block;
    margin: 20px auto;
    max-width: 400px;
    height: auto;
    object-fit: contain;
    border-radius: 8px;
}}
</style>
</head>
<body>
{header_html_indigenas}

<div class="content-wrapper">
<h1>indígenas liwres autónomos</h1>

<div class="intro">
hola soy sergio sebastian costilla les explico que mi intención fue y es decirles propaganda de gente que verdaderamente trabaja y de personas que quieren progresar
si no le interesa no le preste atención pero si hay gente que si trabaja de enserio y hay personas que si quieren progresar les explico que yo sergio sebastian costilla vuelvo a insistir desde el año 2015 que si yo beneficie a progresar ya puede venir personalmente a mi dirección ernesto renan 75 parque san martin libertad merlo gran buenos aires argentina y dejar personalmente las ayudas con lo que puedan
</div>

<img src="{imagen_indi_path}" alt="Indígenas" class="img_indi">

</div>
</body>
</html>
"""

with open(indigenas_file, "w", encoding="utf-8") as f:
    f.write(indigenas_content)

print(f"Index actualizado: {index_file}")
print(f"Páginas de ideas creadas con galería organizada y tamaño fijo")
print(f"Página de indígenas creada SIN datos personales, con imagen centrada y texto explicativo: {indigenas_file}")
