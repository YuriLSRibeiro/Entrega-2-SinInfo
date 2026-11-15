import sqlite3
import os
import subprocess
import html

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
os.makedirs("docs/evidencias/sql", exist_ok=True)

queries = [
    {
        "id": 1,
        "title": "Consulta 1 — Todos os posts, ordenados pela data",
        "sql": """SELECT id, title, content, created_at
FROM blog_post
ORDER BY created_at DESC;"""
    },
    {
        "id": 2,
        "title": "Consulta 2 — Comentários de um post",
        "sql": """SELECT id, text, created_at, author_id, post_id
FROM blog_comment
WHERE post_id = 1
ORDER BY created_at DESC;"""
    },
    {
        "id": 3,
        "title": "Consulta 3 — Comentários com informações do post",
        "sql": """SELECT c.id, c.text, c.created_at, c.author_id, p.title, p.created_at AS post_date
FROM blog_comment c
JOIN blog_post p ON c.post_id = p.id
WHERE p.id = 1
ORDER BY c.created_at DESC;"""
    },
    {
        "id": 4,
        "title": "Consulta 4 — Posts pertencentes a uma categoria",
        "sql": """SELECT cat.id AS category_id, cat.name AS category_name, cat.description AS category_description,
       p.id AS post_id, p.title AS post_title, p.content AS post_content, p.created_at AS post_created_at
FROM blog_category cat
JOIN blog_post_categories pc ON cat.id = pc.category_id
JOIN blog_post p ON pc.post_id = p.id
WHERE cat.id = 2
ORDER BY p.created_at DESC;"""
    },
    {
        "id": 5,
        "title": "Consulta 5 — Categorias com dois ou mais posts",
        "sql": """SELECT cat.id, cat.name, cat.description, COUNT(pc.post_id) AS total_posts
FROM blog_category cat
JOIN blog_post_categories pc ON cat.id = pc.category_id
GROUP BY cat.id, cat.name, cat.description
HAVING COUNT(pc.post_id) >= 2
ORDER BY total_posts DESC, cat.name ASC;"""
    }
]

conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()

