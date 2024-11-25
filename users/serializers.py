from .models import CustomUser
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True)

	class Meta:
		model = CustomUser
		fields =['username','password','nickname','name','birthday','gender','email','phone_number','address','profile_image','bio','created_at','updated_at']

	def create(self, validated_data):
		password = validated_data.pop('password')
		user = CustomUser.objects.create(**validated_data)
		user.set_password(password) #패스워드 해싱처리
		user.save()
		return user
	

class UserprofileSerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomUser
		fields = ['nickname','name','birthday','gender','email','profile_image','bio']


