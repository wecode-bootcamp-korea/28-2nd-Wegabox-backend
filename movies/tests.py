import json

from movies.models        import Movie
from django.test          import TestCase, Client
from datetime             import datetime

from ticketings.models import Region, Schedule, Theater, Ticketing, User

class MovieTest(TestCase):
    def setUp(self):
        Region.objects.create(
            id = 1,
            name = '서울',
            )
        Theater.objects.create(
            id = 1,
            name = '강남',
            region_id = 1,
            )
        Movie.objects.create(
            id = 1,
            title = '해리포터와 친구들1',
            description = '해리포터와 친구들의 여행 이야기',
            thumbnail_url = 'https://images.unsplash.com/photo-1610466024868-910c6e7e8929?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80',
            release_date = '2022-01-16',
            )
        Movie.objects.create(
            id = 2,
            title = '해리포터와 친구들2',
            description = '해리포터와 친구들의 여행 이야기',
            thumbnail_url = 'https://images.unsplash.com/photo-1610466024868-910c6e7e8929?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80',
            release_date = '2022-01-17',
            )
        Movie.objects.create(
            id = 3,
            title = '해리포터와 친구들3',
            description = '해리포터와 친구들의 여행 이야기',
            thumbnail_url = 'https://images.unsplash.com/photo-1610466024868-910c6e7e8929?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80',
            release_date = '2022-01-18',
            )
        Movie.objects.create(
            id = 4,
            title = '해리포터와 친구들4',
            description = '해리포터와 친구들의 여행 이야기',
            thumbnail_url = 'https://images.unsplash.com/photo-1610466024868-910c6e7e8929?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80',
            release_date = '2022-01-19',
            )
        Movie.objects.create(
            id = 5,
            title = '해리포터와 친구들5',
            description = '해리포터와 친구들의 여행 이야기',
            thumbnail_url = 'https://images.unsplash.com/photo-1610466024868-910c6e7e8929?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80',
            release_date = '2022-01-20',
            )
        Schedule.objects.create(
            id = 1,
            running_date = '2022-01-18',
            start_time = '08:30:00.000000',
            end_time = '11:00:00.000000',
            movie_id = 1,
            theater_id = 1,
            )
        Schedule.objects.create(
            id = 2,
            running_date = '2022-01-18',
            start_time = '08:30:00.000000',
            end_time = '11:00:00.000000',
            movie_id = 1,
            theater_id = 1,
            )
        Schedule.objects.create(
            id = 3,
            running_date = '2022-01-18',
            start_time = '08:30:00.000000',
            end_time = '11:00:00.000000',
            movie_id = 1,
            theater_id = 1,
            )
        Schedule.objects.create(
            id = 4,
            running_date = '2022-01-18',
            start_time = '08:30:00.000000',
            end_time = '11:00:00.000000',
            movie_id = 2,
            theater_id = 1,
            )
        Schedule.objects.create(
            id = 5,
            running_date = '2022-01-18',
            start_time = '08:30:00.000000',
            end_time = '11:00:00.000000',
            movie_id = 2,
            theater_id = 1,
            )
        User.objects.create(
            id = 1,
            kakao_id = 1234,
            nickname = 'jang',
            email = 'jang@naver.com',
        )
        Ticketing.objects.create(
            id = 1,
            schedule_id = 1,
            user_id = 1,
        )
        Ticketing.objects.create(
            id = 2,
            schedule_id = 2,
            user_id = 1,
        )
        Ticketing.objects.create(
            id = 3,
            schedule_id = 3,
            user_id = 1,
        )
        Ticketing.objects.create(
            id = 4,
            schedule_id = 4,
            user_id = 1,
        )
        Ticketing.objects.create(
            id = 5,
            schedule_id = 5,
            user_id = 1,
        )

    def tearDown(self):
        Movie.objects.all().delete()

    def test_movie_get_success(self):
        client   = Client()
        response = client.get('/movies?offset=0&limit=2&released=false')

        self.assertEqual(response.json(),
            {
                "result": [
                    {
                        "movie_id": 1,
                        "title": "해리포터와 친구들1",
                        "description": "해리포터와 친구들의 여행 이야기",
                        "thumbnail_url": "https://images.unsplash.com/photo-1610466024868-910c6e7e8929?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80",
                        "release_date": "2022-01-16",
                        "ticket_rate": 60
                    },
                    {
                        "movie_id": 2,
                        "title": "해리포터와 친구들2",
                        "description": "해리포터와 친구들의 여행 이야기",
                        "thumbnail_url": "https://images.unsplash.com/photo-1610466024868-910c6e7e8929?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80",
                        "release_date": "2022-01-17",
                        "ticket_rate": 40
                    }
                ],
                "total_movie": {
                    "total_movie": 5
                }
            }
        )
        self.assertEqual(response.status_code, 200)