from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from events.models import Event
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Crea usuarios de prueba con diferentes roles'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('\n' + '='*60))
        self.stdout.write(self.style.WARNING('CREANDO USUARIOS Y EVENTOS DE PRUEBA'))
        self.stdout.write(self.style.WARNING('='*60 + '\n'))

        # Obtener grupos
        admin_group = Group.objects.get(name='Administradores')
        organizer_group = Group.objects.get(name='Organizadores')
        attendee_group = Group.objects.get(name='Asistentes')

        # Crear Administrador
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_user(
                username='admin',
                password='admin123',
                email='admin@eventos.com',
                first_name='Carlos',
                last_name='Administrador'
            )
            admin_user.groups.add(admin_group)
            admin_user.is_staff = True
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('✓ Usuario Administrador creado'))
            self.stdout.write(f'  Username: admin | Password: admin123')
        else:
            admin_user = User.objects.get(username='admin')
            self.stdout.write(self.style.WARNING('! Usuario admin ya existe'))

        # Crear Organizador
        if not User.objects.filter(username='organizador').exists():
            org_user = User.objects.create_user(
                username='organizador',
                password='org123',
                email='organizador@eventos.com',
                first_name='María',
                last_name='Organizadora'
            )
            org_user.groups.add(organizer_group)
            org_user.save()
            self.stdout.write(self.style.SUCCESS('✓ Usuario Organizador creado'))
            self.stdout.write(f'  Username: organizador | Password: org123')
        else:
            org_user = User.objects.get(username='organizador')
            self.stdout.write(self.style.WARNING('! Usuario organizador ya existe'))

        # Crear Asistente
        if not User.objects.filter(username='asistente').exists():
            att_user = User.objects.create_user(
                username='asistente',
                password='asist123',
                email='asistente@eventos.com',
                first_name='Juan',
                last_name='Pérez'
            )
            att_user.groups.add(attendee_group)
            att_user.save()
            self.stdout.write(self.style.SUCCESS('✓ Usuario Asistente creado'))
            self.stdout.write(f'  Username: asistente | Password: asist123')
        else:
            att_user = User.objects.get(username='asistente')
            self.stdout.write(self.style.WARNING('! Usuario asistente ya existe'))

        # Crear eventos de ejemplo
        eventos_ejemplo = [
            {
                'title': 'Conferencia de Tecnología 2024',
                'description': 'La conferencia más importante sobre tecnología e innovación del año.',
                'event_type': 'conference',
                'date': datetime.now() + timedelta(days=30),
                'location': 'Centro de Convenciones Santiago',
                'is_private': False,
                'organizer': admin_user
            },
            {
                'title': 'Concierto de Rock en Vivo',
                'description': 'Una noche increíble con las mejores bandas de rock nacional.',
                'event_type': 'concert',
                'date': datetime.now() + timedelta(days=15),
                'location': 'Estadio Nacional',
                'is_private': False,
                'organizer': org_user
            },
            {
                'title': 'Seminario de Marketing Digital',
                'description': 'Aprende las últimas estrategias de marketing digital y redes sociales.',
                'event_type': 'seminar',
                'date': datetime.now() + timedelta(days=7),
                'location': 'Hotel Marriott - Sala Principal',
                'is_private': True,
                'organizer': org_user
            },
        ]

        self.stdout.write('\n' + '-'*60)
        self.stdout.write('Creando eventos de ejemplo...\n')

        for evento_data in eventos_ejemplo:
            if not Event.objects.filter(title=evento_data['title']).exists():
                event = Event.objects.create(**evento_data)
                self.stdout.write(self.style.SUCCESS(f'✓ Evento creado: {event.title}'))
            else:
                self.stdout.write(self.style.WARNING(f'! Evento ya existe: {evento_data["title"]}'))

        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('CONFIGURACIÓN COMPLETADA'))
        self.stdout.write('='*60)
        
        self.stdout.write('\n📋 CREDENCIALES DE ACCESO:\n')
        self.stdout.write('┌─────────────────┬──────────────┬──────────────┐')
        self.stdout.write('│ Rol             │ Usuario      │ Contraseña   │')
        self.stdout.write('├─────────────────┼──────────────┼──────────────┤')
        self.stdout.write('│ Administrador   │ admin        │ admin123     │')
        self.stdout.write('│ Organizador     │ organizador  │ org123       │')
        self.stdout.write('│ Asistente       │ asistente    │ asist123     │')
        self.stdout.write('└─────────────────┴──────────────┴──────────────┘\n')