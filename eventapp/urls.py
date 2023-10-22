from django.urls import path
from .views import UserListCreateView, EventListCreateView, RegistrationListCreateView, AllEventsListView, \
    UserCreatedEventsListView, EventUpdateDestroyView, RegistrationDestroyView

urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('events/', EventListCreateView.as_view(), name='event-list-create'),
    path('events/all/', AllEventsListView.as_view(), name='all-events-list'),
    path('events/user/', UserCreatedEventsListView.as_view(), name='user-created-events-list'),
    path('events/<int:pk>/', EventUpdateDestroyView.as_view(), name='event-update-destroy'),
    path('events/<int:event_pk>/register/', RegistrationListCreateView.as_view(), name='event-registration'),
    path('events/<int:event_pk>/unregister/', RegistrationDestroyView.as_view(), name='event-unregistration'),

]
