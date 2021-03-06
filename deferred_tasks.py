from main import *
from lxml.html.clean import Cleaner

''' Herein we find all the functions that are called through deferred.defer
	Currently the two primary functions being called are refreshPage and 
	urlFetch. '''

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
		                   'blocked':None,
		                   'excerpt':'',
		                   'image_url':''}

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
			top_links[tl]['members'] = sort_links(members, sortby = 'votes')

	info("top_links", top_links)
	top_links = sort_links(top_links)
	top_links = top_links[:config.NUMHEADLINES]

	latest = {'data':top_links,
			  'html':render_str('index2.html',top_links=top_links,title=config.TITLE,stylesheet=config.STYLESHEET),
			  'html_edit':render_str('admin_edit.html',top_links=top_links,title=config.TITLE + ' Edit', active = 'edit')}
	# Put to DB
	Content.putContent(latest)

	# Set memcache
	memcache.set('latest_content',latest,time=360)

def sort_links(l, sortby = 'score'):
	''' Takes list of links l in form of {'id':{key:value,...},...}
	and returns a sorted list in form of [[id,[prop,val]],[id,...],...].
	Also adds domain attribute.'''
	# Sort links
	l = [[k,v] for k,v in l.items()]
	if sortby == 'votes':
		l = sorted(l, key=lambda x: x[1]['votes'],reverse=True)
	else:
		l = sorted(l, key=lambda x: x[1]['score'],reverse=True)		
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

def render_str(template, **params):
	t = jinja_env.get_template(template)
	return t.render(params)

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
				# Values to create the new story entry with
				url_full = new_url_story['url_full']
				excerpt = new_url_story['excerpt']
				image_url = new_url_story['image_url']
				domain = utils.domain(url_full)

				# title is run through the splitter to remove website name
				title = utils.remove_non_ascii(utils.split_by(new_url_story['title'],domain,domains.TITLESPLITMAPPING,domains.SPLITTYPES))

				# story id is md5 hash of domain and title
				story_id = utils.md5_str(domain,title)

				if to_put.get(story_id): # story already in batch
					ex_links += 1
					# Should only occur rarely (eg. cold cache)
					to_put[story_id]['votes'] += 1
				elif not to_put.get(story_id):
					new_links += 1
					to_put[story_id] = {'title':title, 
									     'url_full':url_full,
									     'votes':1,
									     'score':0,
									     'blocked':None if validUrl(new_url_story) else True,
									     'excerpt':excerpt,
									     'image_url':image_url}
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
	cj = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	
	try:
		c = opener.open(request, timeout=30)
		response =c.read()

		if response:
			url_full = c.geturl()
			code = c.getcode()
			title,excerpt,image_url = getExcerpt(response)
			info('title',title)
			info('excerpt',excerpt)
			info('image_url',image_url)
			return {'code':code, 
					'url_full':url_full, 
					'title':title,
					'excerpt':excerpt,
					'image_url':image_url}
		else: 
			logging.error('urlFetch: No response.')
			return {'code':404,'url_full':'','title':'','excerpt':'','image_url':''}
	except:
		utils.catch_exception()
		return {'code':404,'url_full':'','title':'','excerpt':'','image_url':''}

def getExcerpt(url_response):
	''' Takes url_response and attempts to find and return a title, excerpt, and image. 
	Code a combination from http://bit.ly/11xofXZ and http://bit.ly/23pdRS '''
	doc = fromstring(url_response)

	cleaner = Cleaner(meta = False, 
					  safe_attrs_only = False,
					  page_structure = False,
					  remove_tags=['h1','h2','h3','h4','h5','h6'])

	doc = cleaner.clean_html(doc)

	title = ''
	description = ''
	image_url = ''

	# Title
	try: # <meta> og:title: (http://ogp.me/ for more)
		path = '/html/head/meta[@content][@property="og:title"]'
		title = doc.xpath(path)[0].get('content')
	except IndexError:
		pass

	if not title:
		try: # <title> tag
			path = '/html/head/title'
			title = doc.xpath(path)[0].text_content().strip()
		except IndexError:
			pass
	
	# Description
	try: # <meta> og:description
		path = '/html/head/meta[@content][@property="og:description"]'
		description = doc.xpath(path)[0].get('content')
	except IndexError:
		pass

	if not description:
		try: # <meta> description
			path = '/html/head/meta[@content][@name="description"]'
			description = doc.xpath(path)[0].get('content')
			# some dumbasses are including HTML tags in the description, so...
			description = re.sub('<[^>]+?>','',description)
		except IndexError:
			pass

	if not description:
		# Drop the <head>
		doc.head.drop_tree()

		# Parse page doc text into list, split by newlines
		text_list = [t.strip() for t in doc.text_content().split('\n')]

		# Pick out longest text string
		description = max((len(t),t) for t in text_list)[1].strip()
		info('description', description)
	
	description = excerpt(description)

	# Image URL
	try: # <meta> og:image
		path = '/html/head/meta[@content][@property="og:image"]'
		image_url = doc.xpath(path)[0].get('content')
	except IndexError:
		pass

	return (title, description, image_url)

def excerpt(s, length = 255, ellipses = False):
	''' Will take string s and return the first length characters + any till next punctuation if ellipses = False. '''
	if not ellipses and len(s) > length:
		punctuation = '!.?'
		for c in s[length:]:
			if c in punctuation:
				i = s[length:].index(c)
				return '%s%s' % (s[:length],s[length:][:i+1])
				break
		return s[:length]
	elif len(s) <= length:
		return s
	elif ellipses:
		if s.endswith('...'): return s[:length]
		else: return '%s...' % (s[:length],)


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