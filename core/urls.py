from django.urls import path, include

#from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('register/', views.RegisterView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),

    path('users/', views.UserList.as_view()),
    path('user/<int:pk>/', views.UserDetail.as_view()),
    path('user/auth/', views.UserAuth.as_view()),

    path('lists/', views.SnippetList.as_view(), name='snippets'),
    path('detail/<int:pk>/', views.SnippetDetail.as_view()),
]

#urlpatterns = format_suffix_patterns(urlpatterns)