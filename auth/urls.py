from django.urls import path

from auth.views import GitHubLogin, GoogleLogin

urlpatterns = [
    path('github/', GitHubLogin.as_view(), name='github_login'),
    path('google/', GoogleLogin.as_view(), name='google_login'),
]