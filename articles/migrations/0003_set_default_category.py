# Generated migration - edited to set default category

from django.db import migrations


def create_default_category_and_assign(apps, schema_editor):
    """Create a default category and assign it to all existing articles."""
    Category = apps.get_model('articles', 'Category')
    Article = apps.get_model('articles', 'Article')
    
    # Create default category if it doesn't exist
    default_category, created = Category.objects.get_or_create(
        name='General',
        defaults={
            'slug': 'general',
            'description': 'General articles and content'
        }
    )
    
    # Assign default category to all articles without a category
    Article.objects.filter(category__isnull=True).update(category=default_category)


def reverse_migration(apps, schema_editor):
    """Reverse migration - set category to null for articles with default category."""
    Category = apps.get_model('articles', 'Category')
    Article = apps.get_model('articles', 'Article')
    
    try:
        default_category = Category.objects.get(slug='general')
        Article.objects.filter(category=default_category).update(category=None)
    except Category.DoesNotExist:
        pass


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_add_category_and_tags'),
    ]

    operations = [
        migrations.RunPython(create_default_category_and_assign, reverse_migration),
    ]
