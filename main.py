import handler
import utils
import config
import keys
import domains
from utils import info
from models import *
from twitter import TwitterSearch

import webapp2
import datetime
import os
import sys
import jinja2
import time
import urllib
import urllib2
import hashlib
import logging
import zlib
import difflib
from google.appengine.api import memcache
from lxml.html import fromstring
from google.appengine.api import logservice
from google.appengine.ext import deferred
logservice.AUTOFLUSH_ENABLED = True
logservice.AUTOFLUSH_EVERY_SECONDS = 5
logservice.AUTOFLUSH_EVERY_BYTES = None

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
							   autoescape = True)

sys.path.append(os.path.join(os.path.dirname(__file__),'lib'))

def test(s):
	info('s',s)

def urlFetch(urls):
	info('Starting urlFetch, number of urls to process',len(urls))
	to_put = Stories.topStoriesDict()
	new_links = 0
	ex_links = 0

	# Parse each URL in status
	for url in urls:
		# Init var
		title = None

		# See if we have stories already; if not, add it to stories batch
		if not memcache.get(url):
			new_url_story = goFetch(url)
			if new_url_story['code'] == 200: # only add successful URLs to stories
				url_full = new_url_story['url_full']
				domain = utils.domain(url_full)
				title = utils.remove_non_ascii(utils.split_by(new_url_story['title'],domain,domains.TITLESPLITMAPPING,domains.SPLITTYPES))
				story_id = utils.md5_str(domain,title)
				if to_put.get(story_id):
					ex_links += 1
					# Should only occur rarely (eg. cold cache)
					to_put[story_id]['votes'] += 1
				elif not to_put.get(story_id):
					new_links += 1
					to_put[story_id] = {'title':title, 
									     'url_full':url_full,
									     'votes':1,
									     'score':0,
									     'blocked':None if validUrl(new_url_story) else True}
				memcache.set(url,story_id)
			else:
				info('Bad URL',url)
		elif memcache.get(url):
			ex_links += 1
			key = memcache.get(url)
			if not to_put.get(key):
				if Stories.get_by_key_name(key):
					to_put[key] = {'votes':Stories.get_by_key_name(key).votes}
				else:
					# Shouldn't really happen since url was in memcache
					to_put[key] = {'votes':1}
			else:
				to_put[key]['votes'] += 1

	info('New links',new_links)
	info('Existing links',ex_links)
	info('to_put length',len(to_put))
		
	# Put to DB
	Stories.putStories(to_put)

def goFetch(url):
	headers = {'User-Agent': 'lee clemmer - twitter: @leeclemmer | email: clemmerl@gmail.com'}
	request = urllib2.Request(url,headers=headers)
	title = ''

	try:
		c = urllib2.urlopen(request, timeout=30)
		response = c.read()

		if response:
			url_full = c.geturl()
			code = c.getcode()
			try:
				doc = fromstring(response)
				title = doc.xpath('/html/head/title')[0].text_content().strip()
			except:
				utils.catch_exception()
			return {'code':code, 'url_full':url_full, 'title':title}
		else: 
			logging.error('urlFetch: No response.')
			return {'code':404,'url_full':'','title':''}
	except:
		utils.catch_exception()
		return {'code':404,'url_full':'','title':''}

def validUrl(urlo):
	'''Takes a goFetch result and returns True if it passes the tests.'''
	url = urlo['url_full']
	title = urlo['title']

	# Check Title
	if not title or title == 'None': return False
	if not utils.listNotInString(title,config.WORDSTOEXCLUDE): return False
	if not utils.listInString(title,config.WORDSTOINCLUDE): return False
	
	# Check if it's a pure domain URL
	url = url.split('://')
	if len(url) < 2: return False
	url = url[1]
	if url.find('/') == len(url) - 1: return False # Pure domain url

	return True

