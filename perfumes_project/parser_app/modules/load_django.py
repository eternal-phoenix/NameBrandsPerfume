import sys, os, django


sys.path.append(os.path.abspath('perfumes_project'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'perfumes_project.settings'

django.setup()