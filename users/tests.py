import json
import unittest

from unittest      import mock
from unittest.mock import MagicMock, patch
from django.test   import TestCase, Client

from users.models import User

class KakaoSignInTest(TestCase):
    def setUp(self):
        User.objects.create(
            id = 1,
            kakao_id = 11111111,
            nickname = '모모',
            email = 'momo@gmail.com'
        )

    def tearDown(self):
        User.objects.all().delete()
    
    @patch('users.views.requests')
    def test_kakao_signin_success(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                    'id'            : 11111111,
                    'properties'    : {'nickname': '모모'}, 
                    'kakao_account' : {'email': 'momo@gmail.com'}
                }

        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {'HTTP_Authorization': 'fake_access_token'}
        response            = client.get("/users/login", **headers)
        self.assertEqual(response.status_code, 200)
    
    @patch('users.views.requests')
    def test_kakao_signin_key_error(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                    'id'            : 11111111,
                    'properties'    : {'nickname': '모모'}
                }

        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {'HTTP_Authorization': 'fake_access_token'}
        response            = client.get("/users/login", **headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'KEY_ERROR'})
