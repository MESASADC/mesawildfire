from afis_web_basic import *

# The initial syncdb fails if afisweb is present. Workaround:
# Run python manage.py syncdb --settings=settings.afis_web_basic_init
# then run python manage.py syncdb --settings=settings.afis_web_basic

INSTALLED_APPS.remove('afisweb')

