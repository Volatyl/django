from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        password = validated_data.pop("password")
        email = validated_data.pop("email")
        user = User.objects.create_user(
            email=email, password=password, **validated_data
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
      
        email = data.get('email')
        password = data.get('password')

        user = User.objects.filter(email=email).first()
        
        if user is None:
                raise ValidationError('This email does not exist.')
            
        if not user.check_password(password):
            raise ValidationError('Wrong password')

        if not user.is_active:
            raise ValidationError("This user account is not active.")

        data["user"] = user
        
        return data
