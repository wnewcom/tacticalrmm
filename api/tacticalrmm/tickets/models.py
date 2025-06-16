from django.db import models

from clients.models import Client
from agents.models import Agent
from accounts.models import User
from logs.models import BaseAuditModel
from tacticalrmm.models import PermissionQuerySet


class TicketStatus(models.TextChoices):
    OPEN = "open", "Open"
    IN_PROGRESS = "in_progress", "In Progress"
    RESOLVED = "resolved", "Resolved"
    CLOSED = "closed", "Closed"


class Ticket(BaseAuditModel):
    objects = PermissionQuerySet.as_manager()

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, choices=TicketStatus.choices, default=TicketStatus.OPEN
    )
    client = models.ForeignKey(Client, related_name="tickets", on_delete=models.CASCADE)
    agent = models.ForeignKey(
        Agent, related_name="tickets", null=True, blank=True, on_delete=models.SET_NULL
    )
    assigned_to = models.ForeignKey(
        User, related_name="tickets", null=True, blank=True, on_delete=models.SET_NULL
    )
    priority = models.CharField(max_length=50, default="normal")

    def __str__(self) -> str:
        return self.title

    @staticmethod
    def serialize(ticket: "Ticket"):
        from .serializers import TicketAuditSerializer

        return TicketAuditSerializer(ticket).data


class TicketComment(BaseAuditModel):
    ticket = models.ForeignKey(
        Ticket, related_name="comments", on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    comment = models.TextField()

    def __str__(self) -> str:
        return f"Comment on {self.ticket_id}"

    @staticmethod
    def serialize(comment: "TicketComment"):
        from .serializers import TicketCommentSerializer

        return TicketCommentSerializer(comment).data
