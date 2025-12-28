# detection/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from hairfall_detection.permission import LoginRequiredPermission
from .models import HairScan, ProgressImage
from .serializers import HairScanSerializer, ProgressImageSerializer
from .utils import predict_hair_condition
from .gemini_hair_analysis import analyze_hair_loss

class HairScanAPIView(APIView):
    permission_classes = [LoginRequiredPermission]

    def post(self, request):
        # Only accept images
        if "image" not in request.FILES:
            return Response(
                {"message": "No image provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Initialize serializer with the uploaded image
        serializer = HairScanSerializer(data=request.FILES)
        serializer.is_valid(raise_exception=True)

        # Save the scan with the logged-in user
        scan = serializer.save(user=request.user)

        try:
            # Predict hair condition using AI model
            prediction = predict_hair_condition(scan.image.path)

            # Save prediction results to DB
            scan.result = prediction["predicted_class"]
            scan.confidence = round(prediction["confidence"] * 100, 2)
            scan.save()

            # Return response with scan info
            return Response(
                {
                    "message": "Hair scan completed!",
                    "data": {
                        "scan_id": str(scan.id),
                        "condition": scan.result,
                        "confidence_percent": scan.confidence,
                        "image_url": scan.image.url,
                    },
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            # Rollback if AI prediction fails
            scan.delete()
            return Response(
                {"message": f"AI prediction error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class ProgressAPIView(APIView):
    permission_classes = [LoginRequiredPermission]

    def get(self, request):
        # Get all scans for the user, most recent first
        scans = HairScan.objects.filter(user=request.user).order_by('-created_at')

        if not scans.exists():
            return Response(
                {
                    "message": "First time scan – no progress image available.",
                    "last_scan_image": None,
                    "recent_scan_image": None,
                },
                status=status.HTTP_200_OK,
            )

        # Last scan (oldest)
        last_scan = scans.last()
        # Most recent scan
        recent_scan = scans.first()

        return Response(
            {
                "last_scan_image": last_scan.image.url if last_scan else None,
                "recent_scan_image": recent_scan.image.url if recent_scan else None,
            },
            status=status.HTTP_200_OK,
        )
    
class ProgressDailyHairScanAPIView(APIView):
    permission_classes = [LoginRequiredPermission]

    def get(self, request):
        # Get all scans for the user, most recent first
        scans = ProgressImage.objects.filter(user=request.user).order_by('-created_at')

        serializer = ProgressImageSerializer(scans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DailyHairScanApiView(APIView):
    permission_classes = [LoginRequiredPermission]

    def post(self, request):
        # Only accept images
        if "image" not in request.FILES:
            return Response(
                {"message": "No image provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Initialize serializer with the uploaded image
        serializer = ProgressImageSerializer(data=request.FILES)
        serializer.is_valid(raise_exception=True)

        # Save the progress image with the logged-in user
        progress_image = serializer.save(user=request.user)

        return Response(
            {
                "progress_image_id": str(progress_image.id),
                "image_url": progress_image.image.url,
            },
            status=status.HTTP_200_OK,
        )


class HairAnalysisView(APIView):
    permission_classes = [LoginRequiredPermission]

    def post(self, request):
        symptoms = request.data.get("symptoms", [])
        
        if not symptoms or len(symptoms) == 0:
            return Response({"error": "Please select at least one symptom"}, status=400)

        try:
            analysis = analyze_hair_loss(symptoms)
            return Response({
               **analysis,
            }, status=200)
            
        except Exception as e:
            return Response({
                "error": "AI trichologist is having coffee. Try again in 5 seconds!",
                "details": str(e)
            }, status=500)