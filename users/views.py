from django.shortcuts import render

# Create your views here.
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from . serializers import UserLoginSerializer, UserDetailSerializer
from rest_framework import status
from datetime import timezone, timedelta, datetime
import jwt, json, string, random
from . models import User, UserToken
from django.contrib.auth.hashers import check_password
from directorydrive.settings import SECRET_KEY


class UserLoginView(GenericAPIView):
    
    serializer_class = UserLoginSerializer
    
    def post(self, request):
        
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(data={'message': "Something went wrong", 'errors':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = User.objects.filter(email=email).exists()

        if not user:
            return Response(data={'message': "User with email doesnot exists"}, status=status.HTTP_404_NOT_FOUND)

        user = User.objects.get(email=email)
        verify_password = check_password(password, user.password)

        if not verify_password:
            return Response(data={'message':"Password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

        # token generation:
        dt = datetime.now(tz=timezone.utc) + timedelta(days=100)
        letters = string.ascii_letters
        random_string = ''.join(random.choice(letters) for i in range(15))
        payload = {
            'exp': dt,
            'id': user.id,
            'email': user.email,
            'random_string': random_string            
        }

        if UserToken.objects.filter(user=user).exists():
            UserToken.objects.filter(user=user).delete()

        encoded_token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        UserToken.objects.create(user=user, token=encoded_token)

        serializer = UserDetailSerializer(user)

        return Response(
            data={
                'status':status.HTTP_200_OK,
                'detail':"User successfully login",
                'data':{
                    'token': encoded_token,
                    'user_data': serializer.data
                }
            }
        )
    

class UserRegisterView(GenericAPIView):

    def post(self, request):
        pass