from .models import StaticPage


def static_pages(request):
    """
    Context processor to make active static pages available in all templates.
    """
    return {
        'static_pages': StaticPage.objects.filter(is_active=True).order_by('title')
    }