def refreshPage():
	info('Frontpage refreshed')

	top_links = Stories.topStoriesDict()

	titles = [(k,v['title']) for k,v in top_links.iteritems()]
	e, eht = edges(titles,config.SIMILARITY)
	c, cht = clusters(e,eht)

	for cid, cluster in c.iteritems():
		# Create a new place in top_links for the new cluster
		# The new cluster will look almost like a regular story
		# object, except have sub-stories as 'members'
		tlid = 'cid_%s' % (cid,)
		top_links[tlid] = {'members':cluster,
		                   'title':tlid,
		                   'added_on':0,
		                   'votes':0,
		                   'score':0,
		                   'blocked':None}

		# Members are currently (id,title) tuples. Let's grab the 
		# story object from top_links and put it under 'members'
		top_links[tlid]['members'][:] = [{member[0]:top_links[member[0]]} for member in top_links[tlid]['members']]
		for k in top_links[tlid]['members']:
			del top_links[k.keys()[0]]

		# Update votes, date, and score of each cluster
		votes = []
		dates = []
		score = 0

		for member in top_links[tlid]['members']:
			for properties in member.values():
				votes.append(properties['votes'])
				dates.append(properties['added_on'])

		top_links[tlid]['votes'] = utils.average(votes)
		top_links[tlid]['added_on'] = utils.avg_date(dates)
		top_links[tlid]['score'] = Stories.calcScore(top_links[tlid]['votes'],
													 utils.hours_ago_from_date(top_links[tlid]['added_on']))

	# Sort member lists > Can probably do better
	for tl,vals in top_links.iteritems():
		if 'cid_' in tl:
			members = {}
			for member in top_links[tl]['members']:
				members.update(member)
			top_links[tl]['members'] = sort_links(members)
	top_links = sort_links(top_links)

	latest = {'data':top_links,
			  'html':render_str('index.html',top_links=top_links,title=config.TITLE,stylesheet=config.STYLESHEET),
			  'html_edit':render_str('admin_edit.html',top_links=top_links,title=config.TITLE)}
	# Put to DB
	Content.putContent(latest)

	# Set memcache
	memcache.set('latest_content',latest,time=360)

def sort_links(l):
	''' Takes list of links l in form of {'id':{key:value,...},...}
	and returns a sorted list in form of [[id,[prop,val]],[id,...],...].
	Also adds domain attribute.'''
	# Sort links
	l = [[k,v] for k,v in l.items()]
	l = sorted(l, key=lambda x: x[1]['score'],reverse=True)
	l = l[:config.NUMHEADLINES]
	for i in l:
		if i[1].get('url_full'): i[1]['domain'] = utils.domain(i[1]['url_full'])
		else: i[1]['domain'] = ''
	return l


def similarity(a,b):
	''' Returns how similar strings a and b are, between 0 and 1. '''
	return difflib.SequenceMatcher(None,a.lower(),b.lower()).ratio()

def edges(l,t=0):
	''' Returns a sorted list of tuple pairs and their similarity in the form of [[(aid,a),(bid,b),s],...],
	as well as a hashtable of in the form of {((aid,a),(bid,b)):s,...}. 
	If threshhold t is given, it will only return edges where similarity is > t'''
	# Init return values
	edges = []
	edges_ht = {}

	for tuple_a in l:
		a = tuple_a[1]
		a_i = l.index(tuple_a)
		for tuple_b in l[a_i + 1:]: # prevent looking up (a,b) and (b,a)
			b = tuple_b[1]
			b_i = l.index(tuple_b)
			sab = similarity(a, b)
			if sab >= t:
				edges.append([tuple_a, tuple_b, sab])
				edges_ht[(tuple_a,tuple_b)] = edges_ht[(tuple_b,tuple_a)] = sab

	edges = sorted(edges, key=lambda x: x[2], reverse = True)

	return (edges,edges_ht)

