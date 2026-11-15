import os
import subprocess
import urllib.request
import urllib.parse
import http.cookiejar

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
BASE_URL = "http://127.0.0.1:8000"

os.makedirs("docs/evidencias/app", exist_ok=True)
os.makedirs("docs/evidencias/sql", exist_ok=True)

# Edge headless screenshot function
def take_screenshot(url, output_path):
    abs_out = os.path.abspath(output_path)
    cmd = [
        EDGE_PATH,
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--window-size=1280,820",
        "--hide-scrollbars",
        f"--screenshot={abs_out}",
        url
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    print(f"Captured: {output_path} (Return code: {res.returncode})")

# Pages to capture directly
pages = [
    (f"{BASE_URL}/", "docs/evidencias/app/crud_01_listagem.png"),
    (f"{BASE_URL}/post/1/", "docs/evidencias/app/crud_02_detalhe.png"),
    (f"{BASE_URL}/post/novo/", "docs/evidencias/app/crud_03_criacao.png"),
    (f"{BASE_URL}/post/1/editar/", "docs/evidencias/app/crud_04_edicao.png"),
    (f"{BASE_URL}/post/1/excluir/", "docs/evidencias/app/crud_05_remocao.png"),
    (f"{BASE_URL}/post/1/", "docs/evidencias/app/comentarios_01_post_com_comentarios.png"),
    (f"{BASE_URL}/post/1/", "docs/evidencias/app/categorias_01_post_com_categorias.png"),
    (f"{BASE_URL}/categorias/", "docs/evidencias/app/categorias_02_listagem_categorias.png"),
    (f"{BASE_URL}/categorias/2/", "docs/evidencias/app/categorias_03_categoria_detalhe.png"),
]

for url, out_path in pages:
    take_screenshot(url, out_path)

# Authenticated comment form capture
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

# GET login page
resp = opener.open(f"{BASE_URL}/accounts/login/")
cookies = {c.name: c.value for c in cj}
csrftoken = cookies.get('csrftoken', '')

# POST login
login_data = urllib.parse.urlencode({
    'username': 'admin',
    'password': 'admin123',
    'csrfmiddlewaretoken': csrftoken
}).encode('utf-8')

req = urllib.request.Request(f"{BASE_URL}/accounts/login/", data=login_data, headers={'Referer': f"{BASE_URL}/accounts/login/"})
opener.open(req)

# GET comment page
comment_resp = opener.open(f"{BASE_URL}/post/1/comentar/")
html_content = comment_resp.read().decode('utf-8')

# Save temp HTML with absolute static path
html_content = html_content.replace('href="/static/', f'href="{BASE_URL}/static/')
tmp_html = os.path.abspath("tmp_comment_form.html")
with open(tmp_html, "w", encoding="utf-8") as f:
    f.write(html_content)

take_screenshot(f"file:///{tmp_html}", "docs/evidencias/app/comentarios_02_formulario_comentario.png")
if os.path.exists(tmp_html):
    os.remove(tmp_html)

print("App screenshots finished successfully.")
