from rest_framework import serializers
from .models import User, ShortenedURL

class UserRegistrationSerializer(serializers.ModelSerializer):
    
    confirm_password = serializers.CharField(write_only= True)
    
    class Meta:
        model = User
        fields = ['first_name','last_name','email','password','confirm_password']
        extra_kwargs = {
            'password':{'write_only':True}
        }
    
        
    def validate(self, data):
        if data['password'] != data['confirm_psasword']:
            raise serializers.ValidationError('Passwords do not match')
        return data
    
    
    def create(self, validated_data):
        user = User.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only = True)


class ShortenedURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortenedURL
        fields = ['id','user','original_url', 'shortened_code', 'visits_count', 'qr_code']
        

class ShortenedURLEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortenedURL
        fields = ['original_url']