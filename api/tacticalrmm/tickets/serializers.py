from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Ticket, Category, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'color', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'created_at', 'is_internal']

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class TicketSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    assigned_to = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    assigned_to_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Ticket
        fields = [
            'id', 'title', 'description', 'priority', 'status', 'category', 'category_id',
            'created_by', 'assigned_to', 'assigned_to_id', 'created_at', 'updated_at',
            'due_date', 'is_overdue', 'comments'
        ]

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class TicketListSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    assigned_to = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = [
            'id', 'title', 'priority', 'status', 'category', 'created_by',
            'assigned_to', 'created_at', 'updated_at', 'due_date', 'is_overdue',
            'comments_count'
        ]

    def get_comments_count(self, obj):
        return obj.comments.count()