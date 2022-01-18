import json

from django.http             import JsonResponse
from django.views            import View
from django.db.models        import Q
from datetime                import datetime
from django.utils.dateformat import DateFormat

from utils.login_decorator import login_decorator
from users.models          import User
from movies.models         import Movie
from ticketings.models     import Schedule, Ticketing, Region, Theater

class TicketingView(View):
    def get(self, request):
        today             = DateFormat(datetime.now()).format('Y-m-d')
        running_date      = request.GET.get('running_date', today)
        movie_id          = request.GET.getlist('movie_id', None)
        deactive_movie_id = request.GET.get('deactive_movie_id', None) # 불가능 영화를 선택한 경우
        region            = request.GET.get('region', None)
        theater           = request.GET.getlist('theater', None)

        schedules_list     = self.get_schedules(running_date, movie_id, theater)
        regions            = self.get_regions(movie_id, region, running_date)
        theaters           = self.get_theaters(region, running_date, movie_id)
        movies             = self.get_movies(running_date, theater)
        fast_date          = ''

        result = {
            'all_regions_list'  : regions['all'],
            'able_regions_list' : regions['available'],
            'all_movies_list'   : movies['all'],
            'able_movies_list'  : movies['available'],
            'fast_date'         : fast_date
        }

        result = self.handle_result(result, theater, region, theaters, schedules_list, deactive_movie_id)

        return JsonResponse(result, status=200)
    
    @login_decorator
    def post(self, request):
        try:
            data        = json.loads(request.body)
            schedule_id = int(data['schedule_id'])
            schedule    = Schedule.objects.get(id=schedule_id)

            Ticketing.objects.create(user=request.user, schedule=schedule)

            return JsonResponse({'message' : '예매가 완료되었습니다.'}, status=201)
        
        except Schedule.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_SCHEDULE'}, status=400)
        
    def get_schedules(self, running_date, movie_id, theater):
        # 스케줄(날짜|영화|극장)
        schedule_condition = Q(running_date = running_date)

        if movie_id:
            schedule_condition &= Q(movie_id__in = movie_id)

        if theater:
            schedule_condition &= Q(theater_id__in = theater)

        schedules = Schedule.objects.filter(schedule_condition) ## 스케줄(날짜|영화|극장)
        schedules_list = [{
            'id'        : schedule.id,
            'title'     : schedule.movie.title,
            'start_time': schedule.start_time,
            'end_time'  : schedule.end_time
        } for schedule in schedules]

        return schedules_list

    def get_regions(self, movie_id, region, running_date):
        # 지역(날짜|영화)
        ## 전체 지역(:극장) 리스트
        all_regions = Region.objects.all()
        all_regions_list = [{
            'id'       : region.id,
            'value'    : region.name,
            'theaters' : [{
                'id'    : theater.id, 
                'value' : theater.name
                } for theater in Theater.objects.filter(region=region)]
        } for region in all_regions]

        ## 가능 지역(극장) 리스트
        region_schedule_condition = Q(running_date=running_date)

        if movie_id:
            region_schedule_condition &= Q(movie_id__in=movie_id)

        able_region_condition = Q()

        if movie_id:
            able_region_condition &= Q(id__in=Schedule.objects.filter(movie_id__in=movie_id).values_list('theater__region_id'))
        
        if region:
            able_region_condition &= Q(id=region)
        
        able_regions = Region.objects.filter(able_region_condition, id__in=Schedule.objects.filter(region_schedule_condition).values_list('theater__region_id'))
        able_regions_list = [{
            'id'       : region.id,
            'value'    : region.name,
            'theaters' : [{
                'id'    : theater.id, 
                'value' : theater.name
                } for theater in Theater.objects.filter(region=region, id__in=Schedule.objects.filter(region_schedule_condition).values_list('theater_id'))]
        } for region in able_regions]    
        
        return {
            'all': all_regions_list, 
            'available': able_regions_list
        }
    
    def get_theaters(self, region, running_date, movie_id):
        # 극장(날짜|영화|지역)
        ## 전체 극장 리스트
        all_theater_condition = Q()

        if region:
            all_theater_condition &= Q(region_id=region)

        all_theaters      = Theater.objects.filter(all_theater_condition)
        all_theaters_list = [{
            'id'    : theater.id, 
            'value' : theater.name
            } for theater in all_theaters]

        ## 가능 극장 리스트
        theater_schedule_condition = Q(running_date = running_date)

        if movie_id:
            theater_schedule_condition &= Q(movie_id__in=movie_id)

        able_theater_condition = Q()

        if region:
            able_theater_condition &= Q(region=region)
        
        able_theater_condition &= Q(id__in = Schedule.objects.filter(theater_schedule_condition).values_list('theater_id'))
        able_theaters           = all_theaters.filter(able_theater_condition)
        able_theaters_list      = [{
            'id'    : theater.id, 
            'value' : theater.name
            } for theater in able_theaters]
        
        return {
            'all': all_theaters_list, 
            'available': able_theaters_list
        }

    def get_movies(self, running_date, theater):
        # 영화(날짜|극장)
        ## 전체 영화 리스트
        all_movies      = Movie.objects.all()
        all_movies_list = [{
            'id'    : movie.id, 
            'value' : movie.title
            } for movie in all_movies]
        ## 가능 영화 리스트
        able_movie_condition = Q(id__in = Schedule.objects.filter(running_date=running_date).values_list('movie_id'))
        
        if theater:
            able_movie_condition &= Q(id__in = Schedule.objects.filter(theater_id__in=theater).values_list('movie_id'))
        
        able_movies      = Movie.objects.filter(able_movie_condition)
        able_movies_list = [{
            'id'    : movie.id, 
            'value' : movie.title
            } for movie in able_movies]

        return {
            'all': all_movies_list, 
            'available': able_movies_list
        }

    def handle_result(self, result, theater, region, theaters, schedules_list, deactive_movie_id):
        # 극장이 있는 경우
        if theater:
            result['schedules_list'] = schedules_list 

        # 극장이 없고 지역만 있는 경우
        if region:
            result['all_theaters_list']  = theaters['all']
            result['able_theaters_list'] = theaters['available']

        # 불가능 영화를 선택한 경우
        if deactive_movie_id:
            deactive_movie      = Movie.objects.get(id=deactive_movie_id)
            fast_date           = Schedule.objects.filter(movie=deactive_movie).order_by('-running_date')[0].running_date
            result['fast_date'] = fast_date

        return result