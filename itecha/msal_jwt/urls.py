from django.urls import path

from.views import MSALLoginView, MSALRedirectView

urlpatterns = [
    path("msal/login", MSALLoginView.as_view()),
    path("msal/redirect", MSALRedirectView.as_view()),
]
