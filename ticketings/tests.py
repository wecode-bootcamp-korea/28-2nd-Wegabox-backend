import json
import jwt

from django.test             import TestCase, Client
from datetime                import datetime
from django.utils.dateformat import DateFormat

from movies.models     import Movie
from ticketings.models import Schedule, Region, Theater, Ticketing
from users.models      import User
from my_settings       import SECRET_KEY, ALGORITHM

class TicketingTest(TestCase):
    def setUp(self):
        User.objects.create(
            id = 1,
            kakao_id = 11111111,
            nickname = '모모',
            email = 'momo@gmail.com'
        )
        Movie.objects.create(
            id    = 1,
			title  = '첫번째 영화',
            description = '첫번째 영화의 설명',
            release_date = '2020-12-11',
            thumbnail_url = 'https://media.vlpt.us/images/nonasking/post/b5404a75-7771-49df-9726-b3ed5326c2fe/myphone3main.jpg'
        )
        Region.objects.create(
            id    = 1,
			name  = '첫번째 지역'
        )
        Theater.objects.create(
            id    = 1,
			name  = '첫번째 극장',
            region_id = 1
        )
        Schedule.objects.create(
            id    = 1,
            movie_id = 1,
            theater_id = 1,
            running_date = DateFormat(datetime.now()).format('Y-m-d'),
            start_time = '08:30',
            end_time = '11:00'
        )

        self.token = jwt.encode({'id' : 1}, SECRET_KEY, algorithm=ALGORITHM)

    def tearDown(self):
        Movie.objects.all().delete()
        Region.objects.all().delete()
        Theater.objects.all().delete()
        Schedule.objects.all().delete()
        User.objects.all().delete()
        
    def test_ticketingview_get_success(self):
        client = Client()
        response = client.get('/ticketings')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                "all_movies_list": [
                    {
                        "id": 1,
                        "value": "첫번째 영화"
                    }
                    
                ],
                "able_movies_list": [
                    {
                        "id": 1,
                        "value": "첫번째 영화"
                    }
                ],
                "all_regions_list": [
                    {
                        "id": 1,
                        "value": "첫번째 지역",
                        "theaters": [
                            {
                                "id": 1,
                                "value": "첫번째 극장"
                            }
                        ]
                    }
                ],
                "able_regions_list": [
                    {
                        "id": 1,
                        "value": "첫번째 지역",
                        "theaters": [
                            {
                                "id": 1,
                                "value": "첫번째 극장"
                            }
                        ]
                    }
                ],
                "fast_date":""
            }
        )
    
    def test_ticketingview_post_success(self):
        client = Client()
        header = {'HTTP_Authorization' : self.token}
        post_json = {
            'schedule_id' : 1
        }
        response = client.post('/ticketings', json.dumps(post_json), content_type='application/json', **header)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), 
            {
                'message' : '예매가 완료되었습니다.'
            }
        )
    
    def test_ticketingview_post_invalid_schedule(self):
        client = Client()
        header = {'HTTP_Authorization' : self.token}
        post_json = {
            'schedule_id' : 2
        }
        response = client.post('/ticketings', json.dumps(post_json), content_type='application/json', **header)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 
            {
                'message' : 'INVALID_SCHEDULE'
            }
        )


