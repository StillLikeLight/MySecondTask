from rest_framework.permissions import IsAuthenticated
from .models import CompanyInfoModel
from .serializers import CompanyInfoSerializer
from rest_framework.viewsets import ModelViewSet


class InfoViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = CompanyInfoModel.objects.all()
    serializer_class = CompanyInfoSerializer
