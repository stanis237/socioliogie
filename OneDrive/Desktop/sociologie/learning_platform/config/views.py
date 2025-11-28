from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import os
from django.conf import settings

class FrontendAppView(View):
    """
    Servir la build React complète en production ou rediriger vers le serveur de développement.
    """
    def get(self, request, *args, **kwargs):
        if settings.DEBUG:
            # En mode développement, rediriger vers le serveur React (port 3000)
            frontend_url = f"http://localhost:3000{request.get_full_path()}"
            return HttpResponseRedirect(frontend_url)
        else:
            # En production, servir la build React
            try:
                with open(os.path.join(settings.BASE_DIR, 'frontend', 'build', 'index.html')) as file:
                    return HttpResponse(file.read())
            except FileNotFoundError:
                return HttpResponse(
                    "La build React n'a pas été trouvée. "
                    "Effectuez un 'npm run build' dans le dossier frontend.",
                    status=501,
                )
