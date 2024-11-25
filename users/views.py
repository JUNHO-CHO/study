from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import authenticate
from.serializers import UserSerializer, UserprofileSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model


#회원가입 API
@api_view(['POST'])
def sign_up(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)  # 201 Created 응답
        return Response(serializer.errors, status=400)  # 400 Bad Request 응답
    

#로그인 API
@api_view(['POST'])
def sign_in(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'detail': '아이디와 비밀번호가 맞지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if user:
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)  

        return Response({
            'access': str(access_token),
            'refresh': str(refresh) 
        }, status=status.HTTP_200_OK)
    return Response({'detail': '로그인 실패'}, status=status.HTTP_401_UNAUTHORIZED)


#로그아웃 API
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sign_out(request):
    refresh_token =request.data.get("refresh_token")

    if not refresh_token:
        return Response({'detail': '로그아웃 실패'}, status=status.HTTP_400_BAD_REQUEST)
    token = RefreshToken(refresh_token)
    token.blacklist()
    return Response({'detail': '로그아웃 완료'}, status=status.HTTP_200_OK)


#회원탈퇴 API
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    password = request.data.get("password")
    if not password:
        return Response({'messate':'비밀번호를 입력해야 합니다.'}, status = status.HTTP_400_BAD_REQUEST)
    
    if not request.user.check_password(password):
        return Response({'message':'비밀번호가 틀렸습니다.'}, status = status.HTTP_400_BAD_REQUEST)
    
    request.user.delete()
    return Response({'detail': '회원탈퇴 완료'}, status=status.HTTP_200_OK)

#회원 비밀번호 수정
@api_view(['put'])
@permission_classes([IsAuthenticated])
def updatepassword(request):
    old_password = request.data.get("old_password")
    new_password = request.data.get("new_password")

    if not old_password or not new_password:
        return Response({'message':'변경할 비밀번호 입력하세요.'}, status = status.HTTP_400_BAD_REQUEST)    
    if not request.user.check_password(old_password):
        return Response({'message':'기존 비밀번호를 틀렸습니다.'}, status = status.HTTP_400_BAD_REQUEST)
    if old_password == new_password:
        return Response({'message':'변경할 비밀번호와 기존 비밀번호를 다르게 입력하세요.'}, status = status.HTTP_400_BAD_REQUEST)
    
    request.user.set_password(new_password)
    request.user.save()

    refresh = RefreshToken.for_user(request.user)
    access_token = refresh.access_token
    
    return Response({
        'access': str(access_token),
        'refresh': str(refresh),
        'message':'비밀번호가 변경되었습니다.'
    }, status=status.HTTP_200_OK)

#프로필 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request, pk):
    User = get_user_model() #커스텀 유저를 동적으로 가져옴
    user = get_object_or_404(User, pk=pk)
    serializer = UserprofileSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)

#회원 프로필 수정
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







# 
# 1. 토큰인증 세션인증 하는방법 
# 2. 두개의 인증 차이
# ( 인증 둘다 구현 가능하고 선택할 수도 있게)
# 3.회원기능 구현(모델 이것저것 다넣어서)
# 4.★ FBV기반으로 구현
# 5.재밌는거
# - 패스워드 변경시 기존패스워드랑 같으면 변경처리 안되게
# 