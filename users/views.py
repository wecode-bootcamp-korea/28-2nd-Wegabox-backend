import json
import jwt
import requests

from django.http  import JsonResponse
from django.views import View

from users.models import User
from my_settings  import SECRET_KEY, ALGORITHM

class KakaoClient:
    def __init__(self, access_token):
        self.API_URL = 'https://kapi.kakao.com/v2/user/me'
        self.headers = {'Authorization': f'Bearer {access_token}'}

    def get_user_profile(self):
        response = requests.get(self.API_URL, headers = self.headers, timeout=10)
        return response.json()

class KakaoSignInView(View):
    def get(self, request):
        try:
            access_token = request.headers['Authorization'] 

            kakao_client = KakaoClient(access_token)
            profile = kakao_client.get_user_profile()

            kakao_account = profile['kakao_account']
            kakao_id = profile['id']
            properties = profile['properties']
            email = kakao_account['email']
            nickname = properties['nickname']

            user, created  = User.objects.get_or_create(
                kakao_id = kakao_id,
                email    = email,
                nickname = nickname
            )
            jwt_token = jwt.encode({"id" : user.id}, SECRET_KEY, algorithm=ALGORITHM)   

            return JsonResponse({
                'token'    : jwt_token,
                'nickname' : user.nickname,
                'kakao_id' : user.kakao_id,
                'email'    : user.email
            }, status = 200)
            
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)