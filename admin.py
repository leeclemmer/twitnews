from models import *
from handler import *
from main import refreshPage
from google.appengine.ext import deferred

title = config.TITLE

def str_to_class(s):
	''' Return a class with name s. '''
	return getattr(sys.modules[__name__], s)

class AdminMain(Handler):
	def get(self):
		self.render('admin_main.html',title=title)
	pass

class AdminRefresh(Handler):
	def get(self):
		''' Adds refreshPage function in main.py to task queue. '''
		status = ''
		if  self.request.get('refresh'):			
			deferred.defer(refreshPage)
			status = 'Page refresh task added'
		self.render('admin_refresh.html',title=title,status=status)

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

		self.render('admin_edit_post.html',title=title,status='Items updated. Frontpage being refreshed.',items=items)


class AdminUpdate(Handler):
	pass

class AdminLookup(Handler):
	def get(self):
		kind = self.request.get('kind')
		keyname = self.request.get('keyname')
		if kind and keyname:
			kind = str_to_class(kind)
			kind_ent = kind.get_by_key_name(keyname)
			obj = []
			obj.append(['keyname',keyname])
			for prop in kind_ent.properties():
				obj.append([prop,getattr(kind_ent,prop)])
			obj[1:] = sorted([o for o in obj[1:]],key = lambda x: x[0])

			self.render('admin_lookup.html',title=title,obj=obj)
		else:
			self.render('admin_lookup.html',title=title)
	pass

class AdminStream(Handler):
	pass

class AdminDebug(Handler):
	pass

app = webapp2.WSGIApplication([('/admin/?',AdminMain),
							   ('/admin/refresh',AdminRefresh),
							   ('/admin/edit',AdminEdit),
							   ('/admin/update',AdminUpdate),
							   ('/admin/lookup',AdminLookup),
							   ('/admin/stream',AdminStream),
							   ('/admindebug',AdminDebug)], debug=True)

