from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from events.models import Event

class Command(BaseCommand):
    help = 'Muestra el contenido de auth_permission y los permisos asignados a cada grupo'

    def handle(self, *args, **kwargs):
        # 1. Explorar la tabla auth_permission
        # Filtramos por el modelo Event para enfocarnos en lo relevante del ejercicio
        self.stdout.write(self.style.WARNING('\n1. EXPLORANDO TABLA AUTH_PERMISSION (Filtrado por app "events")'))
        self.stdout.write('='*80)
        
        try:
            event_content_type = ContentType.objects.get_for_model(Event)
            permissions = Permission.objects.filter(content_type=event_content_type)
            
            self.stdout.write(f"{'ID':<5} | {'Codename':<25} | {'Name'}")
            self.stdout.write('-'*80)
            
            for perm in permissions:
                self.stdout.write(f"{perm.id:<5} | {perm.codename:<25} | {perm.name}")
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error leyendo permisos: {e}"))

        # 2. Confirmar asignación a grupos
        self.stdout.write(self.style.WARNING('\n\n2. CONFIRMANDO PERMISOS POR GRUPO'))
        self.stdout.write('='*80)
        
        groups = Group.objects.prefetch_related('permissions').all()
        
        if not groups.exists():
            self.stdout.write(self.style.ERROR("No existen grupos creados. Ejecuta 'python manage.py setup_permissions' primero."))
            return

        for group in groups:
            self.stdout.write(self.style.SUCCESS(f"\nGrupo: {group.name}"))
            self.stdout.write('-'*40)
            
            group_perms = group.permissions.all()
            if group_perms.exists():
                for perm in group_perms:
                    # Marcamos con [x] los permisos que pertenecen a nuestra app de eventos
                    if perm.content_type == event_content_type:
                        self.stdout.write(f"  [x] {perm.codename:<25} - {perm.name}")
                    else:
                        self.stdout.write(f"  [ ] {perm.codename:<25} - {perm.name}")
            else:
                self.stdout.write(self.style.ERROR("  (Sin permisos asignados)"))
                
        self.stdout.write('\n' + '='*80 + '\n')