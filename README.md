# study
블로그 주소 : https://junoblog.tistory.com/manage/posts

USER
코드와 코드 작동 순서

#회원가입 API
@api_view(['POST'])
def sign_up(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)  # 201 Created 응답
        return Response(serializer.errors, status=400)  # 400 Bad Request 응답
    
1. 회원가입 API (sign_up)
1) 입력 데이터 검증: 클라이언트에서 POST 요청으로 전달된 데이터를 UserSerializer로 검증
2) 데이터 유효성 검사: 데이터가 유효하면 사용자 정보를 저장
3) 응답: 저장된 사용자 데이터와 함께 HTTP 201 상태 코드로 응답
4) 유효하지 않으면 오류 응답: 데이터가 유효하지 않으면 오류 메시지와 함께 HTTP 400 상태 코드로 응답



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

2. 로그인 API (sign_in)
1) 입력 데이터 확인: POST 요청에서 username과 password를 가져옴
2) 유효성 검사: username 또는 password가 없으면 오류메세지 응답
3) 인증: authenticate() 함수로 사용자 인증을 시도
4) 인증 성공:
     RefreshToken.for_user(user)로 JWT Refresh Token 생성
     access_token을 포함하여 응답
5) 인증 실패: 로그인 실패 시 401 상태 코드와 함께 오류메세지 응답



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

3. 로그아웃 API (sign_out)
1) POST 요청 처리: 요청 데이터에서 refresh_token을 가져옴
2) 유효성 검사: refresh_token이 없으면 오류메세지 응답
3) 토큰 블랙리스트 처리: RefreshToken(refresh_token) 객체로 토큰을 처리한 후, blacklist() 메서드로 블랙리스트에 등록
4) 응답: 로그아웃 완료 메시지와 함께 HTTP 200 상태 코드로 응답




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

4. 회원 탈퇴 API (delete_user)
1) 비밀번호 확인: 요청 데이터에서 password를 가져오고 비밀번호가 제공되지 않으면 오류메세지 응답
2) 비밀번호 검증: 사용자가 입력한 비밀번호가 실제 비밀번호와 일치하는지 확인
3) 비밀번호가 틀리면 오류메세지 응답
4) 회원 삭제: 비밀번호가 맞으면 사용자를 삭제하고 HTTP 200 상태 코드로 응답


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

5. 회원 비밀번호 수정 API (updatepassword)
1) 입력 데이터 검증: 요청 데이터에서 old_password와 new_password를 가져옴
2) 유효성 검사 
2-1) old_password 또는 new_password가 없으면 오류메세지 응답
2-1) 기존 비밀번호가 맞지 않으면 오류메세지 응답
2-2) 새 비밀번호가 기존 비밀번호와 같으면 오류메세지 응답
3) 비밀번호 변경:
3-1) 비밀번호가 유효하면 request.user.set_password(new_password)로 새 비밀번호 설정
3-2) 사용자 저장 후, JWT 토큰을 새로 발급
4) 응답: 변경된 비밀번호에 대한 확인 메시지와 함께 새로운 access_token과 refresh_token을 반환


#프로필 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request, pk):
    User = get_user_model() #커스텀 유저를 동적으로 가져옴
    user = get_object_or_404(User, pk=pk)
    serializer = UserprofileSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)
    
6. 프로필 조회 API (profile)
1) GET 요청 처리: pk 파라미터를 통해 특정 사용자 프로필 조회
2) 사용자 가져오기: get_user_model()로 현재 사용자의 모델을 동적으로 가져오고, 
                   get_object_or_404()로 pk에 해당하는 사용자 정보 조회
3) 프로필 데이터 반환: UserprofileSerializer를 사용해 사용자 데이터를 직렬화하고 
                      HTTP 200 상태 코드와 함께 응답



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
    
7. 회원 프로필 수정 API (update_profile)
1) PUT 요청 처리: request.user로 현재 로그인한 사용자 정보를 수정
2) 직렬화 및 검증: UserSerializer를 사용해 사용자 데이터 업뎃
    partial=True로 일부 필드만 수정 가능하도록 설정
3) 수정된 데이터 저장: 직렬화된 데이터를 저장하고 HTTP 200 상태 코드와 함께 수정된 데이터를 반환
4) 검증 실패: 데이터 검증이 실패하면 오류 메시지와 함께 HTTP 400 상태 코드로 응답