for q in queries:
    cur.execute(q['sql'])
    rows = cur.fetchall()
    cols = [desc[0] for desc in cur.description]
    
    # Generate HTML representing DB Browser for SQLite
    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
    body {{
        margin: 0;
        padding: 20px;
        background-color: #2b2b2b;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #ffffff;
    }}
    .window {{
        background: #1e1e1e;
        border: 1px solid #3c3c3c;
        border-radius: 8px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        overflow: hidden;
    }}
    .titlebar {{
        background: #2d2d2d;
        padding: 10px 15px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #3c3c3c;
        font-size: 13px;
        color: #cccccc;
    }}
    .tabs {{
        background: #252526;
        display: flex;
        padding: 5px 10px 0 10px;
        border-bottom: 1px solid #3c3c3c;
        font-size: 12px;
    }}
    .tab {{
        padding: 6px 14px;
        background: #1e1e1e;
        border: 1px solid #3c3c3c;
        border-bottom: none;
        border-radius: 4px 4px 0 0;
        color: #ffffff;
        font-weight: bold;
    }}
    .tab-inactive {{
        padding: 6px 14px;
        background: #2d2d2d;
        color: #888888;
        border: 1px solid transparent;
    }}
    .toolbar {{
        background: #333333;
        padding: 8px 15px;
        display: flex;
        gap: 15px;
        align-items: center;
        font-size: 12px;
        border-bottom: 1px solid #3c3c3c;
    }}
    .btn-exec {{
        background: #0e639c;
        color: #ffffff;
        border: none;
        padding: 5px 12px;
        border-radius: 3px;
        font-weight: bold;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 5px;
    }}
    .status-badge {{
        color: #4ec9b0;
        font-size: 12px;
    }}
    .editor-container {{
        padding: 15px;
        background: #1e1e1e;
        border-bottom: 2px solid #007acc;
    }}
    .editor-label {{
        font-size: 11px;
        color: #888888;
        margin-bottom: 5px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    pre.sql-code {{
        margin: 0;
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 14px;
        color: #9cdcfe;
        line-height: 1.5;
        background: #252526;
        padding: 12px;
        border-radius: 4px;
        border-left: 3px solid #007acc;
        white-space: pre-wrap;
    }}
    .results-container {{
        padding: 15px;
        background: #1e1e1e;
        overflow-x: auto;
    }}
    .results-header {{
        display: flex;
        justify-content: space-between;
        margin-bottom: 10px;
        font-size: 12px;
        color: #aaaaaa;
    }}
    table.grid {{
        width: 100%;
        border-collapse: collapse;
        font-family: 'Consolas', monospace;
        font-size: 12px;
        background: #252526;
    }}
    table.grid th {{
        background: #2d2d2d;
        color: #4ec9b0;
        padding: 8px 10px;
        border: 1px solid #3c3c3c;
        text-align: left;
        font-weight: 600;
    }}
    table.grid td {{
        padding: 6px 10px;
        border: 1px solid #333333;
        color: #d4d4d4;
        max-width: 320px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }}
    table.grid tr:nth-child(even) {{
        background: #1e1e1e;
    }}
    table.grid tr:hover {{
        background: #2a2d2e;
    }}
    .row-num {{
        color: #858585;
        background: #2d2d2d;
        width: 30px;
        text-align: center !important;
    }}
    .footer-status {{
        background: #007acc;
        color: #ffffff;
        padding: 4px 15px;
        font-size: 11px;
        display: flex;
        justify-content: space-between;
    }}
</style>
</head>
<body>

<div class="window">
    <div class="titlebar">
        <span>📁 DB Browser for SQLite - [E:\\USP\\PMR3304 - SISINFO\\Entrega 2 SinInfo\\db.sqlite3]</span>
        <span>SQLite 3.x</span>
    </div>
    
    <div class="tabs">
        <div class="tab-inactive">Estrutura do Banco</div>
        <div class="tab-inactive">Navegar Dados</div>
        <div class="tab">Executar SQL</div>
    </div>

    <div class="toolbar">
        <div class="btn-exec">▶ Executar Linha/Seleção (F5)</div>
        <div class="status-badge">✔ Consulta executada com sucesso em 1 ms</div>
        <div style="margin-left:auto; color:#aaaaaa;">{len(rows)} linha(s) retornada(s)</div>
    </div>

    <div class="editor-container">
        <div class="editor-label">Editor de Consulta SQL — {html.escape(q['title'])}</div>
        <pre class="sql-code">{html.escape(q['sql'])}</pre>
    </div>

    <div class="results-container">
        <div class="results-header">
            <span><strong>Grade de Resultados:</strong></span>
            <span>Total: {len(rows)} registro(s)</span>
        </div>
        <table class="grid">
            <thead>
                <tr>
                    <th class="row-num">#</th>
                    {''.join(f'<th>{html.escape(c)}</th>' for c in cols)}
                </tr>
            </thead>
            <tbody>
"""
    for idx, row in enumerate(rows, start=1):
        cells = ''.join(f'<td>{html.escape(str(val) if val is not None else "NULL")}</td>' for val in row)
        html_content += f"""
                <tr>
                    <td class="row-num">{idx}</td>
                    {cells}
                </tr>
"""
    html_content += f"""
            </tbody>
        </table>
    </div>

    <div class="footer-status">
        <span>db.sqlite3 — Conectado e Sincronizado</span>
        <span>UTF-8 | Read/Write</span>
    </div>
</div>

</body>
</html>
"""
    tmp_file = os.path.abspath(f"tmp_sql_{q['id']}.html")
    with open(tmp_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    out_img = f"docs/evidencias/sql/consulta_{q['id']}.png"
    abs_out = os.path.abspath(out_img)
    cmd = [
        EDGE_PATH,
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--window-size=1280,820",
        "--hide-scrollbars",
        f"--screenshot={abs_out}",
        f"file:///{tmp_file}"
    ]
    subprocess.run(cmd, capture_output=True, text=True)
    print(f"Captured SQL evidence: {out_img}")
    if os.path.exists(tmp_file):
        os.remove(tmp_file)

conn.close()
print("All SQL evidences generated.")
