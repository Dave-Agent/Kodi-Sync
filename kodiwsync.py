__author__ = 'dave'
from kodijsonrpc import Kodi, PLAYER_VIDEO
import socket

def epfind(thelist, title, showtitle):
    for i in range(len(thelist)):
        if (thelist[i]['title'] == title):
            if (thelist[i]['showtitle'] == showtitle):
                if (thelist[i]['playcount'] == 0):
                    return i
    return False

def imdbfind(thelist, imdbid):
    for i in range(len(thelist)):
        if (thelist[i]['imdbnumber'] == imdbid):
            if (thelist[i]['playcount'] == 0):
                return i
    return False

servers = ['http://192.168.1.15:8000/jsonrpc', 'http://192.168.1.7:8080/jsonrpc']

mergeicon = 'http://cdn.mysitemyway.com/etc-mysitemyway/icons/legacy-previews/icons-256/orange-grunge-stickers-icons-signs/094132-orange-grunge-sticker-icon-signs-z-roadsign60.png'
episodeLists = []
movieLists = []
hostnames = []

##########################################################
##  Load hostnames, movies & episodes                   ##
##########################################################
for server in servers:
    print('Loading from:' + server)
    kodi = Kodi(server)
    #hostnames
    ip = server.split('//')[1].split(':')[0]
    try:
        hostname = socket.gethostbyaddr(ip)[0]
    except socket.error:
        hostname = ip
    hostnames.append(hostname)
    #movies
    all_movies = kodi.VideoLibrary.GetMovies({"properties": ["title", "imdbnumber", "playcount"]})
    movieLists.append(all_movies['result']['movies'])
    #episodes
    kodi = Kodi(server)
    all_episodes = kodi.VideoLibrary.GetEpisodes({"properties": ["title", "showtitle", "playcount"]})
    episodeLists.append(all_episodes['result']['episodes'])


##########################################################
##  Sync watched movies                                 ##
##########################################################
for i in range(len(movieLists)):
    for x in range(len(movieLists[i])):
        if (movieLists[i][x]['playcount'] > 0):
            for ii in range(len(movieLists)):
                if (ii != i):
                    destination = movieLists[ii][imdbfind(movieLists[ii], movieLists[i][x]['imdbnumber'])]
                    if (destination):
                        if (movieLists[i][x]['imdbnumber'] == destination['imdbnumber']):
                            print(str(movieLists[i][x]['movieid']) + ' (' + movieLists[i][x][
                                'imdbnumber'] + ') played on ' + hostnames[i] + ' but not ' + str(
                                destination['movieid']) + ' on ' + hostnames[ii] + '')
                            kodi = Kodi(servers[ii])
                            kodi.VideoLibrary.SetMovieDetails({"movieid": destination['movieid'], "playcount": 1})
                            kodi.GUI.ShowNotification(
                                {"title": "Movie Sync:", "message": destination['title'],
                                 "image": mergeicon})

##########################################################
##  Sync watched tv espisodes                           ##
##########################################################
for i in range(len(episodeLists)):
    for x in range(len(episodeLists[i])):
        if (episodeLists[i][x]['playcount'] > 0):
            for ii in range(len(episodeLists)):
                if (ii != i):
                    destinationIndex = epfind(episodeLists[ii], episodeLists[i][x]['title'], episodeLists[i][x]['showtitle'])
                    if (destinationIndex):
                        destination = episodeLists[ii][destinationIndex]
                        print(episodeLists[i][x]['showtitle'] + ' - ' + episodeLists[i][x]['title'] + ': ' + str(
                            episodeLists[i][x]['episodeid']) + ' played on ' + hostnames[i] + ' but not ' + str(
                            destination['episodeid']) + ' on ' + hostnames[ii])
                        kodi = Kodi(servers[ii])
                        kodi.VideoLibrary.SetEpisodeDetails({"episodeid": destination['episodeid'], "playcount": 1})
                        kodi.GUI.ShowNotification({"title": "Episode Sync:",
                                                   "message": destination['showtitle'] + " - " + destination[
                                                       'title'], "image": mergeicon})

