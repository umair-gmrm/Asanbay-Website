# Finalize author migration by removing old field and renaming new field

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0006_migrate_authors'),
    ]

    operations = [
        # Remove old author field
        migrations.RemoveField(
            model_name='article',
            name='author',
        ),
        # Rename author_new to author
        migrations.RenameField(
            model_name='article',
            old_name='author_new',
            new_name='author',
        ),
        # Make author field non-nullable
        migrations.AlterField(
            model_name='article',
            name='author',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='articles',
                to='articles.author'
            ),
        ),
    ]

