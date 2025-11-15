from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from .models import StaticPage


class StaticPageView(DetailView):
    """
    Display a static page (About Us, Content Policies, etc.).
    Public access - no login required.
    Only shows pages that are marked as active.
    """
    model = StaticPage
    template_name = 'core/static_page.html'
    context_object_name = 'page'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return StaticPage.objects.filter(is_active=True)
