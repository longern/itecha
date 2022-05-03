import uuid

from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView


class MSALLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        try:
            import msal

            state = request.GET.get("state", str(uuid.uuid4()))
            request.session["msal_state"] = state
            msal_settings = getattr(settings, "MSAL_JWT")

        except ImportError:
            return Response("msal is not installed", status=500)

        except AttributeError:
            return Response("msal is not correctly configured", status=500)

        authorization_request_url = msal.PublicClientApplication(
            msal_settings.get("CLIENT_ID"),
            authority=msal_settings.get(
                "AUTHORITY_URL", "https://login.microsoftonline.com/common/"
            ),
        ).get_authorization_request_url(
            msal_settings.get("SCOPES", ["User.ReadBasic.All"]),
            state=state,
            redirect_uri=msal_settings.get("REDIRECT_URI"),
        )

        return HttpResponseRedirect(authorization_request_url)

    def options(self, request):
        try:
            getattr(settings, "MSAL_JWT")

            return Response(status=200)

        except (ImportError, AttributeError):
            return Response("MSAL is not enabled", status=500)


class MSALRedirectView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        import msal

        msal_settings = getattr(settings, "MSAL_JWT")
        tokens = msal.ConfidentialClientApplication(
            msal_settings.get("CLIENT_ID"),
            client_credential=msal_settings.get("CLIENT_SECRET"),
            authority=msal_settings.get(
                "AUTHORITY_URL", "https://login.microsoftonline.com/common/"
            ),
        ).acquire_token_by_authorization_code(
            request.GET["code"],
            msal_settings.get("SCOPES", ["User.ReadBasic.All"]),
            redirect_uri=msal_settings.get("REDIRECT_URI"),
        )

        if "access_token" in tokens:
            email = tokens["id_token_claims"]["preferred_username"]
            try:
                user = get_user_model().objects.get(email=email)
            except ObjectDoesNotExist:
                user = get_user_model().objects.create_user(username=email, email=email)
            login(request, user)

        return HttpResponseRedirect("/")
