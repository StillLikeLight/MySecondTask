from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.authtoken.models import Token
from OTPVerificationClass import OTPVerification
from usr.serializers import UserSerializer

otp_verifier = OTPVerification()


@api_view(['POST'])
def send_otp_email_verification(request):
    # 获取前端发送的邮件
    email_address_from_request = request.data.get('email')

    if not email_address_from_request:
        return Response('Email address is required', status=status.HTTP_400_BAD_REQUEST)

    # 生成验证码、记录当前时间、邮箱地址
    otp_store = otp_verifier.generate_otp(email_address_from_request)

    try:
        # 发送验证码
        otp_verifier.send_otp_email(email_address_from_request, otp_store['otp'])
    except Exception as e:
        print(e)
        return Response('Failed to send OTP email', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'message': 'OTP sent successfully', 'otp_store': otp_store}, status=status.HTTP_200_OK)


@api_view(['POST'])
def register(request):
    # 判断邮箱是否已经注册
    if User.objects.filter(email=request.data.get('email')).exists():
        return Response('Email address already exists', status=status.HTTP_400_BAD_REQUEST)

    if otp_verifier.verify_otp(request.data['email'], request.data['otp']):
        request.data.pop('otp')

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            user = User.objects.get(username=request.data['username'])

            # hashes the password
            user.set_password(request.data['password'])
            user.save()

            # create the user and save to the database
            token = Token.objects.create(user=user)

            # returns the response
            return Response({'token': token.key, 'user': serializer.data})
        else:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response("Wrong or No OTP Code!", status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def login(request):
    if otp_verifier.verify_otp(request.data['email'], request.data['otp']):
        # 验证码不需要保存到数据库中
        request.data.pop('otp')

        # 通过邮箱地址获取一个user对象
        user = User.objects.get(email=request.data.get('email'))
        # user为True表示邮箱正确，然后检查密码
        if user and user.check_password(request.data.get('password')):
            # 获取或生成token
            token, created = Token.objects.get_or_create(user=user)
            serializer = UserSerializer(user)
            return Response({'token': token.key, 'user': serializer.data})
        else:
            return Response({"message": "email or password is incorrect"}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"message": "Wrong or No OTP Code!"}, status=status.HTTP_404_NOT_FOUND)


# @api_view(['GET'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def test_token(request):
#     return Response("passed!")
