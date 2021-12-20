from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializer import UserSerializer
from rest_framework.decorators import action

# Create your views here.


class UserView(viewsets.ViewSet):

    @action(methods=['POST'], detail=True)
    def signup(self, request):
        data = request.data.dict()
        if User.objects.filter(username=data['username']).exists():
            return Response({'message': 'Username Already Exist', 'status': status.HTTP_200_OK})
        user = User.objects.create(**data)
        user.set_password(raw_password=data['password'])
        user.save()
        try:
            return Response({'message': 'User Created Successfully', 'status': status.HTTP_201_CREATED})
        except Exception as error:
            return Response({'error': str(error), 'status': status.HTTP_400_BAD_REQUEST})

    @action(methods=['POST'], detail=True)
    def login(self, request):
        username = request.data['username']
        password = request.data['password']

        user = authenticate(username=username, password=password)

        if user:
            user_obj = User.objects.get(username=username)
            token = Token.objects.create(user=user_obj)

            return Response({'token': token.key, 'status': status.HTTP_200_OK})
        else:
            return Response({'message': 'User does not exist', 'status': status.HTTP_401_UNAUTHORIZED})