def clusters(e,eht,t=0):
	''' Returns a list of clusters in the form of {cid:[(aid,a),(bid,b),...)]}
	where cid = cluster id, aid is the id of a, which is the string.
	Also returns a hash table in the form of {(aid,a):cid,...}
	Take a matching list and hash table of edges, as well as 
	threshold t as a minimum similarity.'''
	# Init return val
	clusters = {}
	clusters_ht = {}
	cid = 0

	for edge in e:
		a = edge[0] # first point
		b = edge[1] # second point
		s = edge[2] # similarity of (a,b)

		if s >= t:
			caid = clusters_ht.get(a)
			cbid = clusters_ht.get(b)

			# 1. a or b is already part of a cluster; add a and b to cluster
			if caid or cbid:
				cid = caid and caid or cbid

			# 2. Neither a nor b is part of a cluster (and there are clusters already); 
			#    Check a and b against existing cluster members, and add to cluster it's most similar to
			if not caid and not cbid and clusters_ht:
				similar = False
				'''a_clusters = {}
				b_clusters = {}'''

				for xid, clid in clusters_ht.iteritems():
					'''# Init the cluster similarity collections for a and b
					if not a_clusters.get(clid): a_clusters[clid] = []
					if not b_clusters.get(clid): b_clusters[clid] = []

					# As we're iterating over the clusters, we're collecting lists of similarity
					a_clusters[clid].append(eht.get((caid,xid)))
					b_clusters[clid].append(eht.get((caid,xid)))

					# Now we're collapsing each similarity list into an average similarity per cluster
					a_clusters = avg_dol(a_clusters)
					b_clusters = avg_dol(b_clusters)

					for clid in b_clusters:
						b_clusters[clid] = average(b_clusters[clid])

					# Now let's sort them by their averages and take the top one
					a_clusters = sorted(a_clusters, reverse=True)[0]
					b_clusters = sorted(b_clusters, reverse=True)[0]'''


					if eht.get((caid,xid)) >= t or eht.get((cbid,xid)) >= t:
						cid = clid
						similar = True
				if not similar:
					# 3. a and b aren't part of any cluster and have no similarity to any cluster members;
					#    Add to new cluster
					cid = len(set(clusters_ht.values()))
			
			clusters_ht[a] = clusters_ht[b] = cid

	for xid, cid in clusters_ht.iteritems():
		if not clusters.get(cid): clusters[cid] = []
		clusters[cid].append(xid)

	return (clusters, clusters_ht)

def write(*a, **kw):
	self.response.out.write(*a, **kw)

def render_str(template, **params):
	t = jinja_env.get_template(template)
	return t.render(params)

def render(template, **kw):
	self.write(self.render_str(template, **kw))

class MainPage(handler.Handler):
	def get(self):
		# Get latest content
		latest_content = memcache.get('latest_content')
		if not latest_content:
			latest_content = self.setLatestContentCache()

		self.write(latest_content['html'])

	def getResponse(self,reset_cache=True):
		'''
		Handles interaction with Twitter module and manages memcache.
		Returns response JSON or None as well as a tuple with memcache info.
		'''
		# Initialize Twitter Search
		twsearch = TwitterSearch(keys.CONSUMER_KEY, keys.CONSUMER_SECRET)

		# See what and when the last status we fetched was
		fetched_on = memcache.get('last_status_fetched_on')

		# Delete last fetched status ID if it's too old (or doesn't exist) to prevent loading 1000's of statuses
		if (not fetched_on or time.time() - fetched_on > config.LASTFETCHEDTIMEOUT) and reset_cache:
			memcache.delete('last_status_fetched_id')

		# Get results till you hit this guy
		fetch_until = memcache.get('last_status_fetched_id')
		
		# Get JSON response
		response = twsearch.search(config.SEARCH,fetch_until=fetch_until,count=config.SEARCHCOUNT)

		# Update memcache
		if response and reset_cache:
			memcache.set('last_status_fetched_id', response.get('statuses')[0].get('id'),time=config.LASTFETCHEDTIMEOUT*2)
			memcache.set('last_status_fetched_on', time.time(),time=config.LASTFETCHEDTIMEOUT*2)

		return (response,memcache.get('last_status_fetched_id'),memcache.get('last_status_fetched_on'),fetch_until)

