from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.dal.models import Module
from apps.dashboard.rest.serializers.module import ModuleDashboardSerializer, ModuleCreateSerializer, ModuleUpdateSerializer


class ModuleDashboardView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None, *args, **kwargs):
        if id:
            try:
                module = Module.objects.get(id=id)
            except Module.DoesNotExist:
                return Response({"detail": "Module not found."}, status=status.HTTP_404_NOT_FOUND)
            serializer = ModuleDashboardSerializer(module)
            return Response(serializer.data)

        modules = Module.objects.all()
        serializer = ModuleDashboardSerializer(modules, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = ModuleCreateSerializer(data=request.data)
        if serializer.is_valid():
            module = serializer.save()
            response_serializer = ModuleDashboardSerializer(module)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id, *args, **kwargs):
        try:
            module = Module.objects.get(id=id)
        except Module.DoesNotExist:
            return Response({"detail": "Module not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ModuleUpdateSerializer(module, data=request.data)
        if serializer.is_valid():
            module = serializer.save()
            response_serializer = ModuleDashboardSerializer(module)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id, *args, **kwargs):
        try:
            module = Module.objects.get(id=id)
        except Module.DoesNotExist:
            return Response({"detail": "Module not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ModuleUpdateSerializer(module, data=request.data, partial=True)
        if serializer.is_valid():
            module = serializer.save()
            response_serializer = ModuleDashboardSerializer(module)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, *args, **kwargs):
        try:
            module = Module.objects.get(id=id)
        except Module.DoesNotExist:
            return Response({"detail": "Module not found."}, status=status.HTTP_404_NOT_FOUND)

        module.delete()
        return Response({"detail": "Module deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
