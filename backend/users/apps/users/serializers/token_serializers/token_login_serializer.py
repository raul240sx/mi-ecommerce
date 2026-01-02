from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class TokenLoginSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['name'] = user.first_name
        token['last_name'] = user.last_name
        token['email'] = user.email
        token['is_verified'] = user.is_verified

        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)

        data['is_verified'] = self.user.is_verified

        return data