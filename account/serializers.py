from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password              = serializers.CharField(min_length=6, required=True)
    password_confirmation = serializers.CharField(min_length=6, required=True)


    class Meta:
        model    = User
        fields   = (
            'password', 'password_confirmation',
            'username', 'email', 'name' 
        )

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('This username is already exists!')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('This email is already exists!')
        return value

    def validate(self, attrs):
        password         = attrs.get('password')
        password_confirm = attrs.pop('password_confirmation')
        if password      != password_confirm:
            raise serializers.ValidationError('Your password did not match!')
        return attrs

    def save(self, **kwargs):
        username = self.validated_data.get('username')
        email    = self.validated_data.get('email')
        password = self.validated_data.get('password')
        name     = self.validated_data.get('name')
        user     = User.objects.create_user(username, email,
                                            password, name=name)
        return user


class LoginSerializer(serializers.Serializer):
    username    = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username    = attrs.get('username')
        password = attrs.get('password')
        print(username)
        print(password)

        if username and password:
            user = authenticate(
                request=self.context.get('request'),
                username=username, password=password
            )
            print(user)
            if not user:
                raise serializers.ValidationError(
                    "Impossible to enter!",
                    code='authorization'
                )
        else:
            raise serializers.ValidationError(
                'You need to enter "Username" or "password"'
            )
        attrs['user'] = user
        return attrs

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ('username', 'email', 'name')
