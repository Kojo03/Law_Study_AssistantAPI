from rest_framework import serializers
from django.utils.html import escape
from .models import Case

class CaseSerializer(serializers.ModelSerializer):
    is_available = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Case
        fields = ["id", "topic", "title", "suit_number", "number_of_pages", 
                 "summary", "citation", "year", "total_copies", "available_copies", "is_available"]
        read_only_fields = ['available_copies']
    
    def validate(self, attrs):
        # Sanitize text fields
        for field in ['title', 'suit_number', 'summary', 'citation']:
            if field in attrs and attrs[field]:
                attrs[field] = escape(str(attrs[field]))
        return attrs
