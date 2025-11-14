from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import Article, ArticleStatus, Category, Tag


class HomeView(ListView):
    """
    Home page displaying recent articles.
    Shows last 10-15 published articles.
    Public access - no login required.
    """
    model = Article
    template_name = 'home.html'
    context_object_name = 'articles'
    paginate_by = None  # Don't paginate on home page, just show recent articles

    def get_queryset(self):
        return Article.objects.filter(
            status=ArticleStatus.PUBLISHED,
            is_active=True
        ).select_related('author', 'category').prefetch_related('tags').order_by('-published_at', '-created_at')[:15]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ensure we only show 15 articles (queryset is already limited)
        articles = context.get('articles', [])
        if hasattr(articles, '__iter__') and not isinstance(articles, str):
            context['articles'] = list(articles)[:15]
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
