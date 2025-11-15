from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from core.models import BaseModel


class ArticleStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    PUBLISHED = 'published', 'Published'
    ARCHIVED = 'archived', 'Archived'


class Author(BaseModel):
    """
    Author model for article authors.
    Authors are independent entities managed by admins, not linked to user accounts.
    """
    name = models.CharField(max_length=200, help_text="Author's full name")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    bio = models.TextField(blank=True, help_text="Author biography or description")
    photo = models.ImageField(upload_to='authors/', blank=True, null=True, help_text="Author photo/avatar")
    contact_info = models.TextField(blank=True, help_text="Contact information (optional)")

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_articles_count(self):
        """Return the count of published articles by this author."""
        return self.articles.filter(status=ArticleStatus.PUBLISHED, is_active=True).count()


class Category(BaseModel):
    """
    Category model for organizing articles by topic or theme.
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True, help_text="Optional description of the category")

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(BaseModel):
    """
    Tag model for labeling articles with keywords.
    """
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Article(BaseModel):
    """
    Article model for blog posts.
    Inherits from BaseModel (created_at, updated_at, is_active).
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = models.TextField()
    excerpt = models.TextField(max_length=500, blank=True, help_text="Short summary for article list")
    author = models.ForeignKey(Author, on_delete=models.PROTECT, related_name='articles')
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        related_name='articles',
        help_text="Required: Select a category for this article"
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='articles',
        blank=True,
        help_text="Optional: Add tags to categorize this article"
    )
    status = models.CharField(
        max_length=20,
        choices=ArticleStatus.choices,
        default=ArticleStatus.DRAFT
    )
    published_at = models.DateTimeField(null=True, blank=True, help_text="Publication date")

    class Meta:
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['status', '-published_at']),
            models.Index(fields=['-published_at']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Auto-set published_at when status changes to published
        if self.status == ArticleStatus.PUBLISHED and not self.published_at:
            from django.utils import timezone
            self.published_at = timezone.now()
        # Generate slug from title if not provided
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
