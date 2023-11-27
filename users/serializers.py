from django.contrib.auth.models import User 
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'first_name', 'last_name')
        extra_kwargs = {"password": {"write_only":True}}

    def create(self, validated_data):
        user = User(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
        )
        password = validated_data.get('password')
        password2 = validated_data.get('password2')
        if password != password2:
            raise serializers.ValidationError({'password':"비밀번호가 일치하지 않습니다."})
        user.set_password(password)
        user.save()
        return user