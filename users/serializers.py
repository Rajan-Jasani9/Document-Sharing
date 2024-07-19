from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import User
class UserLoginSerializer(ModelSerializer):
    
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    
    class Meta:
        model = User
        fields = ['email', 'password']
        

class InputUserSerializer(ModelSerializer):
    
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    date_of_birth = serializers.DateField(required=True)

    class Meta:
        model = User
        fields =['id', 'first_name', 'last_name', 'email', 'password']
        
        
class UserDetailSerializer(ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'date_of_birth']
        


    