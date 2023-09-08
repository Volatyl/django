from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = fields = ["email", "password", "first_name", "last_name"]
            extra_kwargs = {"password": {"write_only": True}}

        def validate_password(self, value):
            validate_password(value)
            return value

        def create(self, validated_data):
            user = User(**validated_data)
            user.set_password(validated_data["password"])
            user.save()
            return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = authenticate(username=email, password=password)

        if user is None:
            if not User.objects.filter(email=email).exists():
                raise ValidationError('This email does not exist.')

            raise ValidationError('Incorrect password.')

        if not user.is_active:
            raise ValidationError('This user account is not active.')

        data['user'] = user
        return data
