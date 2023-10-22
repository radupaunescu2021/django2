import django_filters
from django.utils import timezone

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics, status

from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import Event, Registration
from .permissions import IsEventCreator
from .serializers import UserSerializer, EventSerializer, RegistrationSerializer
from django.contrib.auth import get_user_model

class UserListCreateView(generics.ListCreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

##Filter events by type class
class EventFilter(django_filters.FilterSet):
    class Meta:
        model = Event
        fields = ['type']

class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]  # Require authentication for this view

    #FIltering by type
    filter_backends = (DjangoFilterBackend,)
    filterset_class = EventFilter
    def perform_create(self, serializer):
        # Set the created_by field to the currently authenticated user
        serializer.save(created_by=self.request.user)


#Show all events
class AllEventsListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    #Filtering by type
    filter_backends = (DjangoFilterBackend,)
    filterset_class = EventFilter

#Show only  events for a certain user
class UserCreatedEventsListView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    #Filtering by type
    filter_backends = (DjangoFilterBackend,)
    filterset_class = EventFilter
    def get_queryset(self):
        # Filter the queryset to include only events created by the currently authenticated user
        return Event.objects.filter(created_by=self.request.user)

class RegistrationListCreateView(generics.ListCreateAPIView):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [IsAuthenticated]

    #Check if event is in the future
    def create(self, request, *args, **kwargs):
        event_pk = kwargs.get('event_pk')  # Get the event_pk from the URL
        event = get_object_or_404(Event, pk=event_pk)  # Get the event object
        if event.start_date <= timezone.now():
            return Response({'error': 'Registration for past events is not allowed.'},
                            status=status.HTTP_400_BAD_REQUEST)
        registration, created = Registration.objects.get_or_create(user=request.user, event=event)
        if created:
            serializer = self.get_serializer(registration)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': 'Already registered.'}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        # Optionally filter registrations by the current user
        return Registration.objects.filter(user=self.request.user)

###Separate view for unregistering from event
class RegistrationDestroyView(generics.DestroyAPIView):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [IsAuthenticated]

    #Uneregister is available only for future events
    def get_object(self):
        event = get_object_or_404(Event, pk=self.kwargs.get('event_pk'))
        if event.start_date <= timezone.now():
            raise Response({'error': 'Unregistration from past events is not allowed.'}, status=status.HTTP_400_BAD_REQUEST)
        return get_object_or_404(Registration, user=self.request.user, event=event)


#Edit events created by a ceratin user
class EventUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsEventCreator]

    #field remains unchanged when the event is updated
    def perform_update(self, serializer):
        serializer.save(created_by=self.request.user)