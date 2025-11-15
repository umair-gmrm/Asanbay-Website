from django.db import models
from django.utils.text import slugify


class BaseModel(models.Model):
    """
    Abstract base model with common fields for all models.
    All Django models should inherit from this BaseModel.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class StaticPage(BaseModel):
    """
    Model for managing static pages like About Us, Content Policies, etc.
    Content is stored in database and managed through Django admin.
    """
    title = models.CharField(max_length=200, help_text="Page title (e.g., 'About Us')")
    slug = models.SlugField(max_length=200, unique=True, help_text="URL slug (e.g., 'about-us')")
    content = models.TextField(help_text="Page content (plain text for now, rich text editor optional for future)")
    
    class Meta:
        ordering = ['title']
        verbose_name = "Static Page"
        verbose_name_plural = "Static Pages"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
