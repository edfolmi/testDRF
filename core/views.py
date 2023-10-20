from django.contrib.auth.models import User
from django.http import Http404
from django.contrib.auth import authenticate, login, logout

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token

from .models import Snippet
from .serializers import RegisterSerializer, UserSerializer, SnippetSerializer
from .permissions import IsOwnerOrReadOnly
from .decorators import un_authenticated, authenticated, authorisation
# Create your views here.


class RegisterView(APIView):
    @un_authenticated
    def get(self, request, *args, **kwargs):
        return Response({"response": "register your account!"})

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if request.user.is_authenticated:
            return Response({"response": "This user is already authenticated."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if serializer.is_valid():
                user = User.objects.create_user(
                    username=serializer.validated_data['username'],
                    email=serializer.validated_data['email'],
                    password=serializer.validated_data['password']
                )
                user.save()

                return Response({'response': 'user created succesfully'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    @un_authenticated
    def get(self, request, *args, **kwargs):
        return Response({"response": "login your account!"})

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if request.user.is_authenticated:
            return Response({"response": "This user is already authenticated."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user = authenticate(username=username, password=password)
            if user is not None:
                token, _ = Token.objects.get_or_create(user=user)
                login(request, user)
                return Response({"token": token.key, "user": token.user_id}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'user': 'logout succesfully!'})


class UserList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        snippets = User.objects.all()
        serializer = UserSerializer(snippets, context={'request': request}, many=True)
        return Response(serializer.data)


class UserAuth(APIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        content = {
            'user': str(request.user),
            'auth': str(request.auth)
        }
        return Response(content)

    def post(self, request):
        try:
            create = Token.objects.get_or_create(user=request.user)
            print(create)
            return Response({'auth_token': 'create token successfully'})
        except Exception as e:
            return Response({'error': f'error creating: {e}'})


class UserDetail(APIView):
    def get_user(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        detail = self.get_user(pk)
        serializer = UserSerializer(detail, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class SnippetList(APIView):

    def get(self, request):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @authenticated
    def post(self, request):
        serializer = SnippetSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(creator=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SnippetDetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_detail(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        detail = self.get_detail(pk)
        serializer = SnippetSerializer(detail)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @authorisation
    def put(self, request, pk):
        detail = self.get_detail(pk)
        serializer = SnippetSerializer(detail, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @authorisation
    def delete(self, request, pk):
        detail = self.get_detail(pk)
        detail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
