from blog.models import Post
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'text', 'created_date', 'published_date', 'image')
    
    def create(self, validated_data):
        request = self.context.get('request')
        auth_header = request.headers.get('Authorization')
        
        if auth_header and auth_header.startswith('JWT '):
            token_key = auth_header.split(' ')[1]
            user = get_user_from_token(token_key)
            if not user:
                raise AuthenticationFailed('Invalid or expired token.')
        else:
            raise AuthenticationFailed('No token provided or incorrect token format.')
        
        validated_data['author'] = user
        return super().create(validated_data)
    
    def validate(self, data):
        if 'image' not in data or not data['image']:
            data['image'] = 'default.png'
        return data

def get_user_from_token(token_key):
    try:
        token = Token.objects.get(key=token_key)
        user = token.user
        return user
    except Token.DoesNotExist:
        return None