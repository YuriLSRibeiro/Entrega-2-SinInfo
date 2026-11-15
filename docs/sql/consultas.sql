-- ==============================================================================
-- PMR3304 - SISTEMAS DE INFORMAÇÃO (USP) - SEGUNDA ENTREGA DE LABORATÓRIO
-- ARQUIVO: docs/sql/consultas.sql
-- BANCO DE DADOS: SQLite (db.sqlite3 gerado pelo Django)
-- DESCRIÇÃO: Consultas SQL obrigatórias executadas sobre a estrutura do blog
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- Consulta 1 — Todos os posts, ordenados pela data
-- Finalidade: Retornar todos os registros da tabela de postagens (blog_post),
-- ordenados da publicação mais recente para a mais antiga.
-- ------------------------------------------------------------------------------
SELECT 
    id, 
    title, 
    content, 
    created_at
FROM 
    blog_post
ORDER BY 
    created_at DESC;


-- ------------------------------------------------------------------------------
-- Consulta 2 — Comentários de um post
-- Finalidade: Selecionar uma postagem específica (neste caso, post_id = 1) e 
-- listar todos os comentários associados a ela, ordenados cronologicamente.
-- ------------------------------------------------------------------------------
SELECT 
    id, 
    text, 
    created_at, 
    author_id, 
    post_id
FROM 
    blog_comment
WHERE 
    post_id = 1
ORDER BY 
    created_at DESC;


-- ------------------------------------------------------------------------------
-- Consulta 3 — Comentários com informações do post
-- Finalidade: Retornar todos os comentários de um post (todas as colunas da 
-- tabela blog_comment exceto post_id), acrescidos do título do post e de sua 
-- data de publicação sob o alias 'post_date'. Utiliza INNER JOIN entre blog_comment 
-- e blog_post.
-- ------------------------------------------------------------------------------
SELECT 
    c.id, 
    c.text, 
    c.created_at, 
    c.author_id, 
    p.title, 
    p.created_at AS post_date
FROM 
    blog_comment c
JOIN 
    blog_post p ON c.post_id = p.id
WHERE 
    p.id = 1
ORDER BY 
    c.created_at DESC;


-- ------------------------------------------------------------------------------
-- Consulta 4 — Posts pertencentes a uma categoria
-- Finalidade: Selecionar uma categoria específica (id = 2, 'Programação') e 
-- retornar todas as colunas da tabela de categorias combinadas com todas as colunas
-- das postagens pertencentes a essa categoria. Utiliza JOIN duplo contemplando
-- a tabela associativa intermediária ManyToMany (blog_post_categories).
-- ------------------------------------------------------------------------------
SELECT 
    cat.id AS category_id, 
    cat.name AS category_name, 
    cat.description AS category_description,
    p.id AS post_id, 
    p.title AS post_title, 
    p.content AS post_content, 
    p.created_at AS post_created_at
FROM 
    blog_category cat
JOIN 
    blog_post_categories pc ON cat.id = pc.category_id
JOIN 
    blog_post p ON pc.post_id = p.id
WHERE 
    cat.id = 2
ORDER BY 
    p.created_at DESC;


-- ------------------------------------------------------------------------------
-- Consulta 5 — Categorias com dois ou mais posts
-- Finalidade: Identificar e retornar todas as categorias que possuem pelo menos 
-- dois posts vinculados. Utiliza JOIN com a tabela intermediária, agrupamento
-- com GROUP BY pelas colunas da categoria, e filtro agregado com HAVING COUNT >= 2.
-- ------------------------------------------------------------------------------
SELECT 
    cat.id, 
    cat.name, 
    cat.description, 
    COUNT(pc.post_id) AS total_posts
FROM 
    blog_category cat
JOIN 
    blog_post_categories pc ON cat.id = pc.category_id
GROUP BY 
    cat.id, 
    cat.name, 
    cat.description
HAVING 
    COUNT(pc.post_id) >= 2
ORDER BY 
    total_posts DESC, 
    cat.name ASC;
