from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from blog.models import Post, Comment, Category

User = get_user_model()


class Command(BaseCommand):
    help = 'Popula o banco de dados com dados iniciais realistas para o blog (idempotente)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Iniciando população do banco de dados...'))

        # 1. Usuários
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@usp.br',
                'is_staff': True,
                'is_superuser': True,
                'first_name': 'Administrador',
                'last_name': 'Sistema',
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Superusuário "admin" criado (senha: admin123).'))
        else:
            self.stdout.write('Superusuário "admin" já existente.')

        rick, created = User.objects.get_or_create(
            username='rick_sanchez',
            defaults={
                'email': 'rick@c137.universe',
                'first_name': 'Rick',
                'last_name': 'Sanchez',
            }
        )
        if created:
            rick.set_password('wubba123')
            rick.save()
            self.stdout.write(self.style.SUCCESS('Usuário "rick_sanchez" criado.'))

        morty, created = User.objects.get_or_create(
            username='morty_smith',
            defaults={
                'email': 'morty@smith.universe',
                'first_name': 'Morty',
                'last_name': 'Smith',
            }
        )
        if created:
            morty.set_password('morty123')
            morty.save()
            self.stdout.write(self.style.SUCCESS('Usuário "morty_smith" criado.'))

        summer, created = User.objects.get_or_create(
            username='summer_smith',
            defaults={
                'email': 'summer@smith.universe',
                'first_name': 'Summer',
                'last_name': 'Smith',
            }
        )
        if created:
            summer.set_password('summer123')
            summer.save()
            self.stdout.write(self.style.SUCCESS('Usuário "summer_smith" criado.'))

        # 2. Categorias
        cat_tec, _ = Category.objects.get_or_create(
            name='Tecnologia',
            defaults={
                'description': 'Artigos sobre inovações tecnológicas, infraestrutura, cloud e tendências da indústria.'
            }
        )
        cat_prog, _ = Category.objects.get_or_create(
            name='Programação',
            defaults={
                'description': 'Desenvolvimento de software, linguagens, arquitetura de sistemas e boas práticas de código.'
            }
        )
        cat_cien, _ = Category.objects.get_or_create(
            name='Ciência',
            defaults={
                'description': 'Pesquisa científica, inteligência artificial, física computacional e algoritmos avançados.'
            }
        )
        self.stdout.write(self.style.SUCCESS('Categorias verificadas/criadas (Tecnologia, Programação, Ciência).'))

        # 3. Posts
        post1, created1 = Post.objects.get_or_create(
            title='Construindo Aplicações Web Resilientes com Django e Arquitetura Limpa',
            defaults={
                'content': (
                    '<p>A construção de sistemas corporativos modernos exige modularidade, desacoplamento e '
                    'facilidade de manutenção. O <strong>Django</strong> fornece um ecossistema completo para '
                    'desenvolvimento ágil, garantindo segurança nativa com proteção robusta contra CSRF, SQL Injection '
                    'e Cross-Site Scripting (XSS).</p>'
                    '<p>Neste artigo, exploramos padrões de design como injeção de dependências, separação clara de '
                    'responsabilidades por meio de CBVs (<em>Class-Based Views</em>) e estratégias de cache para '
                    'atingir alta escalabilidade.</p>'
                )
            }
        )
        post1.categories.set([cat_tec, cat_prog])
        post1.save()

        post2, created2 = Post.objects.get_or_create(
            title='Algoritmos Quânticos e Computação de Alto Desempenho em Python',
            defaults={
                'content': (
                    '<p>A convergência entre a mecânica quântica e a ciência da computação inaugura um novo paradigma '
                    'de processamento distribuído. Com bibliotecas open-source como <strong>Qiskit</strong> e <strong>NumPy</strong>, '
                    'é possível simular circuitos quânticos complexos, explorando fenômenos como superposição linear e '
                    'emaranhamento quântico diretamente em Python.</p>'
                    '<p>Apresentamos benchmarks detalhados comparando algoritmos clássicos de fatoração inteira contra a '
                    'execução do Algoritmo de Shor em simuladores de alta densidade de estado.</p>'
                )
            }
        )
        post2.categories.set([cat_prog, cat_cien])
        post2.save()

        post3, created3 = Post.objects.get_or_create(
            title='O Impacto da Inteligência Artificial Generativa na Engenharia de Software',
            defaults={
                'content': (
                    '<p>Modelos de linguagem de grande escala (LLMs) têm transformado radicalmente os fluxos de trabalho '
                    'no desenvolvimento de software moderno. Da síntese automatizada de testes unitários à refatoração '
                    'de código legado, os ganhos de produtividade são tangíveis.</p>'
                    '<p>Discutimos métricas empíricas de adoção na indústria, implicações de segurança e os novos desafios '
                    'de governança de código gerado por assistentes inteligentes.</p>'
                )
            }
        )
        post3.categories.set([cat_tec])
        post3.save()
        self.stdout.write(self.style.SUCCESS('Posts verificados/criados.'))

        # 4. Comentários (Post 1: 3 comentários, Post 2: 2 comentários, Post 3: 0 comentários)
        if not Comment.objects.filter(post=post1).exists():
            Comment.objects.create(
                post=post1,
                author=rick,
                text='Excelente síntese arquitetural. O uso de Class-Based Views reduz drasticamente o código boilerplate mantendo a extensibilidade necessária para sistemas complexos.'
            )
            Comment.objects.create(
                post=post1,
                author=morty,
                text='Muito esclarecedor! No início achei a validação nativa de formulários do Django confusa, mas ela evita erros críticos de segurança.'
            )
            Comment.objects.create(
                post=post1,
                author=summer,
                text='Gostei especialmente da seção sobre proteção contra CSRF e sanitização no ORM. Recomendo a leitura a todos os estagiários do laboratório.'
            )
            self.stdout.write(self.style.SUCCESS('Comentários do Post 1 cadastrados (3 comentários).'))
        else:
            self.stdout.write('Comentários do Post 1 já existem.')

        if not Comment.objects.filter(post=post2).exists():
            Comment.objects.create(
                post=post2,
                author=rick,
                text='Simulações clássicas de circuitos quânticos acima de 30 qubits sofrem com o gargalo da memória exponencial (2^n amplitudes). O verdadeiro salto virá com processadores quânticos tolerantes a falhas.'
            )
            Comment.objects.create(
                post=post2,
                author=morty,
                text='A matemática da Transformada Quântica de Fourier (QFT) explicada no artigo ajudou muito no meu trabalho de graduação. Parabéns!'
            )
            self.stdout.write(self.style.SUCCESS('Comentários do Post 2 cadastrados (2 comentários).'))
        else:
            self.stdout.write('Comentários do Post 2 já existem.')

        self.stdout.write(self.style.SUCCESS('População do banco de dados concluída com sucesso!'))
