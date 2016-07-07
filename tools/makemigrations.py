"""
Script for creating migration for each application listed in
settings.py:INSTALLED_APPLICATIONS
"""
import os


def main():
    """
    Main method for script

    :return: None
    """
    from pineapple.settings import INSTALLED_APPS
    for app in INSTALLED_APPS:
        print("Make migration for {0}".format(app))
        try:
            os.system("python manage.py makemigrations --noinput " + app.split('.')[-1])
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()
