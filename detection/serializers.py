# detection/serializers.py
from rest_framework import serializers
from .models import HairScan, ProgressImage

class HairScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = HairScan
        fields = ["id", "image", "result", "confidence", "created_at"]
        read_only_fields = ["id", "result", "confidence", "created_at"]

class ProgressImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgressImage
        fields = ["id", "image"]
        read_only_fields = ["id"]