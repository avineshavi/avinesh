from django.urls import path
from .views import UserRegistrationView, UserLoginView, ShortenedURLCreateView, ShortenedURLDetailView, \
    ShortenedURLListView, ShortenedURLEditView, ShortenedURLDeleteView, UserLogoutView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(),name='user_registration'),
    path('login/', UserLoginView.as_view(),name='user_login'),
    path('logout/', UserLogoutView.as_view(),name='user_logout'),
    path('create/', ShortenedURLCreateView.as_view(),name='Shortened_url_create'),
    path('<str:shortened_code>/', ShortenedURLDetailView.as_view(),name='Shortened_url_detail'),
    path('list/', ShortenedURLListView.as_view(),name='Shortened_url_list'),
    path('<str:shortened_code>/edit', ShortenedURLEditView.as_view(),name='Shortened_url_edit'),
    path('<str:shortened_code>/delete', ShortenedURLDeleteView.as_view(),name='Shortened_url_delete'),
]
