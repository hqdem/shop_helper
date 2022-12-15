from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .serializers import UserSubscribeSerializer


class SubscribeToUserAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        serializer = UserSubscribeSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data['user']
            user = get_object_or_404(get_user_model(), pk=user_id)
            request_user = request.user
            if user == request_user:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            user.subscribers.add(request_user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UnSubscribeToUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        serializer = UserSubscribeSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data['user']
            user = get_object_or_404(get_user_model(), pk=user_id)
            request_user = request.user
            if user == request_user:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            user.subscribers.remove(request_user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
