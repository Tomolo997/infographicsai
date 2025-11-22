from infographs.models import Infograph, Template
from infographs.serializers import InfographSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.

class InfographListAPIView(generics.ListAPIView):
    queryset = Infograph.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request):
        infographs = self.get_queryset()
        serializer = InfographSerializer(infographs, many=True)
        return Response(serializer.data)

class InfographCreateAPIView(generics.CreateAPIView):
    queryset = Infograph.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = InfographSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(serializer.data)
        return Response(serializer.data)