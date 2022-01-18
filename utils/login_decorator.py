import jwt

from django.http  import JsonResponse

from my_settings  import SECRET_KEY, ALGORITHM
from users.models import User

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            jwt_token    = request.headers.get('Authorization', None)
            payload      = jwt.decode(jwt_token, SECRET_KEY, algorithms=ALGORITHM)
            user         = User.objects.get(id=payload['id'])
            request.user = user
        
            return func(self, request, *args, **kwargs)

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message' : 'INVALID TOKEN'}, status = 400)

        except User.DoesNotExist:
            return JsonResponse({'message' : 'USER DOES NOT EXIST'}, status = 400)
    
    return wrapper