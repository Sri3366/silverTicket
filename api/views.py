from rest_framework.decorators import api_view # type: ignore
from rest_framework.response import Response # type: ignore
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken # type: ignore
from .models import *
from .serializers import *
from .utils import *
from rest_framework.decorators import permission_classes # type: ignore
from rest_framework.permissions import IsAuthenticated,AllowAny   # type: ignore

# PUBLIC APIs

@api_view(['GET'])
def products(request):
    return Response(ProductSerializer(Product.objects.all(), many=True).data)


@api_view(['GET'])
def upi_info(request):
    upi = UPIInfo.objects.first()
    return Response(UPISerializer(upi).data)


@api_view(['POST'])
def submit_ticket(request):
    serializer = SubmissionSerializer(data=request.data)

    if serializer.is_valid():
        submission = serializer.save()
        return Response({"email": submission.email})

    print(serializer.errors)  # 👈 debug
    return Response(serializer.errors, status=400)


@api_view(['GET'])
def lookup(request):
    email = request.GET.get('email')
    subs = Submission.objects.filter(email=email)
    return Response(SubmissionSerializer(subs, many=True).data)


@api_view(['GET'])
def current_batch(request):
    batch = Batch.objects.filter(status='open').first()
    return Response(BatchSerializer(batch).data if batch else {})


@api_view(['GET'])
def results(request):
    batches = Batch.objects.filter(status='drawn')
    return Response(BatchSerializer(batches, many=True).data)

# ADMIN APIs


from django.contrib.auth.models import User


@api_view(['POST'])
@permission_classes([AllowAny])
def admin_login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    print("EMAIL:", email)

    try:
        user_obj = User.objects.get(email=email)
        print("FOUND USER:", user_obj.username)
    except User.DoesNotExist:
        print("❌ USER NOT FOUND")
        return Response({'detail': 'Invalid credentials'}, status=401)

    user = authenticate(username=user_obj.username, password=password)

    if user is not None:
        print("✅ AUTH SUCCESS")
        token = RefreshToken.for_user(user)
        return Response({'token': str(token.access_token)})

    print("❌ PASSWORD WRONG")
    return Response({'detail': 'Invalid credentials'}, status=401)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_submissions(request):
    status = request.GET.get('status')
    subs = Submission.objects.filter(status=status)
    return Response(SubmissionSerializer(subs, many=True).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def approve(request, id):
    sub = Submission.objects.get(id=id)
    assign_ticket(sub)
    return Response({"msg": "approved"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject(request, id):
    sub = Submission.objects.get(id=id)
    sub.status = 'rejected'
    sub.rejection_reason = request.data.get('reason')
    sub.save()
    return Response({"msg": "rejected"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_batches(request):
    return Response(BatchSerializer(Batch.objects.all(), many=True).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def draw(request, num):
    batch = Batch.objects.get(batch_number=num)
    result = draw_winner(batch)
    return Response(BatchSerializer(result).data)