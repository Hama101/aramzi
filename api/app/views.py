from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import *

from knox.models import AuthToken
from django.contrib.auth import login

from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView

from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework import generics, permissions

@api_view(['GET'])
def apiOverview(request):
    apiOverView = {
    '***users***':'***users***',
    'api/signup/':'signup',
    'api/addprofil/' :'addprofil',
    'api/view_profil/<str:pk>/': 'view_porfil',
    'api/login/': 'login',
    'api/logout/' :'logout',
    'api/logoutall/': 'logoutall',
    'api/user/':'user',
    '***posts***':'***posts***',
    'api/addpost/' :'addpost',
    'api/shop/' :'shop',
    'api/view_post/<str:pk>/':'postDetail',
    'api/update_post/<str:pk>/': 'postUpdate',
    'api/delete_post/<str:pk>/':'postDelete'
    }
    return Response(apiOverView)


#classes
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

    def get_post_response_data(self, request, token, instance):
        UserSerializer = self.get_user_serializer_class()

        data = {
            'expiry': self.format_expiry_datetime(instance.expiry),
            'token': token
        }
        if UserSerializer is not None:
            data["user"] = UserSerializer(
                request.user,
                context=self.get_context()
            ).data
        return data



class UserAPI(generics.RetrieveAPIView):
    permission_classes = [
    permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

# Create your views here.
def home(request):
    return render(request,'home.html')

@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = 'successfully registered new user.'
            data['id']= user.id
            data['email'] = user.email
            data['username'] = user.username
        else:
            data = serializer.errors
            return Response(data)

        user = User.objects.get(username=data['username'])
        data["token"] = AuthToken.objects.create(user)[1]
        return Response(data)

@api_view(['POST'])
def addprofil(request):
    if request.method == 'POST':
        serializer = ProfilSerializer(data=request.data)
        data = {}
        print("validating")
        if serializer.is_valid():
            print("validated")
            profil = serializer.save()
            data['response'] = 'successfully registered new profil.'
            print(profil.user)
            data['user'] = profil.user.username
            data['is_chef'] = profil.is_chef
        else:
            data = serializer.errors
        return Response(data)


@api_view(['GET'])
def view_profil(request , pk):
    data= {}
    user = None
    profil = None
    try:
        user = User.objects.get(username = pk)
        profil = Profil.objects.get(user = user)
        serializer = ProfilSerializer(profil , many=False)
        data['response'] = 'successfully found profil.'
        data['id']=profil.id
        data['user'] = profil.user.username
        data['is_chef'] = profil.is_chef
        return Response(data)

    except :
        if not user:
            raise serializers.ValidationError({'user': 'user does not exist.'})
        else:
            raise serializers.ValidationError({'profil': 'profil does not exist.'})

@api_view(['POST'])
def addPost(request):
    if request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            post = serializer.save()
            data['response'] = 'successfully registered new Post.'
            data['id'] = post.id
            data['title'] = post.title
            data['user'] = post.user.username
            data['description'] = post.description
            data['price'] = post.price
        else:
            data = serializer.errors
        return Response(data)


@api_view(['GET'])
def shop(request):
    posts = Post.objects.all().order_by('-id')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def postDetail(request, pk):
	post = Post.objects.get(id=pk)
	serializer = PostSerializer(post, many=False)
	return Response(serializer.data)

@api_view(['POST'])
def postUpdate(request, pk):
	post = Post.objects.get(id=pk)
	serializer = PostSerializer(instance=post, data=request.data)

	if serializer.is_valid():
		serializer.update(instance=post, validated_data=request.data)

	return Response(serializer.data)


@api_view(['DELETE'])
def postDelete(request, pk):
	post = Post.objects.get(id=pk)
	post.delete()

	return Response('Item succsesfully delete!')


