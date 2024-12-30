from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    # Use the correct template path in the LoginView
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('', views.article_list, name='article_list'),
    path('articles/create/', views.create_article, name='create_article'),
    path('articles/<int:article_id>/', views.article_detail, name='article_detail'),
    path('comments/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('articles/<int:article_id>/delete/', views.delete_article, name='delete_article'),
]
