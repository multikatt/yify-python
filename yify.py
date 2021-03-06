import requests, copy, json

class yify:
    base_url = 'https://yts.re/api/'
    uri = ''

    opt_qualities = ['720p', '1080p', '3D', 'ALL']
    opt_ratings = range(10)
    opt_sorts = ['date', 'seeds', 'size', 'alphabet', 'rating']
    opt_orders = ['desc', 'asc']

    movie_list_params = {
        'limit':            20,         # Maximum number of returned items
        'set':              1,          # Which set (page) do you want to return?
        'quality':          'ALL',      # {720p, 1080p, 3D, ALL}
        'rating':           0,          # Minimum rating between 0 - 9
        'keywords':         '',         # {String}
        'genre':            'ALL',      # {String} Refer to http://www.imdb.com/genre/
        'sort':             'date',     # {date, seeds, size, alphabet, rating}
        'order':            'desc'      # {desc, asc}
    }

    data_formats = ['json', 'xml', 'csv']

    def newest(self, quality= 'ALL', format='json'):
        return self.movie_list(1, 20, 'ALL', 0, '', 'ALL', 'date', 'desc', format)

    def movie_detail(self, id=None, format='json'):
        self.uri = 'movie'

        data = {
            'movie':    [],
            'errors':   {
                'state':    False,
                'message':  []
            }
        }

        errors = {
            'state': False,
            'message': []
        }

        if format in self.data_formats:
            self.uri = '%s.%s' % (self.uri, format)
        else:
            errors['state'] = True
            errors['message'].append('Data return format must be json, xml or csv')

        if id is None:
            errors['state'] = True
            errors['message'].append('Movie ID must be blank')

        if errors['state']:
            data['errors'] = errors
        else:
            url = "%s?id=%s" % (self._construct_url(), id)
            m = self._fetch_data(url)
            if m is not None:
                data['movie'] = m

        return data

    def upcoming(self, format='json'):
        self.uri = 'upcoming'

        data = {
            'movies':   [],
            'errors':   {
                'state':    False,
                'message':  []
            }
        }

        errors = {
            'state': False,
            'message': []
        }

        if format in self.data_formats:
            self.uri = '%s.%s' % (self.uri, format)
        else:
            errors['state'] = True
            errors['message'].append('Data return format must be json, xml or csv')

        if errors['state']:
            data['errors'] = errors
        else:
            url = self._construct_url()
            m = self._fetch_data(url)
            if m is not None:
                data['movies'] = m

        return data

    def movie_list(self,
                   set=1, limit=20,
                   quality='ALL', rating=0,
                   keywords='', genre='ALL',
                   sort='date', order='desc',
                   format='json'):
        self.uri = 'list'

        data = {
            'movies':   [],
            'errors':   {
                'state':    False,
                'message':  []
            }
        }

        params = copy.deepcopy(self.movie_list_params)
        errors = {
            'state': False,
            'message': []
        }

        if quality in self.opt_qualities:
            params['quality'] = quality
        else:
            errors['state'] = True
            errors['message'].append('Quality needs to be 720p, 1080p, 3D or ALL')

        if rating in self.opt_ratings:
            params['rating'] = rating
        else:
            errors['state'] = True
            errors['message'].append('Rating needs to be an integer between 0 to 10')

        if sort in self.opt_sorts:
            params['sort'] = sort
        else:
            errors['state'] = True
            errors['message'].append('Sort needs to be date, seeds, size, alphabet or rating')

        if order in self.opt_orders:
            params['order'] = order
        else:
            errors['state'] = True
            errors['message'].append('Order needs to be desc or asc')

        if format in self.data_formats:
            self.uri = '%s.%s' % (self.uri, format)
        else:
            errors['state'] = True
            errors['message'].append('Data return format must be json, xml or csv')

        if errors['state']:
            data['errors'] = errors
        else:
            url = self._construct_url()
            m = self._fetch_data(url)
            if m is not None:
                data['movies'] = m

        return data

    def _fetch_data(self, url):
        r = requests.get(url)
        if r.status_code == 200:
            return json.loads(r.text)
        else:
            return None

    def _construct_url(self):
        return "%s%s" % (self.base_url, self.uri)

    class client:
        def waku(self):
            return "waku"
