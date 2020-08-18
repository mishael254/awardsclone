from rest_framework import serializers
from .models import Profile,Projects

'''
Serializer classes for profile and projects [API]
Feature E: API endpoints
'''

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('user','profile_photo','bio') 
        
        
class ProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ('title','image_posted','description','link')