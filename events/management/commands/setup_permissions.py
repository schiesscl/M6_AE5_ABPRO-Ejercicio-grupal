from django.core.management.base import BaseCommand
from events.permissions import setup_groups

class Command(BaseCommand):
    help = 'Configura grupos y permisos para la aplicación de eventos'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('\nConfigurando grupos y permisos...'))
        setup_groups()
        self.stdout.write(self.style.SUCCESS('\n✓ Configuración completada exitosamente\n'))