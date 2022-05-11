from django.urls import path

from.views import MSALLoginView, MSALRedirectView, MSALRefreshView

urlpatterns = [
    path("msal/login", MSALLoginView.as_view()),
    path("msal/redirect", MSALRedirectView.as_view()),
    path("msal/refresh", MSALRefreshView.as_view()),
]
