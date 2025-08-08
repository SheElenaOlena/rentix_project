from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'listing', 'author', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'author', 'created_at']


