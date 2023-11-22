from rest_framework import serializers
from apps.notes.models import NoteManagement

class GetNotesResponseSchemas(serializers.ModelSerializer):

    class Meta:
        model = NoteManagement
        fields = ['id', 'title', 'body']
        