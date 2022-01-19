import json

from datetime                   import datetime
from django.http.response       import JsonResponse
from django.views               import View
from movies.models              import Movie
from ticketings.models          import Ticketing
from django.db.models           import Q
from django.db.models           import Count

class MovieView(View):
    def get(self, request):
        offset   = int(request.GET.get('offset',None))
        limit    = int(request.GET.get('limit',None))
        released = request.GET.get('released',None)

        q = Q()

        today = datetime.today().strftime('%Y-%m-%d')

        if released == 'true':
            q &= Q(release_date__lte = today)

        total_movie = Movie.objects.filter(q).count()
        total_movies = dict(total_movie = total_movie)

        ticketings_total = Ticketing.objects.all().count()
 
        movies = Movie.objects.filter(q).annotate(ticket_rate=Count('schedule__ticketing')/ticketings_total *100)
        
        results = [{
            'movie_id'      : movie.id,
            'title'         : movie.title,
            'description'   : movie.description,
            'thumbnail_url' : movie.thumbnail_url,
            'release_date'  : movie.release_date,
            'ticket_rate'   : movie.ticket_rate
            } for movie in movies.order_by('-ticket_rate')[offset:offset+limit]]

        return JsonResponse({'result' : results, 'total_movie' : total_movies}, status = 200)