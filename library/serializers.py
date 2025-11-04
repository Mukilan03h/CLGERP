from rest_framework import serializers
from .models import Book, BookIssue, Fine

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class BookIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookIssue
        fields = '__all__'

class FineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fine
        fields = '__all__'
