from rest_framework import serializers

from .models import Ticket, TicketComment


class TicketCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketComment
        fields = ["id", "ticket", "user", "comment", "created_time"]
        read_only_fields = ["id", "created_time"]


class TicketSerializer(serializers.ModelSerializer):
    comments = TicketCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Ticket
        fields = [
            "id",
            "title",
            "description",
            "status",
            "client",
            "agent",
            "assigned_to",
            "priority",
            "created_time",
            "modified_time",
            "comments",
        ]
        read_only_fields = ["id", "created_time", "modified_time"]


class TicketAuditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            "id",
            "title",
            "description",
            "status",
            "client_id",
            "agent_id",
            "assigned_to_id",
            "priority",
        ]


class TicketCommentAuditSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketComment
        fields = ["id", "ticket_id", "user_id", "comment"]
