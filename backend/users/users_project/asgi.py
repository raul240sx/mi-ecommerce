import os
from pathlib import Path
from dotenv import load_dotenv
from django.core.asgi import get_asgi_application



BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')



#debug_val = os.getenv('DEBUG')
debug_val = False
if debug_val is None:
    raise RuntimeError("DEBUG no definido en el .env")


if debug_val == 'true':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'users_project.settings.local')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'users_project.settings.production')


application = get_asgi_application()