class Update(MainPage):
	''' Gets Twitter JSON response and sends batches of URLs
	(in config.MAXNUMOFURLS increments) as task to urlFetch'''
	def get(self):
		output = {'numstatuses':0,
				  'numtasks':0,
				  'numurls':0}
		# So we can check for dupes
		last_id = memcache.get('last_status_fetched_id')

		# Get Twitter data
		response = self.getResponse()
		statuses = []
		status_times = {} # For time ago strs not in response
		
		# Make sure we've got statuses
		if response[0]:
			# Get statuses from Twitter response
			statuses = response[0].get('statuses')
			output['numstatuses'] = len(statuses)
			task_urls = []

			# Parse each status
			for status in statuses:
				if status['id'] > last_id: # Make sure we only parse new statuses	
					# Extract URLs from status
					urls = []
					if status['entities']['urls']:
						urls = status['entities']['urls']
					elif status.get('retweeted_status') and status['retweeted_status']['entities']['urls']:
						urls = status['retweeted_status']['entities']['urls']
					
					if len(urls) > 0:
						task_urls.append(urls[0]['url'])
						output['numurls'] += 1
						if len(task_urls) >= config.MAXNUMOFURLS:
							output['numtasks'] += 1
							self.addTask(task_urls)
							del task_urls[:]
			output['numtasks'] += 1
			self.addTask(task_urls)
			self.render('update.html',statuses=statuses, error='',**output)
		else: 
			self.render('update.html',statuses=[], error='No response mate.',**output)

	def addTask(self, urls):
		info('Creating new task')
		if urls: 
			deferred.defer(urlFetch,urls)
		else: info('urls list was empty')

class Stream(MainPage):
	def get(self):
		response = self.getResponse(reset_cache=False)
		statuses = []
		status_times = {} # For time ago strs not in response
		error = ''

		if response[0]:
			# Let's get some statuses
			statuses = response[0]['statuses']

			# and traverse them
			for status in statuses:
				# are there any urls?
				urls = None
				if status['entities']['urls']: # Check tweet
					urls = status['entities']['urls']
				elif status.get('retweeted_status') and status['retweeted_status']['entities']['urls']: # and retweets
					urls = status['retweeted_status']['entities']['urls']
				
				if urls:
					# Capture time difference
					created = utils.twt_status_time_to_obj(status['created_at'])
					time_ago = datetime.datetime.now() - created
					status_times[status['id']] = utils.time_ago_str(time_ago.total_seconds())

			if len(statuses) > 0 and len(status_times) > 0:
				velocity = '%d' % (len(statuses) / (((datetime.datetime.now() - utils.twt_status_time_to_obj(statuses[-1]['created_at'])).seconds / 60) + 1))
				summary = {'total':len(statuses),
				   	   'oldest':status_times.get(statuses[-1].get('id')),
				   	   'velocity':velocity}
			if response[2]: cache_date_str = utils.time_ago_str(time.time() - response[2])
			else: cache_date_str = ''
			self.render('stream.html',statuses=statuses,status_times=status_times,error=error,summary=summary,cache_info=list(response[1:3])+[cache_date_str])
		else:
			error = 'Looks like there was no response :('
			self.render('stream.html',statuses=statuses,status_times=status_times,error=error,summary='',cache_info='')

