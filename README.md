# Blog Django — PMR3304 Sistemas de Informação

Aplicação de blog desenvolvida com Django para a segunda entrega de laboratório da disciplina PMR3304 — Sistemas de Informação (USP).

## Funcionalidades

- **CRUD de Posts**: criar, listar, visualizar, editar e excluir postagens
- **Comentários**: sistema de comentários vinculados a posts, com autenticação
- **Categorias**: classificação de posts por categorias (ManyToMany)
- **Administração**: painel Django Admin para gerenciamento completo
- **Autenticação**: sistema de login nativo do Django

## Tecnologias

- Python 3.12
- Django 6.1
- SQLite
- HTML/CSS

## Como executar

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Acesse: http://127.0.0.1:8000/

## Estrutura do Projeto

```
├── manage.py
├── config/          # Configurações Django
├── blog/            # App principal (models, views, urls)
├── templates/       # Templates HTML
├── static/          # Arquivos estáticos (CSS)
├── docs/            # Documentação e evidências
└── requirements.txt
```

## Repositório

GitHub: https://github.com/YuriLSRibeiro/Entrega-2-SinInfo

## Autor

Yuri Leonardo Soares Ribeiro — NUSP 14612923  
PMR3304 — Sistemas de Informação — Escola Politécnica da USP — 2026
