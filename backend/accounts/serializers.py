from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'phone', 'date_of_birth', 'gender', 'blood_group',
            'emergency_contact', 'medical_disclaimer_accepted', 'bio',
            'created_at', 'updated_at'
        ]

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'profile']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)
    medical_disclaimer_accepted = serializers.BooleanField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'first_name', 'last_name', 'medical_disclaimer_accepted']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        if not attrs.get('medical_disclaimer_accepted', False):
            raise serializers.ValidationError({
                "medical_disclaimer_accepted": "You must acknowledge that this application is for informational purposes only and does not provide formal medical diagnoses or prescriptions."
            })
        if User.objects.filter(email__iexact=attrs.get('email', '')).exists():
            raise serializers.ValidationError({"email": "A user with this email address already exists."})
        return attrs

    def create(self, validated_data):
        disclaimer_accepted = validated_data.pop('medical_disclaimer_accepted')
        validated_data.pop('confirm_password')
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        
        # UserProfile created by signal, update acceptance
        profile = user.profile
        profile.medical_disclaimer_accepted = disclaimer_accepted
        profile.save()

        return user

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Incorrect current password.")
        return value