class EditFrontpage(MainPage):
	def get(self):
		# Get latest content
		output = '<a href="/">Home</a> | <a href="/edit">Edit</a> | <a href="/update">Update</a> | <a href="/debug">Debug</a><br/><br/>'
		latest_content = memcache.get('latest_content')
		if not latest_content:
			output += 'couldnt get latest_content: %s' % (latest_content,)
			latest_content = self.setLatestContentCache()
		output += '%s' % (latest_content['html_edit'])
		self.write(output)

	def post(self):
		to_put = []
		output = '<a href="/">Home</a> | <a href="/edit">Edit</a> | <a href="/update">Update</a> | <a href="/debug">Debug</a><br/><br/>'
		
		items = {}
		args = self.request.arguments()

		output += '<small>Args:<br/>' + '  -  '.join(self.request.arguments()) + '</small><br/><br/>'
		
		for arg in args:
			arg_id = arg.split('-')[1]
			if not items.get(arg_id): items[arg_id] = {}
			if 'title-' in arg: items[arg_id]['title'] = self.request.get(arg)
			if 'blocked-' in arg: items[arg.split('-')[1]]['blocked'] = self.request.get(arg)
	
		to_put = []
		top_links = {}
		append = False
		stories = Stories.get_by_key_name(items.keys())

		#self.write(items)

		for story in stories:
			sid = story.key().name()
			if items.get(sid) and items[sid].get('title') and items[sid]['title'] != story.title:
				output += '%s<br/>Old title: %s<br/><b>New title: %s</b><br/><br/>' % (sid,story.title,items[sid]['title'])
				story.title = items[sid]['title']
				append = True
			if items.get(sid) and items[sid].get('blocked'):
				output += '%s<br/>"%s" now blocked<br/><br/>' % (sid,story.title)
				story.blocked = True
				append = True
			elif story.blocked and not items[sid].get('blocked'):
				output += '%s<br/>"%s" now unblocked<br/><br/>' % (sid,story.title)
				story.blocked = None
				append = True
			if append: to_put.append(story)
			append = False
			if story.blocked != True:
				top_links[sid] = {'added_on':story.added_on,
							  'title':story.title,
							  'url_full':story.url_full,
							  'votes':story.votes,
							  'score':story.score,
							  'blocked':story.blocked}
		db.put(to_put)

		deferred.defer(refreshPage)
		output += '<br/><b style="color:red">Page refresh task kicked off.</b>'
		self.write(output)

