from main import *
from deferred_tasks import refreshPage, urlFetch

title = config.TITLE

class AdminMain(Handler):
	def get(self):
		self.render('admin_main.html',title=title, active = 'admin')
	pass

class AdminRefresh(Handler):
	def get(self):
		''' Adds refreshPage function in main.py to task queue. '''
		status = ''
		if  self.request.get('refresh'):			
			deferred.defer(refreshPage)
			status = 'Page refresh task added'
		self.render('admin_refresh.html',title=title + ' Refresh',status=status, active = 'refresh')

class AdminEdit(Handler):
	def get(self):
		''' Fetches the most recently generated html_edit (generated in the refreshPage function in main.py) from memcache (or resets memcache if it's cold) and writes it to page. '''
		latest_content = memcache.get('latest_content')
		status = ''
		if not latest_content:
			status = "latest_content was not found; resetting it now."
			latest_content = self.setLatestContentCache()
		content = latest_content['html_edit']
		self.write(content)

	def post(self):
		''' Gets form arguments and then compares them against entities in DB.  If they differ, then the entities get updated with the new values.  Currently only title and blocked can be updated in edit form. '''
		# Init vars
		to_put = []
		items = {}
		append = False

		# Get all form arguments that were passed
		args = self.request.arguments()

		# Go through arguments and created dict of IDs and their args {id:{title:title value,blocked:blocked value}}
		# Args look like this: title-f8c61a991f6f218ac934957cef2327af
		for arg in args:
			arg_id = arg.split('-')[1]
			if not items.get(arg_id): items[arg_id] = {}
			if 'title-' in arg: items[arg_id]['title'] = self.request.get(arg)
			if 'blocked-' in arg: items[arg_id]['blocked'] = self.request.get(arg)

		# Get stories that were named by their ID
		stories = Stories.get_by_key_name(items.keys())

		for story in stories:
			sid = story.key().name()
			if items.get(sid):
				if items[sid].get('title') and items[sid]['title'] != story.title:
					# Titles don't match, i.e. title was changed
					items[sid]['oldtitle'] = story.title
					story.title = items[sid]['title']
					append = True

				if items[sid].get('blocked'):
					# If blocked is there, it's getting 
					story.blocked = True
					append = True
			if append: to_put.append(story)
			else: del items[sid]
			append = False

		db.put(to_put)

		deferred.defer(refreshPage)

		self.render('admin_edit_post.html',title=title + ' Edit',status='Items updated. Frontpage being refreshed.',items=items, active = 'edit')


class AdminUpdate(Handler):	
	''' Gets Twitter JSON response and sends batches of URLs
	(in config.MAXNUMOFURLS increments) as task to urlFetch'''
	def get(self):
		if  self.request.get('update'):	
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
				self.render('admin_update.html',title=title + ' Update',statuses=statuses, status='', active = 'update',**output)
			else: 
				self.render('admin_update.html',title=title + ' Update',statuses=[], status='No response mate.', active = 'update',**output)
		else:
			self.render('admin_update.html',title=title + ' Update', active = 'update')

	def addTask(self, urls):
		info('Creating new task')
		if urls: 
			deferred.defer(urlFetch,urls)
		else: info('urls list was empty')

class AdminLookup(Handler):
	def get(self):
		kind = self.request.get('kind')
		if kind: kind = self.str_to_class(kind)
		keyname = self.request.get('keyname')
		t = self.request.get('title')
		if kind and keyname:
			kind_ent = kind.get_by_key_name(keyname)
			self.render('admin_lookup.html',title=title + ' Lookup',result=[self.get_obj_props(kind_ent)])
		elif kind and t:
			kinds = kind.all().fetch(limit=10000)
			results = []
			for k in kinds:
				if k.title == t:
					results.append(self.get_obj_props(k))
			self.render('admin_lookup.html',title=title + ' Lookup',result=results, active = 'lookup')
		else:
			self.render('admin_lookup.html',title=title + ' Lookup', active = 'lookup')
	
	def get_obj_props(self, ke):
		''' Takes Kind entity (model instance) ke and returns a list of its properties. '''
		obj = []

		if ke:
			# Add keyname as first item
			obj.append(['keyname',ke.key().name()])

			# Add all properties to list
			for prop in ke.properties():
				obj.append([prop,getattr(ke,prop)])

			# Sort list (except keyname) of properties alphabetically
			obj[1:] = sorted([o for o in obj[1:]],key = lambda x: x[0])
		else:
			info('get_obj_props: ke was None')
			obj.append('ke was None')

		return obj

	def str_to_class(self, s):
		''' Return a class with name s. '''
		return getattr(sys.modules[__name__], s)

class AdminStream(Handler):
	def get(self):
		q = self.request.get('q')
		if q: response = self.getResponse(reset_cache=False, q = q)
		else: 
			q = config.SEARCH
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
			self.render('admin_stream.html',title=title + ' Stream',statuses=statuses,status_times=status_times,status=error,summary=summary,cache_info=list(response[1:3])+[cache_date_str], query=q, active = 'stream')
		else:
			error = 'Looks like there was no response :('
			self.render('admin_stream.html',title=title + ' Stream',statuses=statuses,status_times=status_times,status=error,summary='',cache_info='',query=q, active = 'stream')

class AdminDebug(Handler):
	def get(self):
		self.render('admin_debug.html',title=title + ' Debug', active = 'debug')

app = webapp2.WSGIApplication([('/admin/?',AdminMain),
							   ('/admin/refresh',AdminRefresh),
							   ('/admin/edit',AdminEdit),
							   ('/admin/update',AdminUpdate),
							   ('/admin/lookup',AdminLookup),
							   ('/admin/stream',AdminStream),
							   ('/admin/debug',AdminDebug)], debug=True)

