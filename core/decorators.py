from rest_framework import status
from rest_framework.response import Response

from .models import Snippet


def un_authenticated(func):
    def wrapper(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return Response({"response": "This user is already authenticated."},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            return func(self, *args, **kwargs)
    return wrapper


def authenticated(func):
    def wrappper(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return func(self, *args, **kwargs)
        else:
            return Response({'response': 'user must login first'}, status=status.HTTP_403_FORBIDDEN)
    return wrappper


def authorisation(func):
    def wrapper(self, *args, **kwargs):
        snippet_pk = kwargs.get('pk')
        snippet = Snippet.objects.get(pk=snippet_pk)

        if self.request.user == snippet.creator:
            return func(self, *args, **kwargs)
        else:
            return Response({'response': 'user not permitted to update or delete this post'},
                            status=status.HTTP_403_FORBIDDEN)
    return wrapper
