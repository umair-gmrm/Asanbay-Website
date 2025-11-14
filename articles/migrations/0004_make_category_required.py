# Generated migration - edited to make category field required

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_set_default_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.ForeignKey(
                help_text='Required: Select a category for this article',
                on_delete=django.db.models.deletion.PROTECT,
                related_name='articles',
                to='articles.category'
            ),
        ),
    ]
