from django.core.management.base import BaseCommand, CommandError
from mesa.comms import amqp
import sys, os

def exception_message(e):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    return 'Exception: %s in %s at line %d. "%s"' % (exc_type, fname, exc_tb.tb_lineno, str(e))


class Command(BaseCommand):
    help = 'Runs the comms backend asynchronously to handle AMQP messaging.'

    #def add_arguments(self, parser):
    #    parser.add_argument('some_arg', nargs='+', type=int)

    def handle(self, *args, **options):
        #try:
        amqp.async_run_forever()
        #except Exception, e:
        #    self.stdout.write(exception_message(e))
            #raise CommandError(e)

        self.stdout.write('Done running comms.')
