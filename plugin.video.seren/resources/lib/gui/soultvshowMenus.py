# -*- coding: utf-8 -*-

import datetime
import json
import sys
from threading import Thread

from resources.lib.common import tools
from resources.lib.indexers.trakt import TraktAPI
from resources.lib.modules import database
from resources.lib.modules.trakt_sync.shows import TraktSyncDatabase
from resources.lib.modules.trakt_sync.hidden import TraktSyncDatabase as HiddenDatabase

try:
    from Queue import Queue
except:
    from queue import Queue

sysaddon = sys.argv[0]
try:
    syshandle = int(sys.argv[1])
except:
    syshandle = ''
trakt = TraktAPI()

language_code = tools.get_language_code()

trakt_database = TraktSyncDatabase()
hidden_database = HiddenDatabase()


class Menus:
    def __init__(self):
        self.itemList = []
        self.threadList = []
        self.direct_episode_threads = []
        self.title_appends = tools.getSetting('general.appendtitles')
        self.task_queue = Queue(40)

    ######################################################
    # MENUS
    ######################################################

    def onDeckShows(self):
        hidden_shows = hidden_database.get_hidden_items('progress_watched', 'shows')
        trakt_list = trakt.json_response('sync/playback/episodes', limit=True)

        if trakt_list is None:
            return
        trakt_list = [i for i in trakt_list if i['show']['ids']['trakt'] not in hidden_shows]
        trakt_list = sorted(trakt_list, key=lambda i: tools.datetime_workaround(i['paused_at'][:19],
                                                                                format="%Y-%m-%dT%H:%M:%S",
                                                                                date_only=False), reverse=True)
        filter_list = []
        showList = []
        sort_list = []
        for i in trakt_list:
            if i['show']['ids']['trakt'] not in filter_list:
                if int(i['progress']) != 0:
                    showList.append(i)
                    filter_list.append(i['show']['ids']['trakt'])
                    sort_list.append(i['show']['ids']['trakt'])

        sort = {'type': 'showInfo', 'id_list': sort_list}
        self.mixedEpisodeBuilder(showList, sort=sort)
        tools.closeDirectory('tvshows')

    def discoverSoul(self):

        tools.addDirectoryItem(tools.lang(99998), 'showsGary', '', '')
        tools.addDirectoryItem(tools.lang(99997), 'showsNetflix', '', '')
        tools.addDirectoryItem(tools.lang(99996), 'showsAmazon', '', '')
        tools.addDirectoryItem(tools.lang(99995), 'showsHulu', '', '')
        tools.addDirectoryItem(tools.lang(99994), 'soulSpotlight', '', '')
        tools.addDirectoryItem(tools.lang(99993), 'showssoulSpotlight', '', '')
        tools.addDirectoryItem(tools.lang(99991), 'showssoulCurated', '', '')
        tools.addDirectoryItem(tools.lang(99983), 'showsPixelHunter', '', '')
        tools.closeDirectory('addons')

    def showsGary(self):
        trakt_list = trakt.json_response('users/garycrawfordgc/lists/new-shows/items/show?extended=full', limit=False)
        if trakt_list is None:
            return
        try:
            sort_by = trakt.response_headers['X-Sort-By']
            sort_how = trakt.response_headers['X-Sort-How']
            trakt_list = trakt.sort_list(sort_by, sort_how, trakt_list, 'show')
        except:
            tools.log('Failed to sort trakt list by response headers', 'error')
            pass
        self.showListBuilder(trakt_list)
        tools.closeDirectory('tvshows')

    def showsNetflix(self):
        trakt_list = trakt.json_response('users/enormoz/lists/netflix/items/show?extended=full', limit=False)
        if trakt_list is None:
            return
        try:
            sort_by = trakt.response_headers['X-Sort-By']
            sort_how = trakt.response_headers['X-Sort-How']
            trakt_list = trakt.sort_list(sort_by, sort_how, trakt_list, 'show')
        except:
            tools.log('Failed to sort trakt list by response headers', 'error')
            pass
        self.showListBuilder(trakt_list)
        tools.closeDirectory('tvshows')

    def showsAmazon(self):
        trakt_list = trakt.json_response('users/enormoz/lists/amazon/items/show?extended=full', limit=False)
        if trakt_list is None:
            return
        try:
            sort_by = trakt.response_headers['X-Sort-By']
            sort_how = trakt.response_headers['X-Sort-How']
            trakt_list = trakt.sort_list(sort_by, sort_how, trakt_list, 'show')
        except:
            tools.log('Failed to sort trakt list by response headers', 'error')
            pass
        self.showListBuilder(trakt_list)
        tools.closeDirectory('tvshows')

    def showsHulu(self):
        trakt_list = trakt.json_response('users/enormoz/lists/hulu/items/show?extended=full', limit=False)
        if trakt_list is None:
            return
        try:
            sort_by = trakt.response_headers['X-Sort-By']
            sort_how = trakt.response_headers['X-Sort-How']
            trakt_list = trakt.sort_list(sort_by, sort_how, trakt_list, 'show')
        except:
            tools.log('Failed to sort trakt list by response headers', 'error')
            pass
        self.showListBuilder(trakt_list)
        tools.closeDirectory('tvshows')

    def soulSpotlight(self):
        trakt_list = trakt.json_response('users/soul-tv/lists/spotlight/items/show?extended=full', limit=False)
        if trakt_list is None:
            return
        try:
            sort_by = trakt.response_headers['X-Sort-By']
            sort_how = trakt.response_headers['X-Sort-How']
            trakt_list = trakt.sort_list(sort_by, sort_how, trakt_list, 'show')
        except:
            tools.log('Failed to sort trakt list by response headers', 'error')
            pass
        self.showListBuilder(trakt_list)
        tools.closeDirectory('tvshows')

    def showssoulSpotlight(self):
        trakt_list = trakt.json_response('users/soul-tv/lists/spotlight-tv-shows/items/show?extended=full', limit=False)
        if trakt_list is None:
            return
        try:
            sort_by = trakt.response_headers['X-Sort-By']
            sort_how = trakt.response_headers['X-Sort-How']
            trakt_list = trakt.sort_list(sort_by, sort_how, trakt_list, 'show')
        except:
            tools.log('Failed to sort trakt list by response headers', 'error')
            pass
        self.showListBuilder(trakt_list)
        tools.closeDirectory('tvshows')

    def showssoulCurated(self):
        trakt_list = trakt.json_response('users/soul-tv/lists/soul-picks-movies/items/show?extended=full', limit=False)
        if trakt_list is None:
            return
        try:
            sort_by = trakt.response_headers['X-Sort-By']
            sort_how = trakt.response_headers['X-Sort-How']
            trakt_list = trakt.sort_list(sort_by, sort_how, trakt_list, 'show')
        except:
            tools.log('Failed to sort trakt list by response headers', 'error')
            pass
        self.showListBuilder(trakt_list)
        tools.closeDirectory('tvshows')

    def showsPixelHunter(self):
        trakt_list = trakt.json_response('users/pixelhunterprime/lists/netflix/items/show?extended=full', limit=False)
        if trakt_list is None:
            return
        try:
            sort_by = trakt.response_headers['X-Sort-By']
            sort_how = trakt.response_headers['X-Sort-How']
            trakt_list = trakt.sort_list(sort_by, sort_how, trakt_list, 'show')
        except:
            tools.log('Failed to sort trakt list by response headers', 'error')
            pass
        self.showListBuilder(trakt_list)
        tools.closeDirectory('tvshows')


    ######################################################
    # MENU TOOLS
    ######################################################

    def seasonListBuilder(self, show_id, smartPlay=False):

        self.itemList = trakt_database.get_season_list(show_id)

        self.itemList = [x for x in self.itemList if x is not None and 'info' in x]

        self.itemList = sorted(self.itemList, key=lambda k: k['info']['season'])

        if len(self.itemList) == 0:
            tools.log('We received no titles to build a list', 'error')
            return

        hide_specials = False

        if tools.getSetting('general.hideSpecials') == 'true':
            hide_specials = True

        item_list = []

        for item in self.itemList:

            try:
                if hide_specials and int(item['info']['season']) == 0:
                    continue

                action = 'seasonEpisodes'

                args = {'trakt_id': item['showInfo']['ids']['trakt'],
                        'season': item['info']['season'],
                        'item_type': 'season'}

                args = tools.quote(json.dumps(args, sort_keys=True))

                item['trakt_object']['show_id'] = item['showInfo']['ids']['trakt']
                name = item['info']['season_title']

                if not self.is_aired(item['info']) or 'aired' not in item['info']:
                    if tools.getSetting('general.hideUnAired') == 'true':
                        continue
                    name = tools.colorString(name, 'red')
                    name = tools.italic_string(name)
                    item['info']['title'] = name

                item['info'] = tools.clean_air_dates(item['info'])

            except:
                import traceback
                traceback.print_exc()
                continue

            if smartPlay is True:
                return args

            cm = []
            if tools.getSetting('trakt.auth') != '':
                cm.append(('Trakt Manager', 'RunPlugin(%s?action=traktManager&actionArgs=%s)' % (sysaddon, args)))

            if tools.context_addon():
                cm = []

            item_list.append(tools.addDirectoryItem(name, action, item['info'], item['art'], cm=cm, isFolder=True,
                                                    isPlayable=False, actionArgs=args, set_ids=item['ids'],
                                                    bulk_add=True))

        tools.addMenuItems(syshandle, item_list, len(item_list))

    def episodeListBuilder(self, show_id, season_number, smartPlay=False, hide_unaired=False):

        try:
            item_list = []

            self.itemList = trakt_database.get_season_episodes(show_id, season_number)
            self.itemList = [x for x in self.itemList if x is not None and 'info' in x]

            if len(self.itemList) == 0:
                tools.log('We received no titles to build a list', 'error')
                return

            try:
                self.itemList = sorted(self.itemList, key=lambda k: k['info']['episode'])
            except:
                pass

            for item in self.itemList:

                cm = []

                try:

                    if tools.getSetting('smartplay.playlistcreate') == 'true' and smartPlay is False:
                        action = 'smartPlay'
                        playable = False
                    else:
                        playable = True
                        action = 'getSources'

                    args = {'trakt_id': item['showInfo']['ids']['trakt'],
                            'season': item['info']['season'],
                            'episode': item['info']['episode'],
                            'item_type': 'episode'}

                    args = tools.quote(json.dumps(args, sort_keys=True))

                    name = item['info']['title']

                    if not self.is_aired(item['info']):
                        if tools.getSetting('general.hideUnAired') == 'true' or hide_unaired:
                            continue
                        else:
                            name = tools.colorString(name, 'red')
                            name = tools.italic_string(name)
                            item['info']['title'] = name

                    item['info'] = tools.clean_air_dates(item['info'])

                except:
                    import traceback
                    traceback.print_exc()
                    continue
                cm.append((tools.lang(32070),
                           'XBMC.PlayMedia(%s?action=shufflePlay&actionArgs=%s)' % (sysaddon, args)))

                cm.append(('Browse Season',
                           'XBMC.Container.Update(%s?action=seasonEpisodes&actionArgs=%s)' %
                           (sysaddon,
                            tools.quote(json.dumps({'trakt_id': item['showInfo']['ids']['trakt'],
                                                    'season': item['info']['season'],
                                                    'item_type': 'season'})))))

                cm.append((tools.lang(33022),
                           'PlayMedia(%s?action=getSources&seren_reload=true&actionArgs=%s)' % (sysaddon, args)))

                cm.append((tools.lang(32066),
                           'PlayMedia(%s?action=getSources&source_select=true&actionArgs=%s)' % (sysaddon, args)))

                if tools.getSetting('trakt.auth') != '':
                    cm.append(('Trakt Manager', 'RunPlugin(%s?action=traktManager&actionArgs=%s)' % (sysaddon, args)))

                if tools.context_addon():
                    cm = []

                if tools.getSetting('premiumize.enabled') == 'true' and tools.getSetting('premiumize.pin') != '':
                    cm.append((tools.lang(32068),
                               'XBMC.RunPlugin(%s?action=filePicker&actionArgs=%s)' % (sysaddon, args)))

                item_list.append(tools.addDirectoryItem(name, action, item['info'], item['art'], isFolder=False,
                                                        isPlayable=playable, actionArgs=args, bulk_add=True,
                                                        set_ids=item['ids'], cm=cm))

            if smartPlay is True:
                return item_list
            else:
                tools.addMenuItems(syshandle, item_list, len(item_list))

        except:
            import traceback
            traceback.print_exc()

    def mixedEpisodeBuilder(self, trakt_list, sort=None, hide_watched=False, smartPlay=False, hide_unaired=True,
                            prepend_date=False):

        self.threadList = []

        try:
            if len(trakt_list) == 0:
                tools.log('We received no titles to build a list', 'error')
                return

            self.itemList = trakt_database.get_episode_list(trakt_list)

            self.itemList = [x for x in self.itemList if x is not None and 'info' in x]
            self.itemList = [i for i in self.itemList if 'info' in i and i['info'].get('premiered', None) is not None]
            if sort is None:
                self.itemList = sorted(self.itemList,
                                       key=lambda i: tools.datetime_workaround(i['info']['premiered'],
                                                                               tools.trakt_gmt_format, False),
                                       reverse=True)
            elif sort is not False:
                sort_list = []
                for trakt_id in sort['id_list']:
                    try:
                        if not sort['type']:
                            item = [i for i in self.itemList if i['ids']['trakt'] == trakt_id][0]
                        else:
                            item = [i for i in self.itemList if i[sort['type']]['ids']['trakt'] == trakt_id][0]
                        sort_list.append(item)
                    except IndexError:
                        continue
                    except:
                        import traceback
                        traceback.print_exc()
                self.itemList = sort_list

            item_list = []

            for item in self.itemList:
                if item is None:
                    continue

                if item['info'].get('title', '') == '':
                    continue

                if hide_watched and item['info']['playcount'] != 0:
                    continue

                cm = []

                try:
                    name = tools.display_string(item['info']['title'])

                    if not self.is_aired(item['info']) and hide_unaired is True:
                        continue
                    elif not self.is_aired(item['info']):
                        name = tools.colorString(name, 'red')
                        name = tools.italic_string(name)
                        item['info']['title'] = name

                    item['info'] = tools.clean_air_dates(item['info'])

                    args = {'trakt_id': item['showInfo']['ids']['trakt'],
                            'season': item['info']['season'],
                            'episode': item['info']['episode'],
                            'item_type': 'episode'}

                    args = tools.quote(json.dumps(args, sort_keys=True))

                    if tools.getSetting('smartplay.playlistcreate') == 'true' and smartPlay is False:
                        action = 'smartPlay'
                        playable = False
                    else:
                        playable = True
                        action = 'getSources'

                    if self.title_appends == 'true':
                        name = "%s: %sx%s %s" % (tools.colorString(item['showInfo']['info']['tvshowtitle']),
                                                 tools.display_string(item['info']['season']).zfill(2),
                                                 tools.display_string(item['info']['episode']).zfill(2),
                                                 tools.display_string(item['info']['title']))
                    if prepend_date:
                        release_day = tools.datetime_workaround(item['info']['aired'])
                        release_day = release_day.strftime('%d %b')
                        name = '[%s] %s' % (release_day, name)

                    cm.append((tools.lang(32069),
                               'XBMC.Container.Update(%s?action=showSeasons&actionArgs=%s)' %
                               (sysaddon, tools.quote(json.dumps(str(item['showInfo']))))))

                    cm.append(('Browse Season',
                               'XBMC.Container.Update(%s?action=seasonEpisodes&actionArgs=%s)' %
                               (sysaddon,
                                tools.quote(json.dumps({'trakt_id': item['showInfo']['ids']['trakt'],
                                                        'season': item['info']['season'],
                                                        'item_type': 'season'})))))

                    cm.append((tools.lang(32070),
                               'XBMC.PlayMedia(%s?action=shufflePlay&actionArgs=%s)' % (sysaddon, args)))

                    cm.append((tools.lang(32066),
                               'PlayMedia(%s?action=getSources&source_select=true&actionArgs=%s)' % (sysaddon, args)))

                    cm.append((tools.lang(33022),
                               'PlayMedia(%s?action=getSources&seren_reload=true&actionArgs=%s)' % (sysaddon, args)))

                    if tools.getSetting('trakt.auth') != '':
                        cm.append(('Trakt Manager', 'RunPlugin(%s?action=traktManager&actionArgs=%s)'
                                   % (sysaddon, tools.quote(json.dumps(item['trakt_object'])))))

                    if tools.context_addon():
                        cm = []

                    if tools.getSetting('premiumize.enabled') == 'true' and tools.getSetting('premiumize.pin') != '':
                        cm.append((tools.lang(32068),
                                   'XBMC.RunPlugin(%s?action=filePicker&actionArgs=%s)' % (sysaddon, args)))

                    item['info']['title'] = item['info']['originaltitle'] = name

                    item_list.append(tools.addDirectoryItem(name, action, item['info'], item['art'], isFolder=False,
                                                            isPlayable=playable, actionArgs=args, bulk_add=True,
                                                            set_ids=item['ids'], cm=cm))


                except:
                    import traceback
                    traceback.print_exc()
                    continue

            if smartPlay is True:
                return item_list
            else:
                tools.addMenuItems(syshandle, item_list, len(item_list))

        except:
            import traceback
            traceback.print_exc()

    def showListBuilder(self, trakt_list, forceResume=False, info_only=False):

        try:
            if len(trakt_list) == 0:
                tools.log('We received no titles to build a list', 'error')
                return
        except:
            import traceback
            traceback.print_exc()
            return

        if 'show' in trakt_list[0]:
            trakt_list = [i['show'] for i in trakt_list]

        show_ids = [i['ids']['trakt'] for i in trakt_list]

        self.itemList = trakt_database.get_show_list(show_ids)
        self.itemList = [x for x in self.itemList if x is not None and 'info' in x]
        self.itemList = tools.sort_list_items(self.itemList, trakt_list)

        item_list = []

        for item in self.itemList:
            try:
                # Add Arguments to pass with items
                args = {'trakt_id': item['ids']['trakt'], 'item_type': 'show'}
                args = tools.quote(json.dumps(args, sort_keys=True))

                cm = []

                name = tools.display_string(item['info']['tvshowtitle'])

                if info_only == True:
                    return args

                if not self.is_aired(item['info']):
                    if tools.getSetting('general.hideUnAired') == 'true':
                        continue
                    name = tools.colorString(name, 'red')
                    name = tools.italic_string(name)

                item['info'] = tools.clean_air_dates(item['info'])

                if 'setCast' in item:
                    set_cast = item['setCast']
                else:
                    set_cast = False

                if tools.getSetting('smartplay.clickresume') == 'true' or forceResume is True:
                    action = 'playbackResume'
                else:
                    action = 'showSeasons'

                # Context Menu Items

                cm.append((tools.lang(32070),
                           'XBMC.PlayMedia(%s?action=shufflePlay&actionArgs=%s)' % (sysaddon, args)))

                cm.append((tools.lang(32020),
                           'Container.Update(%s?action=showsRelated&actionArgs=%s)' % (sysaddon, item['ids']['trakt'])))

                cm.append((tools.lang(32069),
                           'XBMC.Container.Update(%s?action=showSeasons&actionArgs=%s)' % (sysaddon, args)))

                if tools.getSetting('trakt.auth') != '':
                    cm.append(('Trakt Manager', 'RunPlugin(%s?action=traktManager&actionArgs=%s)' % (sysaddon, args)))

                cm.append((tools.lang(40153),
                           'XBMC.PlayMedia(%s?action=playFromRandomPoint&actionArgs=%s' % (sysaddon, args)))

                if tools.context_addon():
                    cm = []


            except:
                import traceback
                traceback.print_exc()
                continue

            item_list.append(tools.addDirectoryItem(name, action, item['info'], item['art'], cm=cm, isFolder=True,
                                                    isPlayable=False, actionArgs=args, bulk_add=True, set_cast=set_cast,
                                                    set_ids=item['ids']))

        tools.addMenuItems(syshandle, item_list, len(item_list))

    def runThreads(self, join=True):
        for thread in self.threadList:
            thread.start()

        if join == True:
            for thread in self.threadList:
                thread.join()

    def _start_queue_workers(self):

        self.queue_finished = False

        for i in range(40):
            self.threadList.append(Thread(target=self._queue_worker))

        for i in self.threadList:
            i.start()

    def _finish_queue_workers(self):

        self.queue_finished = True

        for i in self.threadList:
            i.join()

        self.threadList = []

    def _queue_worker(self):
        while not self.task_queue.empty() or not self.queue_finished:
            try:
                target = self.task_queue.get(timeout=3)
            except:
                continue
            try:
                target[0](*target[1])
            except:
                import traceback
                traceback.print_exc()
                pass

    def is_aired(self, info):
        try:
            try:air_date = info['aired']
            except: air_date = info.get('premiered')
            if air_date == '' or air_date is None:
                return False
            if int(air_date[:4]) < 1970:
                return True

            time_format = tools.trakt_gmt_format
            if len(air_date) == 10:
                time_format = '%Y-%m-%d'

            air_date = tools.gmt_to_local(air_date, format=time_format)

            if tools.getSetting('general.datedelay') == 'true':
                air_date = tools.datetime_workaround(air_date, time_format, False)
                air_date += datetime.timedelta(days=1)
            else:
                air_date = tools.datetime_workaround(air_date, time_format, False)

            if air_date > datetime.datetime.now():
                return False
            else:
                return True
        except:
            import traceback
            traceback.print_exc()
            # Assume an item is not aired if we do not have any information on it or fail to identify
            return False
