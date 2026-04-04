from rest_framework import serializers
from .models import Candidate

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'  # Yêu cầu DRF chuyển toàn bộ cột trong Bảng Candidate thành JSON gửi về Client
        