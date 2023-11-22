from rest_framework import serializers
from apps.notes.models import NoteManagement


class CreateOrUpdateAboutUsSerializer(serializers.ModelSerializer):
    
    instance    = serializers.PrimaryKeyRelatedField(required=False, queryset=NoteManagement.objects.all(), default=None)
    title       = serializers.CharField(required=True)
    body        = serializers.CharField(required=True)
    
    class Meta:
        model  = NoteManagement
        fields = ['instance', 'title', 'body']
    
    def create(self, validated_data):
        instance = NoteManagement()
        
        instance.title       = validated_data.get('title')
        instance.body        = validated_data.get('body')
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.title       = validated_data.get('title')
        instance.body        = validated_data.get('body')
        instance.save()
        return instance
    

class DestroyNotesSerializer(serializers.ModelSerializer):
    instance_id   = serializers.ListField(child=serializers.IntegerField(required=True))
    
    class Meta:
        model  = NoteManagement
        fields = ['instance_id']
