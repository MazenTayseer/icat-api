from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.dal.models import Module
from apps.dashboard.rest.serializers.module import ModuleDashboardSerializer


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
