from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.contrib.auth.models import User
from django.db.models import Count, Q
from .models import Ticket, Category, Comment
from .serializers import (
    TicketSerializer, TicketListSerializer, CategorySerializer,
    CommentSerializer, UserSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.select_related('category', 'created_by', 'assigned_to').prefetch_related('comments')
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'priority', 'category', 'assigned_to']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at', 'priority', 'status']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return TicketListSerializer
        return TicketSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # Filter tickets based on user role
        if not user.is_staff:
            queryset = queryset.filter(Q(created_by=user) | Q(assigned_to=user))
        
        return queryset

    @action(detail=False, methods=['get'])
    def dashboard_stats(self, request):
        user = request.user
        
        if user.is_staff:
            tickets = Ticket.objects.all()
        else:
            tickets = Ticket.objects.filter(Q(created_by=user) | Q(assigned_to=user))
        
        stats = {
            'total_tickets': tickets.count(),
            'open_tickets': tickets.filter(status='open').count(),
            'in_progress_tickets': tickets.filter(status='in_progress').count(),
            'resolved_tickets': tickets.filter(status='resolved').count(),
            'my_tickets': tickets.filter(created_by=user).count(),
            'assigned_to_me': tickets.filter(assigned_to=user).count(),
            'high_priority': tickets.filter(priority='high').count(),
            'urgent_priority': tickets.filter(priority='urgent').count(),
        }
        
        return Response(stats)

    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        ticket = self.get_object()
        serializer = CommentSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save(ticket=ticket)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return User.objects.filter(is_active=True)