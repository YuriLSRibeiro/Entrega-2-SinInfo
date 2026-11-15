import sqlite3

conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()

queries = [
    ("Consulta 1 — Todos os posts, ordenados pela data", """
SELECT id, title, created_at
FROM blog_post
ORDER BY created_at DESC;
    """),
    ("Consulta 2 — Comentários de um post", """
SELECT id, text, created_at, author_id, post_id
FROM blog_comment
WHERE post_id = 1
ORDER BY created_at DESC;
    """),
    ("Consulta 3 — Comentários com informações do post", """
SELECT c.id, c.text, c.created_at, c.author_id, p.title, p.created_at AS post_date
FROM blog_comment c
JOIN blog_post p ON c.post_id = p.id
WHERE p.id = 1
ORDER BY c.created_at DESC;
    """),
    ("Consulta 4 — Posts pertencentes a uma categoria", """
SELECT cat.id AS cat_id, cat.name AS cat_name, cat.description,
       p.id AS post_id, p.title, p.created_at
FROM blog_category cat
JOIN blog_post_categories pc ON cat.id = pc.category_id
JOIN blog_post p ON pc.post_id = p.id
WHERE cat.id = 2
ORDER BY p.created_at DESC;
    """),
    ("Consulta 5 — Categorias com dois ou mais posts", """
SELECT cat.id, cat.name, cat.description, COUNT(pc.post_id) AS total_posts
FROM blog_category cat
JOIN blog_post_categories pc ON cat.id = pc.category_id
GROUP BY cat.id, cat.name, cat.description
HAVING COUNT(pc.post_id) >= 2
ORDER BY total_posts DESC, cat.name ASC;
    """)
]

for title, sql in queries:
    print(f"\n==========================================")
    print(f"{title}")
    print(f"==========================================")
    print("SQL:\n" + sql.strip())
    print("\nRESULTADOS:")
    cur.execute(sql.strip())
    rows = cur.fetchall()
    col_names = [description[0] for description in cur.description]
    print(f"Colunas: {col_names}")
    for row in rows:
        print(row)
    print(f"Total de linhas retornadas: {len(rows)}")

conn.close()
