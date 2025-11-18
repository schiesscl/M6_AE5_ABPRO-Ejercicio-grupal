from django import template

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    """
    Verifica si un usuario pertenece a un grupo específico.
    
    Uso en template: {% if user|has_group:"Administradores" %}
    """
    return user.groups.filter(name=group_name).exists()

@register.filter(name='is_event_organizer')
def is_event_organizer(user, event):
    """
    Verifica si el usuario es el organizador del evento.
    
    Uso en template: {% if user|is_event_organizer:event %}
    """
    return event.organizer == user

@register.filter(name='can_edit_event')
def can_edit_event(user, event):
    """
    Verifica si el usuario puede editar el evento.
    
    Uso en template: {% if user|can_edit_event:event %}
    """
    return (event.organizer == user or 
            user.groups.filter(name='Administradores').exists())

@register.filter(name='can_delete_event')
def can_delete_event(user, event):
    """
    Verifica si el usuario puede eliminar el evento.
    
    Uso en template: {% if user|can_delete_event:event %}
    """
    return user.groups.filter(name='Administradores').exists()