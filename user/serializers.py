from django.contrib.auth import get_user_model
from rest_framework import serializers
import re

User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration with all required validations.
    All errors return as {"message": "..."}.
    """
    full_name = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'full_name', 'password', 'confirm_password')

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, value):
            raise serializers.ValidationError("Enter a valid email address.")
        return value

    def validate_password(self, value):
        errors = []
        if len(value) < 8:
            errors.append("Password must be at least 8 characters long.")
        if not re.search(r'\d', value):
            errors.append("Password must contain at least one digit.")
        if not re.search(r'[A-Z]', value):
            errors.append("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', value):
            errors.append("Password must contain at least one lowercase letter.")
        if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', value):
            errors.append("Password must contain at least one special character.")

        if errors:
            raise serializers.ValidationError(" ".join(errors))
        return value

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        user = User.objects.create_user(
            full_name=validated_data['full_name'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    email = serializers.EmailField(required=False)
    full_name = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['email', 'full_name', 'password', 'hair_type', 'shampoo_routine']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def update(self, instance, validated_data):
        # unique email
        if 'email' in validated_data and User.objects.filter(email=validated_data['email']).exclude(pk=instance.pk).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})

        # unique full_name
        if 'full_name' in validated_data and User.objects.filter(full_name=validated_data['full_name']).exclude(pk=instance.pk).exists():
            raise serializers.ValidationError({"full_name": "This full_name is already in use."})

        for attr, value in validated_data.items():
            if attr == "password":
                instance.set_password(value)
            else:
                setattr(instance, attr, value)

        instance.save()
        return instance

    
class UserPhotoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['photo']
        
    def validate_photo(self, value):
        # 5 MB limit
        max_size = 5 * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError("Photo size should not exceed 5MB.")
        return value