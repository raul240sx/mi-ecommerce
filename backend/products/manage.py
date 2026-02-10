import os
from pathlib import Path
from dotenv import load_dotenv
import sys



def main():
    BASE_DIR = Path(__file__).resolve().parent
    load_dotenv(BASE_DIR / '.env')


    debug_val = os.getenv('DEBUG')

    if debug_val is None:
        raise RuntimeError(
            "ERROR CRÍTICO: La variable 'DEBUG' no está definida en el .env. "
            "El sistema no puede determinar si debe usar settings de Local o Production."
        )


    """Run administrative tasks."""
    if debug_val.lower() == 'true':
        settings_module = 'products_project.settings.local'
    else:
        settings_module = 'products_project.settings.production'

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)



    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
