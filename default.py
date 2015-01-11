
import xbmc
import xbmcgui
import json

#retrieve all TV Shows
show_request = '{"jsonrpc": "2.0", \
"method": "VideoLibrary.GetTVShows", \
"params": \
	{"properties": ["genre", "title", "playcount", "mpaa", "watchedepisodes", "episode"]}, \
"id": "allTVShows"}'
raw_shows = json.loads(xbmc.executeJSONRPC(show_request))
shows = raw_shows['result']['tvshows']


#retrieve all TV episodes
episode_request = '{"jsonrpc": "2.0", \
"method": "VideoLibrary.GetEpisodes", \
"params": \
	{"properties": ["season","episode","runtime", "resume","playcount", "tvshowid", "lastplayed", "file"]}, \
"id": "allTVEpisodes"}'
raw_eps = json.loads(xbmc.executeJSONRPC(episode_request))
eps = raw_eps['result']['episodes']

all_shows = sorted(shows, key =  lambda shows: (shows['title']))

working_eids = []
ids = [x['tvshowid'] for x in all_shows]


for sid in ids:
	watched_eps = [x for x in eps if x['tvshowid'] == sid and x['playcount'] != 0]
	lpe = sorted(watched_eps, key =  lambda watched_eps: (watched_eps['season'], watched_eps['episode']), reverse=True)
	if lpe:
		last_played_ep = lpe[0]
		Season = last_played_ep['season']
		Episode = last_played_ep['episode']

		#uses the season and episode number to create a list of unwatched shows older than the last watched one
		unplayed_eps = [x['episodeid'] for x in eps if ((x['season'] == Season and x['episode'] < Episode) or (x['season'] < Season)) and x['tvshowid'] == sid]

		for d in unplayed_eps:
			working_eids.append(d)


pDialog = xbmcgui.DialogProgressBG()
pDialog.create('Backfilling watched status Update', 'Running.')

total = float(len(working_eids))

for i, eid in enumerate(working_eids):

	set_to_watched = '{"jsonrpc": "2.0", \
	"method": "VideoLibrary.SetEpisodeDetails", \
	"params": {"episodeid" : %s, "playcount" : 1}, \
	"id": 1}' % d
	xbmc.executeJSONRPC(set_to_watched)

	pct = int(i/total*100)

	msg = '%s / %s episodes' % (i, int(total))

	pDialog.update(percent = pct, message = msg)

pDialog.close()