class Debug(MainPage):
	def get(self):
		output = '<a href="/">Home</a> | <a href="/edit">Edit</a> | <a href="/update">Update</a> | <a href="/debug">Debug</a><br/><br/>'
		form = 'Input Key Name of entity to look up <br/><form method="post"><input type="text" name="keyname"/><input type="submit"></form>'
		output += '%s<br/>or<br/>' % (form,)
		form = 'Input Name of entity to look up <br/><form method="post"><input type="text" name="name"/><input type="submit"></form>'
		output += form
		
		'''t1 = 'IBM News room - 2013-07-24 Dublin City University to Introduce Students to Master in Analytics and Big Data with IBM Smarter Cities - United States'
		t2 = 'IBM and DCU create masters degree in big data, analytics and smart cities - Ireland\'s cloud news service - Siliconrepublic.com'
		t3 = 'Techmeme: IBM, Pivotal team up on open governance model for Cloud Foundry (Rachel King/ZDNet)'
		info('t1',utils.split_by(t1,'ibm.com',domains.TITLESPLITMAPPING,domains.SPLITTYPES))
		info('t2',utils.split_by(t2,'siliconrepublic.com',domains.TITLESPLITMAPPING,domains.SPLITTYPES))
		info('t3',utils.split_by(t3,'techmeme.com',domains.TITLESPLITMAPPING,domains.SPLITTYPES))
		'''

		self.write(output)

	def post(self):
		output = '<a href="/">Home</a> | <a href="/edit">Edit</a> | <a href="/update">Update</a> | <a href="/debug">Debug</a><br/><br/>'
		form = 'Input Key Name of entity to look up <br/><form method="post"><input type="text" name="keyname"/><input type="submit"></form>'
		if self.request.get('keyname'):
			m = Stories.get_by_key_name(self.request.get('keyname'))
			if memcache.get('last_status_fetched_on'): last_fetched = datetime.datetime(1970,1,1) + datetime.timedelta(seconds=memcache.get('last_status_fetched_on'))
			else: last_fetched = datetime.datetime.now()
			output += ('''<b>Title = %s</b><br/>
							Key name = %s<br/>
							Last fetched on = %s (%sm ago)<br/>
							Current time = %s<br/>
							Added on = %s (%s hrs ago)<br/>
							Full URL = <a href="%s" target="_blank">%s</a><br/>
							Votes = %s<br/>
							Score = %s<br/>
							Blocked = %s<br/><br/>%s''' 
															% ( m.title,
																m.key().name(),
															   last_fetched,
																(datetime.datetime.now() - last_fetched).seconds/60,
																datetime.datetime.now(),
															   m.added_on,
															   utils.hours_ago_from_date(m.added_on),
															   m.url_full,
															   m.url_full,
															   m.votes,
															   m.score,
															   m.blocked,
															   form))
			output += (''' <form method="post">
								<label>Update title</lable>
								<input type="hidden" name="edit" value="1"/>
								<input type="hidden" name="sid" value="%s"/>
								<input type="text" name="title" value="%s"/>
								<input type="submit"/>
								</form>
								''' % (m.key().name(), m.title))
		elif self.request.get('name'):
			stories = Stories.all().fetch(limit=10000)
			for m in stories:
				if m.title == self.request.get('name'):
					last_fetched = datetime.datetime.now()
					output += ('''<b>Title = %s</b><br/>
							Key name = %s<br/>
							Last fetched on = %s (%sm ago)<br/>
							Current time = %s<br/>
							Added on = %s (%s hrs ago)<br/>
							Full URL = <a href="%s" target="_blank">%s</a><br/>
							Votes = %s<br/>
							Score = %s<br/>
							Blocked = %s<br/><br/>%s''' 
															% ( m.title,
															   m.key().name(),
															   last_fetched,
																(datetime.datetime.now() - last_fetched).seconds/60,
																datetime.datetime.now(),
															   m.added_on,
															   utils.hours_ago_from_date(m.added_on),
															  m.url_full,
															   m.url_full,
															  m.votes,
															   m.score,
															   m.blocked,
															   form))
					output += (''' <form method="post">
								<label>Update title</lable>
								<input type="hidden" name="edit" value="1"/>
								<input type="hidden" name="sid" value="%s"/>
								<input type="text" name="title" value="%s"/>
								<input type="submit"/>
								</form>
								''' % (m.key().name(), m.title))
		elif self.request.get('edit'):
			m = Stories.get_by_key_name(self.request.get('sid'))
			m.title = self.request.get('title')
			m.put()

			last_fetched = datetime.datetime.now()
			output += 'Title updated :)<br/>'
			output += ('''<b>Title = %s</b><br/>
							Key name = %s<br/>
							Last fetched on = %s (%sm ago)<br/>
							Current time = %s<br/>
							Added on = %s (%s hrs ago)<br/>
							Full URL = <a href="%s" target="_blank">%s</a><br/>
							Votes = %s<br/>
							Score = %s<br/>
							Blocked = %s<br/><br/>%s''' 
															% ( m.title,
															   m.key().name(),
															   last_fetched,
																(datetime.datetime.now() - last_fetched).seconds/60,
																datetime.datetime.now(),
															   m.added_on,
															   utils.hours_ago_from_date(m.added_on),
															  m.url_full,
															   m.url_full,
															  m.votes,
															   m.score,
															   m.blocked,
															   form))
			output += (''' <form method="post">
								<label>Update title</lable>
								<input type="hidden" name="edit" value="1"/>
								<input type="hidden" name="sid" value="%s"/>
								<input type="text" name="title" value="%s"/>
								<input type="submit"/>
								</form>
								''' % (m.key().name(), m.title))

		info(output)
		self.write(output)

app = webapp2.WSGIApplication([('/',MainPage),
							   ('/edit',EditFrontpage),
							   ('/update',Update),
							   ('/stream',Stream),
							   ('/debug',Debug)], debug=True)