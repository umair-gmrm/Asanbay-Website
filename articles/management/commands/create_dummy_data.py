"""
Django management command to create dummy data for testing.
Usage: python manage.py create_dummy_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from datetime import timedelta
from articles.models import Article, ArticleStatus, Author, Category, Tag


class Command(BaseCommand):
    help = 'Creates dummy articles and authors for testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--articles',
            type=int,
            default=15,
            help='Number of articles to create (default: 15)',
        )
        parser.add_argument(
            '--authors',
            type=int,
            default=5,
            help='Number of authors to create (default: 5)',
        )

    def handle(self, *args, **options):
        num_articles = options['articles']
        num_authors = options['authors']

        self.stdout.write(self.style.SUCCESS('Creating dummy data...'))

        # Create a superuser if it doesn't exist (for admin access)
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@asanbay.org',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            self.stdout.write(self.style.SUCCESS('Created superuser: admin (password: admin123)'))

        # Create default category if it doesn't exist
        default_category, created = Category.objects.get_or_create(
            name='General',
            defaults={'slug': 'general', 'description': 'General articles and content'}
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created default category: {default_category.name}'))

        # Create some tags
        tag_names = ["Social Justice", "Community", "Education", "Equality", "Environment", "Healthcare", "Politics"]
        tags = []
        for name in tag_names:
            tag, created = Tag.objects.get_or_create(
                name=name,
                defaults={'slug': slugify(name)}
            )
            tags.append(tag)

        # Create authors
        authors = []
        author_names = [
            'Sarah Johnson',
            'Michael Chen',
            'Emily Rodriguez',
            'David Thompson',
            'Lisa Anderson',
            'James Wilson',
            'Maria Garcia',
            'Robert Brown'
        ]
        
        for i in range(num_authors):
            if i < len(author_names):
                author_name = author_names[i]
            else:
                author_name = f'Author {i+1}'
            
            # Create unique slug
            base_slug = slugify(author_name)
            slug = base_slug
            counter = 1
            while Author.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            author, created = Author.objects.get_or_create(
                slug=slug,
                defaults={
                    'name': author_name,
                    'bio': f'{author_name} is a dedicated writer and advocate for social justice, with expertise in community organizing and policy analysis.',
                    'is_active': True,
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created author: {author.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Author already exists: {author.name}'))
            
            authors.append(author)

        # Sample article titles and content
        article_data = [
            {
                'title': 'Understanding Social Justice in Modern Society',
                'excerpt': 'An in-depth exploration of social justice principles and their application in contemporary society.',
                'content': '''Social justice is a concept that has gained significant attention in recent years. It encompasses the fair distribution of resources, opportunities, and privileges within a society. This article explores the fundamental principles of social justice and how they can be applied to create a more equitable world.

The concept of social justice is rooted in the belief that all individuals should have equal access to wealth, health, well-being, justice, privileges, and opportunity. It challenges the status quo and seeks to address systemic inequalities that prevent certain groups from achieving their full potential.

Key principles include:
- Equity: Ensuring fair treatment for all
- Access: Removing barriers to opportunities
- Participation: Encouraging involvement from all community members
- Rights: Protecting fundamental human rights

By understanding and applying these principles, we can work towards creating a society where everyone has the opportunity to thrive.''',
            },
            {
                'title': 'The Role of Community Organizations in Social Change',
                'excerpt': 'How grassroots organizations drive meaningful change in their communities.',
                'content': '''Community organizations play a crucial role in driving social change at the local level. These grassroots movements often serve as the backbone of social justice initiatives, bringing together individuals who share common goals and values.

Unlike large-scale political movements, community organizations have the advantage of understanding local needs and contexts. They can respond quickly to emerging issues and mobilize resources effectively within their communities.

Successful community organizations typically share several characteristics:
- Strong leadership and clear vision
- Active community engagement
- Transparent decision-making processes
- Sustainable funding and resource management

Through case studies and real-world examples, this article demonstrates how small, focused organizations can create significant impact in their communities.''',
            },
            {
                'title': 'Education as a Tool for Social Justice',
                'excerpt': 'Exploring how education can be leveraged to promote equality and social mobility.',
                'content': '''Education has long been recognized as one of the most powerful tools for promoting social justice. Access to quality education can break cycles of poverty, reduce inequality, and empower individuals to participate fully in society.

However, educational inequality remains a significant challenge. Disparities in funding, resources, and opportunities create barriers that prevent many students from reaching their full potential. Addressing these issues requires a comprehensive approach that considers:

- Early childhood education programs
- Equitable funding distribution
- Teacher training and support
- Community involvement in schools
- Access to technology and resources

This article examines successful initiatives that have improved educational outcomes in underserved communities and discusses strategies for scaling these efforts.''',
            },
            {
                'title': 'Economic Inequality and Its Impact on Society',
                'excerpt': 'Analyzing the causes and consequences of economic inequality in modern economies.',
                'content': '''Economic inequality has reached unprecedented levels in many countries around the world. The gap between the wealthiest and poorest members of society continues to widen, creating social tensions and limiting opportunities for upward mobility.

This article examines the root causes of economic inequality, including:
- Globalization and technological change
- Tax policies and regulatory frameworks
- Access to education and healthcare
- Labor market dynamics

The consequences of extreme inequality extend beyond economics. Research shows that high levels of inequality are associated with:
- Reduced social mobility
- Increased crime rates
- Poorer health outcomes
- Political instability

Addressing economic inequality requires coordinated efforts from governments, businesses, and civil society organizations. This article explores policy solutions and community-based approaches that have shown promise in reducing inequality.''',
            },
            {
                'title': 'Environmental Justice: Connecting Ecology and Equity',
                'excerpt': 'Understanding how environmental issues disproportionately affect marginalized communities.',
                'content': '''Environmental justice is the fair treatment and meaningful involvement of all people regardless of race, color, national origin, or income with respect to the development, implementation, and enforcement of environmental laws, regulations, and policies.

Historically, marginalized communities have borne a disproportionate burden of environmental hazards. Toxic waste sites, polluting industries, and degraded natural resources are often concentrated in low-income and minority neighborhoods.

Key issues in environmental justice include:
- Access to clean air and water
- Exposure to environmental hazards
- Participation in environmental decision-making
- Climate change impacts on vulnerable populations

This article highlights successful environmental justice movements and discusses strategies for ensuring that all communities have equal protection from environmental harm.''',
            },
            {
                'title': 'Healthcare Access and Social Justice',
                'excerpt': 'Examining barriers to healthcare and strategies for ensuring universal access.',
                'content': '''Access to quality healthcare is a fundamental human right, yet millions of people around the world lack adequate medical care. Healthcare disparities based on income, race, geography, and other factors represent a significant social justice issue.

This article explores the various barriers to healthcare access:
- Financial constraints and lack of insurance
- Geographic barriers in rural areas
- Cultural and language barriers
- Discrimination and bias in healthcare settings

The consequences of limited healthcare access are severe, including:
- Preventable deaths and illnesses
- Reduced quality of life
- Economic hardship from medical expenses
- Intergenerational health impacts

Solutions require comprehensive approaches that address both systemic and individual barriers. This article examines successful healthcare access initiatives and discusses policy reforms needed to ensure universal coverage.''',
            },
            {
                'title': 'Criminal Justice Reform: A Path to Equity',
                'excerpt': 'Exploring reforms needed to create a more just and equitable criminal justice system.',
                'content': '''The criminal justice system in many countries faces significant challenges related to fairness, equity, and effectiveness. Disparities in arrest rates, sentencing, and incarceration highlight the need for comprehensive reform.

This article examines key issues in criminal justice:
- Racial and socioeconomic disparities
- Over-incarceration and mandatory minimums
- Access to legal representation
- Rehabilitation and reentry programs

Research shows that certain communities, particularly communities of color and low-income areas, are disproportionately affected by the criminal justice system. These disparities have far-reaching consequences for individuals, families, and communities.

Criminal justice reform requires addressing multiple aspects of the system, including:
- Police practices and community relations
- Sentencing guidelines and alternatives to incarceration
- Prison conditions and rehabilitation programs
- Reentry support and reducing recidivism

This article discusses evidence-based reforms that have shown promise in creating a more just and effective criminal justice system.''',
            },
            {
                'title': 'Housing Justice: The Right to Safe and Affordable Homes',
                'excerpt': 'Addressing housing inequality and homelessness as social justice issues.',
                'content': '''Housing is a fundamental human need, yet millions of people worldwide lack access to safe, affordable, and stable housing. Housing justice advocates for policies and practices that ensure everyone has a place to call home.

This article explores the housing crisis and its impact on communities:
- Rising housing costs and affordability challenges
- Homelessness and housing insecurity
- Discrimination in housing markets
- Gentrification and displacement

The lack of adequate housing has cascading effects on other aspects of life, including:
- Health and well-being
- Educational opportunities
- Employment stability
- Community connections

Solutions to housing injustice require coordinated efforts across multiple sectors. This article examines successful housing programs, including:
- Affordable housing development
- Tenant protections and rent control
- Homelessness prevention and rapid rehousing
- Community land trusts and cooperative housing

By addressing housing as a social justice issue, we can work towards communities where everyone has access to safe, stable, and affordable homes.''',
            },
            {
                'title': 'Gender Equality: Progress and Challenges',
                'excerpt': 'Assessing the state of gender equality and the work that remains.',
                'content': '''Gender equality has made significant progress in recent decades, but substantial challenges remain. This article examines both the achievements and ongoing struggles in the fight for gender equity.

Key areas of progress include:
- Increased representation in education and employment
- Legal protections against discrimination
- Growing awareness of gender-based violence
- Expanded reproductive rights in some regions

However, significant challenges persist:
- Gender pay gaps and occupational segregation
- Underrepresentation in leadership positions
- Gender-based violence and harassment
- Unequal burden of unpaid care work

This article explores the intersectional nature of gender inequality, recognizing that gender intersects with race, class, sexuality, and other identities to create unique experiences of discrimination and privilege.

The path forward requires continued advocacy, policy reform, and cultural change. This article discusses strategies for advancing gender equality, including:
- Policy interventions and legal reforms
- Corporate diversity and inclusion initiatives
- Educational programs and awareness campaigns
- Support for grassroots women's organizations''',
            },
            {
                'title': 'Immigration and Social Justice',
                'excerpt': 'Examining immigration policies through a social justice lens.',
                'content': '''Immigration is a complex social justice issue that touches on questions of human rights, economic opportunity, and national identity. This article explores immigration from a social justice perspective, examining both the challenges and opportunities it presents.

Key issues in immigration justice include:
- Access to legal pathways and documentation
- Family separation and reunification
- Refugee and asylum protections
- Integration and inclusion of immigrant communities

Immigrants often face significant barriers, including:
- Language barriers and limited access to services
- Discrimination and xenophobia
- Exploitation in labor markets
- Limited access to education and healthcare

This article discusses the contributions of immigrant communities and examines policies that promote:
- Fair and humane immigration processes
- Protection of immigrant rights
- Integration and inclusion programs
- Addressing root causes of migration

By approaching immigration through a social justice framework, we can work towards policies that respect human dignity while addressing legitimate concerns about security and economic impact.''',
            },
        ]

        # Create articles
        statuses = [ArticleStatus.PUBLISHED, ArticleStatus.PUBLISHED, ArticleStatus.PUBLISHED, 
                   ArticleStatus.DRAFT, ArticleStatus.ARCHIVED]
        
        created_count = 0
        for i in range(num_articles):
            # Cycle through article data
            article_info = article_data[i % len(article_data)]
            
            # Vary the status
            status = statuses[i % len(statuses)]
            
            # Assign author (cycle through authors)
            author = authors[i % len(authors)]
            
            # Create published date (vary from recent to older)
            days_ago = i * 3
            published_date = timezone.now() - timedelta(days=days_ago) if status == ArticleStatus.PUBLISHED else None
            
            # Create article
            article = Article.objects.create(
                title=f"{article_info['title']} {i+1 if i >= len(article_data) else ''}".strip(),
                content=article_info['content'],
                excerpt=article_info['excerpt'],
                author=author,
                category=default_category,
                status=status,
                published_at=published_date,
            )
            
            # Add random tags to article
            import random
            random_tags = random.sample(tags, k=random.randint(0, min(len(tags), 3)))
            article.tags.set(random_tags)
            
            created_count += 1
            status_display = self.style.SUCCESS if status == ArticleStatus.PUBLISHED else self.style.WARNING
            self.stdout.write(
                f'Created article: "{article.title}" ({status}) by {author.name}'
            )

        self.stdout.write(self.style.SUCCESS(
            f'\nSuccessfully created {created_count} articles!'
        ))
        self.stdout.write(self.style.SUCCESS(
            f'Created {len(authors)} authors for testing.'
        ))
        self.stdout.write(self.style.SUCCESS(
            '\nYou can now:\n'
            '- Visit http://127.0.0.1:8000/ to see published articles\n'
            '- Visit http://127.0.0.1:8000/authors/ to see all authors\n'
            '- Login to admin at http://127.0.0.1:8000/admin/ with username: admin, password: admin123\n'
            '- Test search functionality with various keywords'
        ))

