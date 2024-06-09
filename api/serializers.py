from rest_framework import serializers
from django.contrib.auth.models import User
from .models import FriendRequest

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','password']
        extra_kwargs = {'password':{'write_only':True}}
        
    def create(self,validate_data):
        user = User(
            email = validate_data['email'],
            username=validate_data['username']
        )
        user.set_password(validate_data['password'])
        user.save()
        return user
    
class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = UserSerializer(read_only=True)
    to_user = UserSerializer(read_only=True)

    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'is_accepted', 'created_at']
        