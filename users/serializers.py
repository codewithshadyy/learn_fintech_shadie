
from rest_framework import serializers
from .models import User

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ['id','username', 'email', 'role', 'password']
        
    def validate_email(self,value):
        
        if User.objects.filter(email=value).exists():
            
            raise serializers.ValidationError(
                "Email exists "
            )
    def validate_username(self,value):
        if len(value) < 3:
            raise serializers.ValidationError(
                "The username is too short"
            ) 
            
    def validate_password(self,value):
        if len(value) < 8:
            raise serializers.ValidationError(
                "The passwordis too short"
            )  
    def validate_role(self, value):
        allowed_roles = ["admin", 'client']
        
        if value not in allowed_roles:
            raise serializers.ValidationError(
                "Role not found"
            )
                  
            
    def create(self, validated_data):
        
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            role =validated_data.get("role", "client")
            
        )   
        
        return user                
            
            
        
            
        
   

    def create(self, validated_data):
        username = validated_data["username"]
        email = validated_data["email"]
        role = validated_data.get("role")
        password = validated_data["password"]
        
        user  = User.objects.create_user(**validated_data)
        
        return user

