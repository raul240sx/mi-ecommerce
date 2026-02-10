import os
from pathlib import Path
from dotenv import load_dotenv
from django.core.wsgi import get_wsgi_application


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')



debug_val = os.getenv('DEBUG')
if debug_val is None:
    raise RuntimeError("DEBUG no definido en el .env")


if debug_val.lower() == 'true':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products_project.settings.local')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products_project.settings.production')

    

application = get_wsgi_application()
