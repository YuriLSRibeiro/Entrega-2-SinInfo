import sqlite3

conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()

print("--- TABELAS BLOG ---")
cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'blog%';")
for row in cur.fetchall():
    print(row[0])

print("\n--- SCHEMA BLOG_POST ---")
cur.execute("PRAGMA table_info(blog_post);")
for col in cur.fetchall():
    print(col)

print("\n--- SCHEMA BLOG_COMMENT ---")
cur.execute("PRAGMA table_info(blog_comment);")
for col in cur.fetchall():
    print(col)

print("\n--- SCHEMA BLOG_CATEGORY ---")
cur.execute("PRAGMA table_info(blog_category);")
for col in cur.fetchall():
    print(col)

print("\n--- SCHEMA BLOG_POST_CATEGORIES ---")
cur.execute("PRAGMA table_info(blog_post_categories);")
for col in cur.fetchall():
    print(col)

print("\n--- DADOS POSTS ---")
cur.execute("SELECT id, title, created_at FROM blog_post;")
for row in cur.fetchall():
    print(row)

print("\n--- DADOS CATEGORIAS ---")
cur.execute("SELECT id, name FROM blog_category;")
for row in cur.fetchall():
    print(row)

print("\n--- DADOS POST_CATEGORIES ---")
cur.execute("SELECT * FROM blog_post_categories;")
for row in cur.fetchall():
    print(row)

print("\n--- DADOS COMENTARIOS ---")
cur.execute("SELECT id, post_id, author_id, text, created_at FROM blog_comment;")
for row in cur.fetchall():
    print(row)

conn.close()
