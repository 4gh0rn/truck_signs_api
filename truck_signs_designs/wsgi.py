import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'truck_signs_designs.settings.production_docker')

application = get_wsgi_application()
