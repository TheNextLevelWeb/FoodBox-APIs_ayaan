from rest_framework import serializers
from users.models import users

class UserSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    billing_address = serializers.CharField(required=False)
    order_history = serializers.JSONField(required=False)
    favourite_list = serializers.JSONField(required=False)
    feedback = serializers.CharField(required=False)

    class Meta:
        model = users
        fields = '__all__'

    def validate_email(self, value):
        if users.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "A user with this email already exists.")
        return value

    def validate_username(self, value):
        if users.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "A user with this username already exists.")
        return value


class LoginSerializer(serializers.ModelSerializer):

    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = users
        fields = ['username', 'password']

    

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise serializers.ValidationError(
                "Both username and password are required.")

        return data


class ChangePasswordSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    old_password = serializers.CharField()
    new_password = serializers.CharField()

    class Meta:
        model = users
        fields = '__all__'


class ForgotPasswordSerializer(serializers.Serializer):
    username = serializers.CharField()
    new_password = serializers.CharField()

    class Meta:
        model = users
        fields = '__all__'


class FOBSerializer(serializers.ModelSerializer):
    class Meta:
        model = users
        fields = [ 'billing_address', 'favourite_list', 'order_history']