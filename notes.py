#views.py
'''

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from django.contrib.auth.models import User


from django.http import Http404

from rest_framework import viewsets, permissions, status

from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from core.models import Snippet
from core.serializers import UserSerializer, SnippetSerializer
from core.permissions import IsOwnerOrReadOnly

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@csrf_exempt
def snippet_get_post(request):
    if request.method == 'GET':
        data = Snippet.objects.all()
        serializer = SnippetSerializer(data, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def snippet_detail(request, pk):

    try:
        detail = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)
    
    if request.method == 'GET':
        serializer = SnippetSerializer(detail)
        return JsonResponse(serializer.data)
    
    elif request.method == 'PUT':
        snippet = JSONParser().parse(request)
        serializer = SnippetSerializer(detail, data=snippet)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    
    elif request.method == 'DELETE':
        detail.delete()
        return HttpResponse(status=204)

@api_view(['GET', 'POST'])
def snippet_listview(request):
    snippets = Snippet.objects.all()
    if request.method == 'GET':
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detailview(request, pk):
    try:
        detail = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SnippetSerializer(detail)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        serializer = SnippetSerializer(detail, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        detail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
'''

#urls.py
'''
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('snippets/', views.snippet_get_post),
    path('snippet_detail/<int:pk>/', views.snippet_detail),
    path('snippets_view/', views.snippet_listview),
    path('snippet_detailview/<int:pk>/', views.snippet_detailview),
]
'''
