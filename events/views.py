from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db import models
from .models import Event

class EventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    
    def get_queryset(self):
        user = self.request.user
        
        # Administradores y organizadores ven todos los eventos
        if user.groups.filter(name__in=['Administradores', 'Organizadores']).exists():
            return Event.objects.all()
        
        # Asistentes solo ven eventos públicos y eventos a los que asisten
        return Event.objects.filter(
            models.Q(is_private=False) | 
            models.Q(attendees=user)
        ).distinct()

class EventCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Event
    template_name = 'events/event_form.html'
    fields = ['title', 'description', 'event_type', 'date', 'location', 'is_private']
    permission_required = 'events.add_event'
    success_url = reverse_lazy('event_list')
    
    def form_valid(self, form):
        form.instance.organizer = self.request.user
        messages.success(self.request, 'Evento creado exitosamente.')
        return super().form_valid(form)
    
    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permisos para crear eventos.')
        return redirect('event_list')

class EventUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Event
    template_name = 'events/event_form.html'
    fields = ['title', 'description', 'event_type', 'date', 'location', 'is_private']
    permission_required = 'events.change_event'
    success_url = reverse_lazy('event_list')
    
    def dispatch(self, request, *args, **kwargs):
        event = self.get_object()
        user = request.user
        
        # Solo el organizador o administradores pueden editar
        if event.organizer != user and not user.groups.filter(name='Administradores').exists():
            messages.error(request, 'Solo el organizador o administradores pueden editar este evento.')
            return redirect('event_list')
        
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, 'Evento actualizado exitosamente.')
        return super().form_valid(form)
    
    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permisos para editar eventos.')
        return redirect('event_list')

class EventDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Event
    template_name = 'events/event_confirm_delete.html'
    permission_required = 'events.delete_event'
    success_url = reverse_lazy('event_list')
    
    def dispatch(self, request, *args, **kwargs):
        event = self.get_object()
        user = request.user
        
        # Solo administradores pueden eliminar
        if not user.groups.filter(name='Administradores').exists():
            messages.error(request, 'Solo los administradores pueden eliminar eventos.')
            return redirect('event_list')
        
        return super().dispatch(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Evento eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)
    
    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permisos para eliminar eventos.')
        return redirect('event_list')

@login_required
def register_attendance(request, pk):
    """Registrar asistencia a un evento"""
    event = get_object_or_404(Event, pk=pk)
    
    if event.is_private and not request.user.has_perm('events.view_private_event'):
        messages.error(request, 'Este evento es privado.')
        return redirect('event_list')
    
    event.attendees.add(request.user)
    messages.success(request, f'Te has registrado al evento: {event.title}')
    return redirect('event_list')

def access_denied(request):
    """Vista para acceso denegado"""
    return render(request, 'events/access_denied.html', status=403)
