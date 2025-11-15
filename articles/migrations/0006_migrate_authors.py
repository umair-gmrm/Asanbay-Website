# Data migration to migrate User authors to Author model

from django.db import migrations
from django.utils.text import slugify


def migrate_authors(apps, schema_editor):
    """Create Author records from existing User authors and migrate Article.author to Article.author_new."""
    Author = apps.get_model('articles', 'Author')
    Article = apps.get_model('articles', 'Article')
    User = apps.get_model('auth', 'User')
    
    # Get all unique users who have authored articles
    articles = Article.objects.all()
    user_author_map = {}
    
    for article in articles:
        user = article.author
        if user.id not in user_author_map:
            # Create author name from user's full name or username
            author_name = user.get_full_name().strip() if user.get_full_name().strip() else user.username
            
            # Create unique slug
            base_slug = slugify(author_name)
            slug = base_slug
            counter = 1
            while Author.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            # Create Author record
            author, created = Author.objects.get_or_create(
                slug=slug,
                defaults={
                    'name': author_name,
                    'bio': f'Author profile for {author_name}',
                    'is_active': True,
                }
            )
            user_author_map[user.id] = author
    
    # Update all articles to use the new author field
    for article in articles:
        if article.author.id in user_author_map:
            article.author_new = user_author_map[article.author.id]
            article.save(update_fields=['author_new'])


def reverse_migration(apps, schema_editor):
    """Reverse migration - set author_new to None."""
    Article = apps.get_model('articles', 'Article')
    Article.objects.all().update(author_new=None)


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0005_create_author_model'),
    ]

    operations = [
        migrations.RunPython(migrate_authors, reverse_migration),
    ]

