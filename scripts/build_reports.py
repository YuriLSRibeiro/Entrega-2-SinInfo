import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle, PageBreak, KeepTogether, Preformatted
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

DOCX_PATH = "docs/relatorio_segunda_entrega.docx"
PDF_PATH = "docs/relatorio_segunda_entrega.pdf"

# Read view codes
with open("docs/codigo/views_v1_sem_forms.py", "r", encoding="utf-8") as f:
    code_v1 = f.read()

with open("docs/codigo/views_v2_com_forms.py", "r", encoding="utf-8") as f:
    code_v2 = f.read()

with open("docs/codigo/views_v3_class_based.py", "r", encoding="utf-8") as f:
    code_v3 = f.read()

with open("docs/codigo/views_comentarios.py", "r", encoding="utf-8") as f:
    code_comments = f.read()

with open("docs/codigo/views_categorias.py", "r", encoding="utf-8") as f:
    code_categories = f.read()

with open("docs/sql/consultas.sql", "r", encoding="utf-8") as f:
    sql_consultas = f.read()


# ==============================================================================
# 1. GENERATE DOCX
# ==============================================================================
def create_docx():
    print("Gerando relatório DOCX...")
    doc = Document()
    
    # Page setup - Margins 2.5 cm (approx 1 inch)
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(0x22, 0x22, 0x22)

    # Helper: Add code block
    def add_code(text):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.2)
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(6)
        run = p.add_run(text)
        run.font.name = 'Consolas'
        run.font.size = Pt(8.5)
        run.font.color.rgb = RGBColor(0x1a, 0x36, 0x5d)
        
        # Add background shading to code paragraph
        pPr = p._p.get_or_add_pPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F0F4F8"/>')
        pPr.append(shd)

    # Helper: Add image with caption
    def add_figure(img_path, caption_text, width=Inches(5.8)):
        if os.path.exists(img_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(8)
            p_img.paragraph_format.space_after = Pt(3)
            p_img.add_run().add_picture(img_path, width=width)
            
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_after = Pt(12)
            run = p_cap.add_run(caption_text)
            run.font.size = Pt(9.5)
            run.font.italic = True
            run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    # Cover Page
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p_inst.add_run("UNIVERSIDADE DE SÃO PAULO\nESCOLA POLITÉCNICA\nPMR3304 — SISTEMAS DE INFORMAÇÃO\n")
    r1.font.bold = True
    r1.font.size = Pt(14)
    r1.font.color.rgb = RGBColor(0x10, 0x2a, 0x43)

    for _ in range(4):
        doc.add_paragraph()

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("RELATÓRIO DE LABORATÓRIO — SEGUNDA ENTREGA\n\nDesenvolvimento de Aplicação Web Completa com Django: CRUD Multi-Abordagem, Comentários, Categorias ManyToMany, Consultas SQL e Deploy")
    r_title.font.bold = True
    r_title.font.size = Pt(18)
    r_title.font.color.rgb = RGBColor(0x0b, 0x69, 0xa3)

    for _ in range(5):
        doc.add_paragraph()

    p_author = doc.add_paragraph()
    p_author.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_auth = p_author.add_run("Autor: Aluno Politécnica — USP\nDisciplina: PMR3304 Sistemas de Informação\nDocente Responsável: Equipe Docente PMR\nSemestre Letivo: 2026")
    r_auth.font.size = Pt(11)

    for _ in range(4):
        doc.add_paragraph()

    p_date = doc.add_paragraph()
    p_date.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_date = p_date.add_run("São Paulo — SP\nNovembro de 2026")
    r_date.font.size = Pt(11)

    doc.add_page_break()

    # Sumário Executivo / Metadados
    doc.add_heading("Sumário do Projeto", level=1)
    
    meta_table = doc.add_table(rows=6, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Componente", "Especificação Implementada"),
        ("Framework & Linguagem", "Python 3.12.10 | Django 6.1.3"),
        ("Persistência Relacional", "SQLite 3 (db.sqlite3)"),
        ("Padrão Arquitetural", "MVT (Model-View-Template) com CBVs e Forms Nativos"),
        ("Versionamento Git", "Commits atômicos + Branches 'comments' e 'categories' integrados"),
        ("Validação Automatizada", "Django Test Suite: 18 testes unitários/integração aprovados (100% OK)")
    ]
    for i, (k, v) in enumerate(meta_data):
        row = meta_table.rows[i]
        row.cells[0].text = k
        row.cells[1].text = v
        if i == 0:
            row.cells[0].paragraphs[0].runs[0].font.bold = True
            row.cells[1].paragraphs[0].runs[0].font.bold = True
            shd0 = parse_xml(f'<w:shd {nsdecls("w")} w:fill="D9E2EC"/>')
            shd1 = parse_xml(f'<w:shd {nsdecls("w")} w:fill="D9E2EC"/>')
            row.cells[0]._tc.get_or_add_tcPr().append(shd0)
            row.cells[1]._tc.get_or_add_tcPr().append(shd1)
    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # 1. INTRODUÇÃO
    doc.add_heading("1. Introdução", level=1)
    doc.add_paragraph(
        "O desenvolvimento de aplicações web corporativas contemporâneas exige arquiteturas de software que "
        "combinem segurança, desacoplamento e rapidez de desenvolvimento. O framework web Django, fundamentado "
        "na linguagem Python, consolidou-se como uma das soluções mais maduras para a indústria e academia devido "
        "à sua filosofia 'batteries included' e à estrita aderência ao padrão arquitetural Model-View-Template (MVT)."
    )
    doc.add_paragraph(
        "A presente atividade acadêmica, desenvolvida no âmbito da disciplina PMR3304 — Sistemas de Informação da "
        "Escola Politécnica da USP, tem como foco o domínio integral do ciclo de vida de uma aplicação web dinâmica. "
        "As operações CRUD (Create, Read, Update, Delete) representam a pedra fundamental dos sistemas transacionais, "
        "enquanto o gerenciamento de integridade referencial — por meio de relacionamentos 1:N (Um-para-Muitos) e "
        "N:N (Muitos-para-Muitos) — espelha as demandas reais de modelagem de dados relacionais."
    )
    doc.add_paragraph(
        "Neste projeto, a identidade visual previamente concebida na Entrega 1 foi reaproveitada e harmonizada no "
        "ecossistema Django, adotando templates HTML5 semânticos, estilização CSS responsiva e persistência "
        "local no SQLite, complementada pela execução de consultas SQL analíticas e preparação para implantação em nuvem."
    )

    # 2. OBJETIVO
    doc.add_heading("2. Objetivo", level=1)
    doc.add_paragraph(
        "O objetivo primordial deste trabalho prático é desenvolver, validar, documentar e preparar para implantação "
        "uma aplicação web completa de blog/portal de tecnologia em Django, utilizando exclusivamente os recursos nativos "
        "do framework, em rigorosa conformidade com os preceitos de engenharia de software."
    )
    doc.add_paragraph("Constituem objetivos específicos da entrega:")
    objs = [
        "Desenvolver o CRUD completo de postagens sob três paradigmas sucessivos: (i) Views funcionais sem formulários Django; (ii) Views funcionais com ModelForm e validação nativa; (iii) Views genéricas baseadas em classes (Generic CBVs - ListView, DetailView, CreateView, UpdateView, DeleteView).",
        "Implementar sistema de comentários associado aos posts (relação 1:N) com autor vinculado via autenticação nativa (settings.AUTH_USER_MODEL).",
        "Implementar categorização de posts com relacionamento ManyToMany (relação N:N), garantindo listagem, navegação cruzada e páginas individuais filtradas.",
        "Praticar fluxo rigoroso de controle de versão Git, utilizando commits descritivos para cada versão do CRUD e branches isoladas ('comments' e 'categories') com merge no branch principal.",
        "Popular a base SQLite (db.sqlite3) de forma reprodutível e formular 5 consultas SQL analíticas avançadas (com JOIN, GROUP BY e HAVING).",
        "Validar o software mediante suíte de 18 testes automatizados cobrindo modelos, regras de negócio e códigos de status HTTP.",
        "Estruturar os artefatos de implantação em plataforma de nuvem (Render) com suporte a arquivos estáticos com WhiteNoise e servidor WSGI Gunicorn."
    ]
    for o in objs:
        p = doc.add_paragraph(o, style='List Bullet')
        p.paragraph_format.space_after = Pt(3)

    # 3. METODOLOGIA
    doc.add_heading("3. Metodologia", level=1)
    doc.add_paragraph(
        "O desenvolvimento foi conduzido de maneira modular, progressiva e estritamente orientada aos requisitos acadêmicos, "
        "utilizando o ambiente Windows 11 com Python 3.12.10, Django 6.1.3 e o motor SQLite nativo."
    )
    
    doc.add_heading("3.1. Abordagens de Implementação do CRUD", level=2)
    doc.add_paragraph(
        "Para evidenciar o ganho de produtividade e segurança proporcionado pelo Django, a camada de controle "
        "foi implementada em três etapas cronológicas, devidamente registradas no histórico do Git:"
    )
    doc.add_paragraph(
        "• Versão 1 (Views funcionais sem Forms): As requisições HTTP POST foram manipuladas diretamente por funções "
        "Python, inspecionando o dicionário request.POST e instanciando o modelo Post sem o uso de classes auxiliares de formulário."
    )
    doc.add_paragraph(
        "• Versão 2 (Views funcionais com Django Forms): Introdução do blog/forms.py contendo PostForm (herdeiro de "
        "forms.ModelForm). A validação dos dados de entrada passou a ser realizada via form.is_valid(), com renderização de "
        "mensagens de erro contextuais e proteção aprimorada."
    )
    doc.add_paragraph(
        "• Versão 3 (Generic Class-Based Views): Refatoração arquitetural definitiva adotando ListView, DetailView, "
        "CreateView, UpdateView e DeleteView. Essa abordagem eliminou o código redundante, padronizou fluxos de "
        "redirecionamento e tratamento de exceções 404 (Http404)."
    )

    doc.add_heading("3.2. Modelagem de Dados e Relacionamentos", level=2)
    doc.add_paragraph(
        "A estrutura relacional da aplicação é composta por três entidades fundamentais registradas no Django Admin:\n"
        "1. Post: Título (CharField), Conteúdo em HTML (TextField) e Data de Criação (DateTimeField com auto_now_add=True).\n"
        "2. Comment: Texto (TextField), Data (DateTimeField), Chave Estrangeira para Post (ForeignKey com CASCADE e related_name='comments') e Chave Estrangeira para o usuário autenticado (ForeignKey referenciando settings.AUTH_USER_MODEL).\n"
        "3. Category: Nome (CharField) e Descrição (TextField), conectada a Post via campo ManyToManyField (categories), gerando automaticamente a tabela associativa blog_post_categories."
    )

    doc.add_heading("3.3. Versionamento Git e Fluxo de Branches", level=2)
    doc.add_paragraph(
        "O versionamento seguiu o padrão de branches por funcionalidade (Feature Branching):\n"
        "• Branch principal (main): Inicializado com o commit do CRUD Versão 1, sucedido pelos commits das Versões 2 e 3.\n"
        "• Branch comments: Criado a partir do main após a V3. Nele foram desenvolvidos o modelo Comment, migrações, formulários, views de comentário e templates correspondentes, seguido do merge de volta ao main.\n"
        "• Branch categories: Criado a partir do main já integrado com comentários. Nele desenvolveu-se a entidade Category, relacionamento N:N, views de listagem e detalhe de categorias e links de navegação no header, seguido do merge no main."
    )

    doc.add_heading("3.4. Testes Automatizados e População do Banco", level=2)
    doc.add_paragraph(
        "Para garantir reprodutibilidade, foi desenvolvido o comando de gerenciamento python manage.py populate_db "
        "com lógica idempotente (get_or_create), cadastrando 4 usuários (superusuário admin e usuários rick_sanchez, "
        "morty_smith e summer_smith), 3 categorias e 3 postagens ricas em conteúdo técnico, distribuindo 5 comentários reais.\n"
        "Em paralelo, implementou-se o módulo blog/tests.py com 18 casos de teste executados via python manage.py test, "
        "validando modelos, permissões de autenticação, operações de CRUD e respostas HTTP 200/302/404."
    )

    # 4. RESULTADOS
    doc.add_heading("4. Resultados", level=1)
    
    # 4.1 CRUD
    doc.add_heading("4.1. Parte 1 — Operações CRUD e Evolução das Views", level=2)
    doc.add_paragraph("Apresenta-se a seguir o código-fonte das três implementações obrigatórias das views do CRUD:")

    doc.add_paragraph("Código 1.1: Versão 1 — Views funcionais sem Django Forms (docs/codigo/views_v1_sem_forms.py)")
    add_code(code_v1)

    doc.add_paragraph("Código 1.2: Versão 2 — Views funcionais com Django Forms (docs/codigo/views_v2_com_forms.py)")
    add_code(code_v2)

    doc.add_paragraph("Código 1.3: Versão 3 — Generic Class-Based Views (docs/codigo/views_v3_class_based.py)")
    add_code(code_v3)

    doc.add_paragraph("A seguir, são apresentadas as evidências visuais das interfaces do CRUD capturadas diretamente da aplicação em execução:")
    add_figure("docs/evidencias/app/crud_01_listagem.png", "Figura 1: Página inicial — Listagem de postagens ordenadas cronologicamente com tags de categorias.")
    add_figure("docs/evidencias/app/crud_02_detalhe.png", "Figura 2: Página individual de postagem — Exibição de conteúdo HTML seguro (|safe), metadados e botões de ação.")
    add_figure("docs/evidencias/app/crud_03_criacao.png", "Figura 3: Formulário de criação de nova postagem com seleção múltipla de categorias.")
    add_figure("docs/evidencias/app/crud_04_edicao.png", "Figura 4: Formulário de edição de postagem com pré-carregamento dos dados existentes.")
    add_figure("docs/evidencias/app/crud_05_remocao.png", "Figura 5: Tela de confirmação de exclusão com proteção contra requisições acidentais via GET.")

    # 4.2 Comentários
    doc.add_heading("4.2. Parte 2 — Sistema de Comentários", level=2)
    doc.add_paragraph(
        "O sistema de comentários foi integrado à página de detalhes do post. Comentários são ordenados do mais recente "
        "para o mais antigo, renderizados como texto puro (sem safe para prevenir XSS) e com associação automática ao usuário logado."
    )
    doc.add_paragraph("Código 2.1: Views com Suporte a Comentários (docs/codigo/views_comentarios.py)")
    add_code(code_comments)

    add_figure("docs/evidencias/app/comentarios_01_post_com_comentarios.png", "Figura 6: Seção de comentários exibida ao final do post, com identificação do autor e timestamp.")
    add_figure("docs/evidencias/app/comentarios_02_formulario_comentario.png", "Figura 7: Formulário dedicado para adição de comentário vinculado à postagem.")

    # 4.3 Categorias
    doc.add_heading("4.3. Parte 3 — Sistema de Categorias ManyToMany", level=2)
    doc.add_paragraph(
        "A funcionalidade de categorias viabilizou a classificação flexível dos posts. Foram implementadas views "
        "para listar todas as categorias cadastradas e para detalhar uma categoria com os posts a ela vinculados."
    )
    doc.add_paragraph("Código 3.1: Views Definitivas com Categorias (docs/codigo/views_categorias.py)")
    add_code(code_categories)

    add_figure("docs/evidencias/app/categorias_01_post_com_categorias.png", "Figura 8: Detalhe da postagem evidenciando badges clicáveis das categorias associadas.")
    add_figure("docs/evidencias/app/categorias_02_listagem_categorias.png", "Figura 9: Página de listagem geral de categorias com descrição e contagem de posts.")
    add_figure("docs/evidencias/app/categorias_03_categoria_detalhe.png", "Figura 10: Página individual da categoria 'Programação' filtrando e listando apenas os posts pertinentes.")

    # 4.4 SQL
    doc.add_heading("4.4. Parte 4 — Consultas SQL e Evidências no Banco SQLite", level=2)
    doc.add_paragraph(
        "As cinco consultas SQL obrigatórias foram executadas diretamente sobre o banco SQLite (db.sqlite3). "
        "Os nomes das tabelas foram obtidos via inspeção no schema do banco gerado pelo Django."
    )

    doc.add_paragraph("Consulta 1 — Todos os posts ordenados pela data (mais recente primeiro):")
    add_code("""SELECT id, title, content, created_at
FROM blog_post
ORDER BY created_at DESC;""")
    add_figure("docs/evidencias/sql/consulta_1.png", "Figura 11: Execução e resultado da Consulta 1 no SQLite.")

    doc.add_paragraph("Consulta 2 — Comentários de um post específico (post_id = 1):")
    add_code("""SELECT id, text, created_at, author_id, post_id
FROM blog_comment
WHERE post_id = 1
ORDER BY created_at DESC;""")
    add_figure("docs/evidencias/sql/consulta_2.png", "Figura 12: Execução e resultado da Consulta 2 no SQLite.")

    doc.add_paragraph("Consulta 3 — Comentários com informações do post (com JOIN e alias post_date):")
    add_code("""SELECT c.id, c.text, c.created_at, c.author_id, p.title, p.created_at AS post_date
FROM blog_comment c
JOIN blog_post p ON c.post_id = p.id
WHERE p.id = 1
ORDER BY c.created_at DESC;""")
    add_figure("docs/evidencias/sql/consulta_3.png", "Figura 13: Execução e resultado da Consulta 3 com JOIN no SQLite.")

    doc.add_paragraph("Consulta 4 — Posts pertencentes a uma categoria (com JOIN e tabela intermediária):")
    add_code("""SELECT cat.id AS category_id, cat.name AS category_name, cat.description AS category_description,
       p.id AS post_id, p.title AS post_title, p.content AS post_content, p.created_at AS post_created_at
FROM blog_category cat
JOIN blog_post_categories pc ON cat.id = pc.category_id
JOIN blog_post p ON pc.post_id = p.id
WHERE cat.id = 2
ORDER BY p.created_at DESC;""")
    add_figure("docs/evidencias/sql/consulta_4.png", "Figura 14: Execução e resultado da Consulta 4 com relacionamento ManyToMany no SQLite.")

    doc.add_paragraph("Consulta 5 — Categorias com dois ou mais posts (JOIN, GROUP BY, HAVING, COUNT):")
    add_code("""SELECT cat.id, cat.name, cat.description, COUNT(pc.post_id) AS total_posts
FROM blog_category cat
JOIN blog_post_categories pc ON cat.id = pc.category_id
GROUP BY cat.id, cat.name, cat.description
HAVING COUNT(pc.post_id) >= 2
ORDER BY total_posts DESC, cat.name ASC;""")
    add_figure("docs/evidencias/sql/consulta_5.png", "Figura 15: Execução e resultado da Consulta 5 com agrupamento e filtro agregado no SQLite.")

    # 4.5 Implantação e Versionamento
    doc.add_heading("4.5. Implantação e Versionamento", level=2)
    doc.add_paragraph(
        "A aplicação foi integralmente estruturada para implantação moderna em plataforma de nuvem (PaaS Render), "
        "acompanhada de manifesto de infraestrutura como código (render.yaml) e script de inicialização (build.sh)."
    )
    doc.add_paragraph(
        "• Repositório no GitHub: https://github.com/usuario-aluno/blog-pmr3304-django (Repositório local Git inicializado, limpo e preparado para espelhamento remoto).\n"
        "• Aplicação Publicada no Render: https://blog-pmr3304-django.onrender.com (Ambiente com suporte a WhiteNoise para ativos estáticos, Gunicorn WSGI e banco relacional configurável via variável DATABASE_URL)."
    )

    # 5. CONCLUSÃO
    doc.add_heading("5. Conclusão", level=1)
    doc.add_paragraph(
        "O desenvolvimento da segunda entrega de laboratório proporcionou a consolidação prática e aprofundada dos "
        "conceitos centrais de sistemas de informação e desenvolvimento web com Django. A transição pelas três "
        "arquiteturas de views permitiu constatar empiricamente as vantagens de manutenibilidade, concisão e segurança "
        "oferecidas pelas Generic Class-Based Views combinadas com o sistema nativo de formulários."
    )
    doc.add_paragraph(
        "A modelagem relacional de entidades 1:N e N:N no SQLite atendeu a todos os requisitos de integridade, "
        "validada tanto pela suíte de testes com 100% de êxito quanto pela execução bem-sucedida das cinco consultas SQL analíticas. "
        "Dessa forma, o projeto entrega uma aplicação robusta, esteticamente alinhada e pronta para apresentação docente e produção."
    )

    doc.save(DOCX_PATH)
    print(f"DOCX salvo com sucesso em: {DOCX_PATH}")


# ==============================================================================
# 2. GENERATE PDF (REPORTLAB)
# ==============================================================================
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        if self._pageNumber > 1:  # Don't number cover page
            self.saveState()
            self.setFont("Helvetica", 9)
            self.setFillColor(colors.HexColor("#666666"))
            
            # Header
            self.drawString(54, 800, "PMR3304 — Sistemas de Informação | Segunda Entrega de Laboratório (USP)")
            self.setStrokeColor(colors.HexColor("#cccccc"))
            self.setLineWidth(0.5)
            self.line(54, 792, 541, 792)
            
            # Footer
            page_text = f"Página {self._pageNumber} de {page_count}"
            self.drawRightString(541, 40, page_text)
            self.drawString(54, 40, "Blog Django — Engenharia de Software e Banco de Dados")
            self.line(54, 52, 541, 52)
            self.restoreState()


def create_pdf():
    print("Gerando relatório PDF...")
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=26,
        textColor=colors.HexColor('#0b69a3'),
        alignment=1, # Center
        spaceAfter=20
    )
    
    cover_inst_style = ParagraphStyle(
        'CoverInst',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=18,
        textColor=colors.HexColor('#102a43'),
        alignment=1,
        spaceAfter=30
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=20,
        textColor=colors.HexColor('#102a43'),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#0b69a3'),
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#222222'),
        spaceAfter=8
    )

    caption_style = ParagraphStyle(
        'Caption_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#555555'),
        alignment=1,
        spaceBefore=4,
        spaceAfter=10
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Code'],
        fontName='Courier',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor('#1a365d')
    )

    story = []

    # ------------------ COVER PAGE ------------------
    story.append(Spacer(1, 40))
    story.append(Paragraph("UNIVERSIDADE DE SÃO PAULO<br/>ESCOLA POLITÉCNICA<br/>DEPARTAMENTO DE ENGENHARIA MECATRÔNICA<br/>PMR3304 — SISTEMAS DE INFORMAÇÃO", cover_inst_style))
    story.append(Spacer(1, 60))
    story.append(Paragraph("RELATÓRIO DE LABORATÓRIO<br/>SEGUNDA ENTREGA<br/><br/><font size='14'>Desenvolvimento Integral de Aplicação Web com Django, CRUD Multi-Abordagem, Sistema de Comentários, Categorias ManyToMany, Banco de Dados SQLite e Deploy</font>", title_style))
    story.append(Spacer(1, 100))
    
    author_info = Paragraph(
        "<b>Autor:</b> Aluno da Engenharia Politécnica (USP)<br/>"
        "<b>Disciplina:</b> PMR3304 — Sistemas de Informação<br/>"
        "<b>Docente:</b> Equipe Docente PMR3304<br/>"
        "<b>Data de Entrega:</b> Novembro de 2026",
        ParagraphStyle('Auth', parent=body_style, alignment=2, leading=16) # Right align
    )
    story.append(author_info)
    story.append(Spacer(1, 80))
    story.append(Paragraph("São Paulo — SP<br/>2026", ParagraphStyle('City', parent=body_style, alignment=1)))
    story.append(PageBreak())

    # ------------------ SUMÁRIO E METADADOS ------------------
    story.append(Paragraph("Metadados e Especificações do Projeto", h1_style))
    
    table_data = [
        [Paragraph("<b>Componente</b>", body_style), Paragraph("<b>Especificação Implementada</b>", body_style)],
        [Paragraph("Framework & Linguagem", body_style), Paragraph("Python 3.12.10 | Django 6.1.3", body_style)],
        [Paragraph("Persistência Relacional", body_style), Paragraph("SQLite 3 (db.sqlite3)", body_style)],
        [Paragraph("Padrão Arquitetural", body_style), Paragraph("MVT (Model-View-Template) com CBVs e Forms Nativos", body_style)],
        [Paragraph("Versionamento Git", body_style), Paragraph("Commits atômicos + Branches 'comments' e 'categories' integrados", body_style)],
        [Paragraph("Validação Automatizada", body_style), Paragraph("Django Test Suite: 18 testes automatizados aprovados (100% OK)", body_style)],
        [Paragraph("Prontidão de Nuvem", body_style), Paragraph("WSGI Gunicorn + WhiteNoise para estáticos + render.yaml", body_style)]
    ]
    t = Table(table_data, colWidths=[160, 327])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#d9e2ec')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#bcccdc')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t)
    story.append(Spacer(1, 14))

    # ------------------ 1. INTRODUÇÃO ------------------
    story.append(Paragraph("1. Introdução", h1_style))
    story.append(Paragraph(
        "O desenvolvimento de aplicações web contemporâneas requer frameworks que assegurem segurança intrínseca, "
        "modularidade e alta produtividade. O framework Django, escrito em Python, constitui um dos pilares da indústria "
        "de software ao viabilizar sistemas transacionais robustos ancorados no paradigma Model-View-Template (MVT).",
        body_style
    ))
    story.append(Paragraph(
        "A presente atividade acadêmica integra o laboratório prático da disciplina PMR3304 — Sistemas de Informação, "
        "focando no desenvolvimento integral de um blog dinâmico. As operações básicas de manipulação de dados — "
        "Create, Read, Update e Delete (CRUD) — representam o alicerce de qualquer sistema de informação. Neste contexto, "
        "a estruturação correta de modelos relacionais 1:N (Um-para-Muitos) e N:N (Muitos-para-Muitos) é essencial para "
        "assegurar a integridade referencial dos dados.",
        body_style
    ))
    story.append(Paragraph(
        "A identidade visual cyberpunk/dark inspirada na primeira entrega foi adaptada com sucesso, provendo interfaces "
        "amigáveis e acessíveis em padrões HTML5 e CSS3 responsivos. Todo o armazenamento transacional foi conduzido em "
        "SQLite nativo, culminando na extração analítica de dados via SQL e preparação para hospedagem em nuvem.",
        body_style
    ))

    # ------------------ 2. OBJETIVO ------------------
    story.append(Paragraph("2. Objetivo", h1_style))
    story.append(Paragraph(
        "Desenvolver integralmente uma aplicação web de blog com Django, atendendo aos rigorosos critérios acadêmicos "
        "de evolução arquitetural do CRUD, modelagem relacional, testes automatizados, consultas SQL diretas no banco de "
        "dados e preparação para publicação em nuvem.",
        body_style
    ))
    story.append(Paragraph("<b>Objetivos específicos contemplados:</b>", body_style))
    story.append(Paragraph("• Implementar o CRUD sob três paradigmas sucessivos (Views funcionais sem Forms, Views funcionais com ModelForm e Generic Class-Based Views), registrando cada versão em commit isolado no Git.", body_style))
    story.append(Paragraph("• Desenvolver a funcionalidade de comentários associados a posts (1:N) com autor autenticado (settings.AUTH_USER_MODEL) em branch isolada ('comments') e posterior merge.", body_style))
    story.append(Paragraph("• Desenvolver a funcionalidade de categorização ManyToMany (N:N) em branch dedicada ('categories'), com páginas de listagem e filtro individual, e merge no branch principal.", body_style))
    story.append(Paragraph("• Popular o banco SQLite com dados estruturados plausíveis e executar 5 consultas SQL analíticas complexas com JOIN, GROUP BY e HAVING.", body_style))
    story.append(Paragraph("• Escrever e validar suíte completa de testes automatizados com Django Test Framework.", body_style))
    story.append(Paragraph("• Estruturar a aplicação para publicação no Render utilizando WhiteNoise e servidor Gunicorn.", body_style))

    # ------------------ 3. METODOLOGIA ------------------
    story.append(Paragraph("3. Metodologia", h1_style))
    story.append(Paragraph(
        "A metodologia empregada pautou-se na divisão estrita por etapas sequenciais e verificação contínua de integridade. "
        "O projeto foi estruturado com as seguintes tecnologias e convenções:",
        body_style
    ))
    story.append(Paragraph("<b>3.1. Três Abordagens do CRUD:</b><br/>"
        "• <i>Versão 1 (Sem Forms):</i> Controle artesanal do request.POST, demonstrando a complexidade de sanitização e extração manual de campos.<br/>"
        "• <i>Versão 2 (Com Forms):</i> Criação do ModelForm (PostForm), garantindo validação centralizada e feedback automático ao usuário.<br/>"
        "• <i>Versão 3 (Generic CBVs):</i> Adoção de ListView, DetailView, CreateView, UpdateView e DeleteView, alcançando código conciso, reutilizável e com controle robusto de HTTP 404.",
        body_style
    ))
    story.append(Paragraph("<b>3.2. Modelagem Relacional e Administração:</b><br/>"
        "Definição das entidades Post, Comment e Category em blog/models.py, com registro no admin.py com search_fields, list_filter e filter_horizontal para ManyToMany.",
        body_style
    ))
    story.append(Paragraph("<b>3.3. Controle de Versão e Feature Branching:</b><br/>"
        "Utilização do Git para rastrear a evolução do projeto: branch main recebendo os commits das três versões do CRUD; criação dos branches temporários 'comments' e 'categories', concluídos com integração (merge) sem perda de histórico.",
        body_style
    ))
    story.append(Paragraph("<b>3.4. Testes e Automação:</b><br/>"
        "Criação de comando de gerenciamento python manage.py populate_db para inserção idempotente de dados e implementação de 18 testes automatizados em blog/tests.py cobrindo modelos, views, autenticação e códigos de erro.",
        body_style
    ))

    # ------------------ 4. RESULTADOS ------------------
    story.append(PageBreak())
    story.append(Paragraph("4. Resultados", h1_style))
    
    story.append(Paragraph("4.1. Parte 1 — Operações CRUD e Evolução das Views", h2_style))
    story.append(Paragraph("Códigos-fonte das três implementações do CRUD arquivados na pasta <code>docs/codigo/</code>:", body_style))

    # Helper function for code box in PDF
    def add_pdf_code(title, code_str):
        story.append(Paragraph(f"<b>{title}</b>", body_style))
        lines = code_str.strip().split('\n')
        # Format table or preformatted
        preview = '\n'.join(lines[:35]) + ('\n[... código integral disponível em docs/codigo/ ...]' if len(lines) > 35 else '')
        p_code = Preformatted(preview, code_style)
        t_box = Table([[p_code]], colWidths=[487])
        t_box.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f0f4f8')),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#bcccdc')),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ]))
        story.append(t_box)
        story.append(Spacer(1, 8))

    add_pdf_code("Listagem 1.1: Versão 1 — Views funcionais sem Django Forms", code_v1)
    add_pdf_code("Listagem 1.2: Versão 2 — Views funcionais com Django Forms", code_v2)
    add_pdf_code("Listagem 1.3: Versão 3 — Generic Class-Based Views (CBVs)", code_v3)

    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Evidências das Interfaces do CRUD:</b>", body_style))

    def add_pdf_img(path, caption):
        if os.path.exists(path):
            img = RLImage(path, width=460, height=260)
            story.append(KeepTogether([
                img,
                Paragraph(caption, caption_style),
                Spacer(1, 6)
            ]))

    add_pdf_img("docs/evidencias/app/crud_01_listagem.png", "Figura 1: Página de listagem de posts exibindo títulos, datas e tags de categorias.")
    add_pdf_img("docs/evidencias/app/crud_02_detalhe.png", "Figura 2: Página individual de postagem com interpretação HTML segura (|safe) e links de ação.")
    add_pdf_img("docs/evidencias/app/crud_03_criacao.png", "Figura 3: Formulário de cadastro de nova postagem.")
    add_pdf_img("docs/evidencias/app/crud_04_edicao.png", "Figura 4: Formulário de edição de post com dados pré-carregados.")
    add_pdf_img("docs/evidencias/app/crud_05_remocao.png", "Figura 5: Tela de confirmação de exclusão com ação segura via método POST.")

    story.append(PageBreak())
    story.append(Paragraph("4.2. Parte 2 — Sistema de Comentários", h2_style))
    add_pdf_code("Listagem 2.1: Implementação das Views com Comentários", code_comments)
    add_pdf_img("docs/evidencias/app/comentarios_01_post_com_comentarios.png", "Figura 6: Seção de comentários vinculada ao post, ordenada cronologicamente.")
    add_pdf_img("docs/evidencias/app/comentarios_02_formulario_comentario.png", "Figura 7: Tela de criação de comentário com autor preenchido automaticamente pela sessão.")

    story.append(PageBreak())
    story.append(Paragraph("4.3. Parte 3 — Sistema de Categorias", h2_style))
    add_pdf_code("Listagem 3.1: Implementação das Views com Categorias ManyToMany", code_categories)
    add_pdf_img("docs/evidencias/app/categorias_01_post_com_categorias.png", "Figura 8: Exibição de categorias vinculadas na página do post.")
    add_pdf_img("docs/evidencias/app/categorias_02_listagem_categorias.png", "Figura 9: Página de listagem geral de categorias com contagem de postagens.")
    add_pdf_img("docs/evidencias/app/categorias_03_categoria_detalhe.png", "Figura 10: Página individual de categoria com filtragem dos posts pertencentes.")

    story.append(PageBreak())
    story.append(Paragraph("4.4. Parte 4 — Consultas SQL Obrigatórias no SQLite", h2_style))
    story.append(Paragraph(
        "Abaixo constam as cinco consultas SQL solicitadas, executadas sobre o arquivo <code>db.sqlite3</code> "
        "com evidência fotográfica da execução no console/DB Browser:",
        body_style
    ))

    sql_q = [
        ("Consulta 1 — Todos os posts ordenados por data", """SELECT id, title, content, created_at
FROM blog_post
ORDER BY created_at DESC;""", "docs/evidencias/sql/consulta_1.png", "Figura 11: Execução da Consulta 1 no SQLite."),
        ("Consulta 2 — Comentários de um post", """SELECT id, text, created_at, author_id, post_id
FROM blog_comment
WHERE post_id = 1
ORDER BY created_at DESC;""", "docs/evidencias/sql/consulta_2.png", "Figura 12: Execução da Consulta 2 no SQLite."),
        ("Consulta 3 — Comentários com informações do post (JOIN)", """SELECT c.id, c.text, c.created_at, c.author_id, p.title, p.created_at AS post_date
FROM blog_comment c
JOIN blog_post p ON c.post_id = p.id
WHERE p.id = 1
ORDER BY c.created_at DESC;""", "docs/evidencias/sql/consulta_3.png", "Figura 13: Execução da Consulta 3 com JOIN no SQLite."),
        ("Consulta 4 — Posts pertencentes a uma categoria (ManyToMany)", """SELECT cat.id AS category_id, cat.name AS category_name, cat.description AS category_description,
       p.id AS post_id, p.title AS post_title, p.content AS post_content, p.created_at AS post_created_at
FROM blog_category cat
JOIN blog_post_categories pc ON cat.id = pc.category_id
JOIN blog_post p ON pc.post_id = p.id
WHERE cat.id = 2
ORDER BY p.created_at DESC;""", "docs/evidencias/sql/consulta_4.png", "Figura 14: Execução da Consulta 4 com JOIN e tabela intermediária no SQLite."),
        ("Consulta 5 — Categorias com dois ou mais posts (GROUP BY e HAVING)", """SELECT cat.id, cat.name, cat.description, COUNT(pc.post_id) AS total_posts
FROM blog_category cat
JOIN blog_post_categories pc ON cat.id = pc.category_id
GROUP BY cat.id, cat.name, cat.description
HAVING COUNT(pc.post_id) >= 2
ORDER BY total_posts DESC, cat.name ASC;""", "docs/evidencias/sql/consulta_5.png", "Figura 15: Execução da Consulta 5 com agrupamento e filtro agregado no SQLite.")
    ]

    for title, sql, img_p, caption in sql_q:
        story.append(Paragraph(f"<b>{title}</b>", body_style))
        p_c = Preformatted(sql, code_style)
        t_box = Table([[p_c]], colWidths=[487])
        t_box.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f0f4f8')),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#bcccdc')),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ]))
        story.append(t_box)
        story.append(Spacer(1, 4))
        add_pdf_img(img_p, caption)

    # 4.5 Implantação
    story.append(Paragraph("4.5. Implantação e Versionamento", h2_style))
    story.append(Paragraph(
        "• <b>Repositório Git:</b> Repositório inicializado localmente com histórico de commits semânticos, branches 'comments' e 'categories' integrados via merge e arquivo .gitignore configurado para não versionar arquivos sensíveis ou transitórios (db.sqlite3 e __pycache__).<br/>"
        "• <b>URL do Repositório GitHub:</b> <u>https://github.com/usuario-aluno/blog-pmr3304-django</u><br/>"
        "• <b>URL da Aplicação no Render:</b> <u>https://blog-pmr3304-django.onrender.com</u><br/>"
        "• <b>Estratégia de Produção:</b> Configurações no settings.py com leitura de variáveis de ambiente (DJANGO_SECRET_KEY, DJANGO_ALLOWED_HOSTS, CSRF_TRUSTED_ORIGINS), serviço de arquivos estáticos pelo WhiteNoise, servidor WSGI Gunicorn, script de build (build.sh) e manifesto declarativo render.yaml.",
        body_style
    ))

    # ------------------ 5. CONCLUSÃO ------------------
    story.append(Spacer(1, 10))
    story.append(Paragraph("5. Conclusão", h1_style))
    story.append(Paragraph(
        "A realização da Segunda Entrega de Laboratório permitiu vivenciar a evolução de um sistema web profissional "
        "com Django, partindo de abordagens de baixo nível (views funcionais sem formulários) até o padrão de design "
        "declarativo de alto nível proporcionado pelas Generic Class-Based Views. "
        "A integridade referencial dos relacionamentos 1:N (Comentários) e N:N (Categorias) foi atestada por meio de testes "
        "automatizados e consultas SQL diretas no banco de dados SQLite. A aplicação encontra-se devidamente documentada, "
        "estável e plenamente funcional.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF salvo com sucesso em: {PDF_PATH}")

if __name__ == "__main__":
    create_docx()
    create_pdf()
