from rest_framework import serializers
from apps.listings.choices.roles import Role
from apps.users.models import User


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)


    class Meta:
        model = User
        fields = ( 'email', 'password')


    def create(self, validated_data):
        email = validated_data['email']
        validated_data['username'] = email.split('@')[0]
        validated_data['role'] = Role.TENANT
        password = validated_data.pop('password')

        return  User.objects.create_user(password=password, **validated_data)
        # return super().create(validated_data)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
            'is_active',
            'date_joined'
        ]
        read_only_fields = ['id', 'date_joined']