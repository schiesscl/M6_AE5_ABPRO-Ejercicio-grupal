from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from events.models import Event

def setup_groups():
    """
    Configurar grupos y permisos para los diferentes roles de la plataforma.
    
    Roles:
    - Administradores: Acceso completo a todos los eventos
    - Organizadores: Pueden crear y editar eventos, pero no eliminar
    - Asistentes: Solo pueden ver y registrarse a eventos
    """
    
    # Obtener el content type del modelo Event
    event_ct = ContentType.objects.get_for_model(Event)
    
    # Obtener los permisos por defecto de Django
    add_event = Permission.objects.get(codename='add_event', content_type=event_ct)
    change_event = Permission.objects.get(codename='change_event', content_type=event_ct)
    delete_event = Permission.objects.get(codename='delete_event', content_type=event_ct)
    view_event = Permission.objects.get(codename='view_event', content_type=event_ct)
    
    # Obtener los permisos personalizados
    manage_event = Permission.objects.get(codename='manage_event', content_type=event_ct)
    view_private = Permission.objects.get(codename='view_private_event', content_type=event_ct)
    
    # ========== GRUPO: ADMINISTRADORES ==========
    # Tienen acceso completo para crear, editar y eliminar eventos
    admin_group, created = Group.objects.get_or_create(name='Administradores')
    admin_group.permissions.set([
        add_event,      # Puede agregar eventos
        change_event,   # Puede modificar eventos
        delete_event,   # Puede eliminar eventos
        view_event,     # Puede ver eventos
        manage_event,   # Puede gestionar eventos
        view_private    # Puede ver eventos privados
    ])
    if created:
        print("✓ Grupo 'Administradores' creado")
    else:
        print("✓ Grupo 'Administradores' actualizado")
    
    # ========== GRUPO: ORGANIZADORES DE EVENTOS ==========
    # Pueden crear y gestionar eventos específicos, pero no pueden eliminarlos
    organizer_group, created = Group.objects.get_or_create(name='Organizadores')
    organizer_group.permissions.set([
        add_event,      # Puede agregar eventos
        change_event,   # Puede modificar eventos
        view_event,     # Puede ver eventos
        manage_event,   # Puede gestionar eventos
        view_private    # Puede ver eventos privados
        # NO tiene delete_event
    ])
    if created:
        print("✓ Grupo 'Organizadores' creado")
    else:
        print("✓ Grupo 'Organizadores' actualizado")
    
    # ========== GRUPO: ASISTENTES ==========
    # Solo pueden ver los eventos a los que están registrados
    attendee_group, created = Group.objects.get_or_create(name='Asistentes')
    attendee_group.permissions.set([
        view_event,     # Solo puede ver eventos
        # NO puede agregar, modificar o eliminar eventos
    ])
    if created:
        print("✓ Grupo 'Asistentes' creado")
    else:
        print("✓ Grupo 'Asistentes' actualizado")
    
    print("\n" + "="*50)
    print("GRUPOS Y PERMISOS CONFIGURADOS CORRECTAMENTE")
    print("="*50)
    print("\nResumen de permisos por grupo:")
    print("\n1. Administradores:")
    print("   - Crear eventos ✓")
    print("   - Editar eventos ✓")
    print("   - Eliminar eventos ✓")
    print("   - Ver eventos privados ✓")
    print("\n2. Organizadores:")
    print("   - Crear eventos ✓")
    print("   - Editar eventos ✓")
    print("   - Eliminar eventos ✗")
    print("   - Ver eventos privados ✓")
    print("\n3. Asistentes:")
    print("   - Ver eventos ✓")
    print("   - Registrarse a eventos ✓")
    print("   - Crear/Editar/Eliminar eventos ✗")
    print("="*50 + "\n")