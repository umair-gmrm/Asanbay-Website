from django.views.generic import ListView, DetailView
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404
from .models import Article, ArticleStatus, Category, Tag, Author


class HomeView(ListView):
    """
    Home page displaying recent articles.
    Shows last 10-15 published articles.
    Categories and tags are displayed for navigation to articles page.
    Home page does NOT filter articles - it only shows recent articles.
    Public access - no login required.
    """
    model = Article
    template_name = 'home.html'
    context_object_name = 'articles'
    paginate_by = None  # Don't paginate on home page, just show recent articles

    def get_queryset(self):
        # Home page always shows recent articles, no filtering
        return Article.objects.filter(
            status=ArticleStatus.PUBLISHED,
            is_active=True
        ).select_related('author', 'category').prefetch_related('tags').order_by('-published_at', '-created_at')[:15]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all active categories and tags for navigation panels
        context['categories'] = Category.objects.filter(is_active=True).order_by('name')
        context['tags'] = Tag.objects.filter(is_active=True).order_by('name')
        
        return context


class ArticleListView(ListView):
    """
    Display a list of published articles.
    Public access - no login required.
    """
    model = Article
    template_name = 'articles/article_list.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        queryset = Article.objects.filter(
            status=ArticleStatus.PUBLISHED,
            is_active=True
        ).select_related('author', 'category').prefetch_related('tags').order_by('-published_at', '-created_at')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = ''  # Initialize search_query for template
        context['categories'] = Category.objects.filter(is_active=True).order_by('name')
        context['selected_category'] = None
        return context


class ArticleDetailView(DetailView):
    """
    Display a single article.
    Public access - no login required.
    """
    model = Article
    template_name = 'articles/article_detail.html'
    context_object_name = 'article'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        # Allow viewing published articles, or draft/archived if user is staff
        queryset = Article.objects.filter(is_active=True).select_related('author', 'category').prefetch_related('tags')
        if not self.request.user.is_staff:
            queryset = queryset.filter(status=ArticleStatus.PUBLISHED)
        return queryset


class ArticleSearchView(ListView):
    """
    Search articles by keywords using simple case-insensitive search.
    HTMX-powered for real-time search results.
    Searches across title, content, and excerpt fields.
    """
    model = Article
    template_name = 'articles/article_list.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_template_names(self):
        # Use partial template for HTMX requests to avoid duplicating navigation
        # HTMX sends HX-Request header, check both headers dict and META
        is_htmx_request = (
            self.request.headers.get('HX-Request') == 'true' or
            self.request.META.get('HTTP_HX_REQUEST') == 'true'
        )
        if is_htmx_request:
            return ['articles/article_list_partial.html']
        return [self.template_name]

    def get_queryset(self):
        query = self.request.GET.get('q', '').strip()
        
        # Base queryset
        queryset = Article.objects.filter(
            status=ArticleStatus.PUBLISHED,
            is_active=True
        ).select_related('author', 'category').prefetch_related('tags')
        
        if not query:
            return queryset.order_by('-published_at', '-created_at')
        
        # Simple case-insensitive search across title, content, and excerpt
        queryset = queryset.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) | 
            Q(excerpt__icontains=query)
        ).order_by('-published_at', '-created_at')
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['categories'] = Category.objects.filter(is_active=True).order_by('name')
        context['selected_category'] = None
        return context


class CategoryFilterView(ListView):
    """
    Filter articles by category.
    Public access - no login required.
    """
    model = Article
    template_name = 'articles/article_list.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        category_slug = self.kwargs.get('slug')
        self.category = get_object_or_404(Category, slug=category_slug, is_active=True)
        
        queryset = Article.objects.filter(
            category=self.category,
            status=ArticleStatus.PUBLISHED,
            is_active=True
        ).select_related('author', 'category').prefetch_related('tags').order_by('-published_at', '-created_at')
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True).order_by('name')
        context['selected_category'] = self.category
        context['search_query'] = ''
        return context


class TagFilterView(ListView):
    """
    Filter articles by tag(s).
    Supports multiple tags with OR logic (articles with any of the selected tags).
    Public access - no login required.
    """
    model = Article
    template_name = 'articles/article_list.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        tag_slugs = self.kwargs.get('slugs', '').split('/')
        # Filter out empty strings
        tag_slugs = [slug for slug in tag_slugs if slug]
        
        if not tag_slugs:
            return Article.objects.none()
        
        # Get tag objects
        tags = Tag.objects.filter(slug__in=tag_slugs, is_active=True)
        if not tags.exists():
            return Article.objects.none()
        
        self.tags = tags
        
        # Filter articles that have any of the selected tags (OR logic)
        queryset = Article.objects.filter(
            tags__in=tags,
            status=ArticleStatus.PUBLISHED,
            is_active=True
        ).select_related('author', 'category').prefetch_related('tags').distinct().order_by('-published_at', '-created_at')
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True).order_by('name')
        context['selected_category'] = None
        context['selected_tags'] = getattr(self, 'tags', Tag.objects.none())
        context['search_query'] = ''
        return context


class AuthorListView(ListView):
    """
    Display a list of all authors.
    Supports sorting: alphabetical (default) or by article count.
    Public access - no login required.
    """
    model = Author
    template_name = 'authors/author_list.html'
    context_object_name = 'authors'
    paginate_by = 20

    def get_queryset(self):
        queryset = Author.objects.filter(is_active=True).annotate(
            published_articles_count=Count(
                'articles',
                filter=Q(articles__status=ArticleStatus.PUBLISHED, articles__is_active=True)
            )
        )
        
        # Get sort parameter
        sort_by = self.request.GET.get('sort', 'name')
        
        if sort_by == 'articles':
            queryset = queryset.order_by('-published_articles_count', 'name')
        else:
            queryset = queryset.order_by('name')
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort_by'] = self.request.GET.get('sort', 'name')
        return context


class AuthorDetailView(DetailView):
    """
    Display an author's profile and their published articles.
    Public access - no login required.
    """
    model = Author
    template_name = 'authors/author_detail.html'
    context_object_name = 'author'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Author.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = self.object
        
        # Get author's published articles, ordered by recency
        articles = Article.objects.filter(
            author=author,
            status=ArticleStatus.PUBLISHED,
            is_active=True
        ).select_related('category').prefetch_related('tags').order_by('-published_at', '-created_at')
        
        context['articles'] = articles
        return context
