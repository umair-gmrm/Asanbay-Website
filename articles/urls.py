from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('articles/', views.ArticleListView.as_view(), name='list'),
    path('articles/search/', views.ArticleSearchView.as_view(), name='search'),
    path('articles/category/<slug:slug>/', views.CategoryFilterView.as_view(), name='category'),
    path('articles/tag/<path:slugs>/', views.TagFilterView.as_view(), name='tag'),  # path allows multiple slugs separated by /
    path('articles/<slug:slug>/', views.ArticleDetailView.as_view(), name='detail'),
]

