# -*- coding: utf-8 -*-

import json
import sys

import datetime
from resources.lib.common import tools
from resources.lib.indexers.tmdb import TMDBAPI
from resources.lib.indexers.trakt import TraktAPI
from resources.lib.modules import database
from resources.lib.modules.trakt_sync.movies import TraktSyncDatabase

try:
    sysaddon = sys.argv[0]
    syshandle = int(sys.argv[1])
except:
    sysaddon = ''
    syshandle = ''

trakt = TraktAPI()
tmdbAPI = TMDBAPI()

trakt_database = TraktSyncDatabase()


class Menus:
    def __init__(self):
        self.itemList = []
        self.threadList = []
        self.viewType = tools.getSetting('movie.view')

    ######################################################
    # MENUS
    ######################################################

    def onDeckMovies(self):
        traktList = trakt.json_response('sync/playback/movies', limit=True)
        if traktList is None:
            return

        trakt_list = sorted(traktList, key=lambda i: tools.datetime_workaround(i['paused_at'][:19],
                                                                               format="%Y-%m-%dT%H:%M:%S",
                                                                               date_only=False), reverse=True)
        movie_list = []
        filter_list = []
        for i in trakt_list:
            if i['movie']['ids']['trakt'] not in filter_list:
                if int(i['progress']) != 0:
                    movie_list.append(i)
                    filter_list.append(i['movie']['ids']['trakt'])

        self.commonListBuilder(movie_list)
        tools.closeDirectory('movies')

    def discoverSoul(self):

        tools.addDirectoryItem(tools.lang(99999), 'moviesLatest', '', '')
        tools.addDirectoryItem(tools.lang(99989), 'moviesLatest4k', '', '')
        tools.addDirectoryItem(tools.lang(99987), 'moviesLatestReddit', '', '')
        tools.addDirectoryItem(tools.lang(99990), 'moviessoulCurated', '', '')
        tools.addDirectoryItem(tools.lang(99985), 'moviesRTBestofyear', '', '')
        tools.addDirectoryItem(tools.lang(99986), 'moviesNetflix', '', '')
        tools.addDirectoryItem(tools.lang(99992), 'moviessoulSpotlight', '', '')
        tools.addDirectoryItem(tools.lang(99984), 'moviesNeverseen', '', '')
        tools.addDirectoryItem(tools.lang(99983), 'moviesPixelHunter', '', '')

        # tools.addDirectoryItem('Years', 'movieYears')
        if tools.getSetting('searchHistory') == 'false':
            tools.addDirectoryItem(tools.lang(32016), 'moviesSearch', isFolder=True, isPlayable=False)
        else:
            tools.addDirectoryItem(tools.lang(32016), 'moviesSearchHistory')
        tools.closeDirectory('addons')

    def moviesLatest(self):
        trakt_list = trakt.json_response('users/giladg/lists/latest-releases/items?extended=full', limit=False)
        if trakt_list is None:
            return
        try:
            sort_by = trakt.response_headers['X-Sort-By']
            sort_how = trakt.response_headers['X-Sort-How']
            trakt_list = trakt.sort_list(sort_by, sort_how, trakt_list, 'movie')
        except:
            import traceback
            traceback.print_exc()
            pass

        self.commonListBuilder(trakt_list)
        tools.closeDirectory('movies')
        tools.closeDirectory('addons')

    def moviesLatest4k(self):
        trakt_list = trakt.json_response('users/giladg/lists/latest-4k-releases/items?extended=full', limit=False)
        if trakt_list is None:
            return
        try:
            sort_by = trakt.response_headers['X-Sort-By']
            sort_how = trakt.response_headers['X-Sort-How']
            trakt_list = trakt.sort_list(sort_by, sort_how, trakt_list, 'movie')
        except:
            import traceback
            traceback.print_exc()
            pass

        self.commonListBuilder(trakt_list)
        tools.closeDirectory('movies')

    def moviesLatestReddit(self):
        trakt_list = trakt.json_response('users/giladg/lists/subreddit-selections/items?extended=full', limit=False)
        if trakt_list is None:
            return
        try:
            sort_by = trakt.response_headers['X-Sort-By']
            sort_how = trakt.response_headers['X-Sort-How']
            trakt_list = trakt.sort_list(sort_by, sort_how, trakt_list, 'movie')
        except:
            import traceback
            traceback.print_exc()
            pass

        self.commonListBuilder(trakt_list)
        tools.closeDirectory('movies')

    def moviesRTBestofyear(self):
        trakt_list = trakt.json_response('users/lish408/lists/rotten-tomatoes-best-of-2019/items?extended=full', limit=False)
        if trakt_list is None:
            return
        try:
            sort_by = trakt.response_headers['X-Sort-By']
            sort_how = trakt.response_headers['X-Sort-How']
            trakt_list = trakt.sort_list(sort_by, sort_how, trakt_list, 'movie')
        except:
            import traceback
            traceback.print_exc()
            pass

        self.commonListBuilder(trakt_list)
        tools.closeDirectory('movies')

    def moviesNetflix(self):
        trakt_list = trakt.json_response('users/enormoz/lists/netflix-movies/items?extended=full', limit=False)
        if trakt_list is None:
            return
        try:
            sort_by = trakt.response_headers['X-Sort-By']
            sort_how = trakt.response_headers['X-Sort-How']
            trakt_list = trakt.sort_list(sort_by, sort_how, trakt_list, 'movie')
        except:
            import traceback
            traceback.print_exc()
            pass

        self.commonListBuilder(trakt_list)
        tools.closeDirectory('movies')

    def moviesPixelHunter(self):
        trakt_list = trakt.json_response('users/pixelhunterprime/lists/netflix/items/movie?extended=full', limit=False)
        if trakt_list is None:
            return
        try:
            sort_by = trakt.response_headers['X-Sort-By']
            sort_how = trakt.response_headers['X-Sort-How']
            trakt_list = trakt.sort_list(sort_by, sort_how, trakt_list, 'movie')
        except:
            import traceback
            traceback.print_exc()
            pass

        self.commonListBuilder(trakt_list)
        tools.closeDirectory('movies')

    def moviesNeverseen(self):
        trakt_list = trakt.json_response('users/_varg/lists/great-movies-you-may-have-never-heard-of/items?extended=full', limit=False)
        if trakt_list is None:
            return
        try:
            sort_by = trakt.response_headers['X-Sort-By']
            sort_how = trakt.response_headers['X-Sort-How']
            trakt_list = trakt.sort_list(sort_by, sort_how, trakt_list, 'movie')
        except:
            import traceback
            traceback.print_exc()
            pass

        self.commonListBuilder(trakt_list)
        tools.closeDirectory('movies')
        
    def moviessoulSpotlight(self):
        trakt_list = trakt.json_response('users/soul-tv/lists/spotlight-movies/items/movies?extended=full', limit=False)
        if trakt_list is None:
            return
        try:
            sort_by = trakt.response_headers['X-Sort-By']
            sort_how = trakt.response_headers['X-Sort-How']
            trakt_list = trakt.sort_list(sort_by, sort_how, trakt_list, 'movie')
        except:
            import traceback
            traceback.print_exc()
            pass

        self.commonListBuilder(trakt_list)
        tools.closeDirectory('movies')
        
    def moviessoulCurated(self):
        trakt_list = trakt.json_response('users/soul-tv/lists/soul-picks-movies/items/movies?extended=full', limit=False)
        if trakt_list is None:
            return
        try:
            sort_by = trakt.response_headers['X-Sort-By']
            sort_how = trakt.response_headers['X-Sort-How']
            trakt_list = trakt.sort_list(sort_by, sort_how, trakt_list, 'movie')
        except:
            import traceback
            traceback.print_exc()
            pass

        self.commonListBuilder(trakt_list)
        tools.closeDirectory('movies')

    ######################################################
    # MENU TOOLS
    ######################################################

    def commonListBuilder(self, trakt_list, info_return=False):

        if len(trakt_list) == 0:
            return
        if 'movie' in trakt_list[0]:
            trakt_list = [i['movie'] for i in trakt_list]

        self.itemList = trakt_database.get_movie_list(trakt_list)

        self.itemList = [x for x in self.itemList if x is not None and 'info' in x]
        self.itemList = tools.sort_list_items(self.itemList, trakt_list)

        list_items = []

        for item in self.itemList:
            try:

                name = tools.display_string(item['info']['title'])

                if not self.is_aired(item['info']):
                    if tools.getSetting('general.hideUnAired') == 'true':
                        continue
                    name = tools.colorString(name, 'red')
                    name = tools.italic_string(name)

                args = {'trakt_id': item['ids']['trakt'], 'item_type': 'movie'}
                args = tools.quote(json.dumps(args, sort_keys=True))

            except:
                import traceback
                traceback.print_exc()
                continue

            if item is None:
                continue

            item['info']['title'] = item['info']['originaltitle'] = name
            list_items.append(tools.addDirectoryItem(name, 'getSources', item['info'], item['art'], item['cast'],
                                                     isFolder=False, isPlayable=True, actionArgs=args,
                                                     set_ids=item['ids'], bulk_add=True))

        if info_return:
            return list_items

        tools.addMenuItems(syshandle, list_items, len(list_items))

    def runThreads(self, join=True):
        for thread in self.threadList:
            thread.start()

        if join == True:
            for thread in self.threadList:
                thread.join()

    def is_aired(self, info):
        try:
            try:
                air_date = info['aired']
            except:
                air_date = info['premiered']

            if tools.getSetting('general.datedelay') == 'true':
                air_date = tools.datetime_workaround(air_date, '%Y-%m-%d', date_only=True)
                air_date += datetime.timedelta(days=1)
            else:
                air_date = tools.datetime_workaround(air_date, '%Y-%m-%d', date_only=True)

            if air_date > datetime.date.today():
                return False

            else:
                return True
        except:
            # Assume an item is aired if we do not have any information on it
            return True
