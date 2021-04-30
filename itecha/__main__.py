#!/usr/bin/env python3
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main_without_arguments():
    import webbrowser

    from django.core.management import execute_from_command_line

    execute_from_command_line([sys.argv[0], "migrate"])

    from django.contrib.auth.models import User

    if not User.objects.exists():
        User.objects.create_superuser(username="admin", password="admin")

    webbrowser.open("http://127.0.0.1")

    execute_from_command_line([sys.argv[0], "runserver", "0.0.0.0:80", "--noreload"])


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "itecha.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    if len(sys.argv) <= 1:
        return main_without_arguments()

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
