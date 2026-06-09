from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ['id','username', 'email', 'role', "phone", 'password',]
        
    def validate_email(self,value):
        
        if User.objects.filter(email=value).exists():
            
            raise serializers.ValidationError(
                "Email exists "
            )
            
        return value    
    def validate_username(self,value):
        if len(value) < 3:
            raise serializers.ValidationError(
                "The username is too short"
            ) 
        return value    
            
    def validate_password(self,value):
        if len(value) < 8:
            raise serializers.ValidationError(
                "The passwordis too short"
            ) 
        return value     
    def validate_role(self, value):
        allowed_roles = ["admin", 'client']
        
        if value not in allowed_roles:
            raise serializers.ValidationError(
                "Role not found"
            )
        return value    
                  
    def create(self, validated_data): 
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            phone=validated_data["phone"],
            role=validated_data.get('role', 'client'),
            password=validated_data['password']
        )

        return user
             


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password  = serializers.CharField()
    
    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        
        
        user = authenticate(username=email, password=password)
        
        if not user:
           raise serializers.ValidationError("Invalid credentials")
       
        attrs["user"] = user
        return user
           

            

            
                            
                
            
        
            
        
   

    

