from rest_framework import serializers

from apps.users.models.user import User



class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)

    def validate(self, attrs):
        attrs['email'] = attrs['email'].strip().lower()
        user = User.objects.filter(email=attrs['email']).first()

        if user:
            if not user.is_active or not user.is_verified:
                user = None

        self.user = user
        return attrs
        

    def save(self):
        user = getattr(self, 'user')

        if not user:
            return None
        
        return user.id
    
