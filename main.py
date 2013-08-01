# built-in
import datetime
import time
import urllib2
import urllib
import cookielib
import logging
import difflib
import sys
import os
from lxml.html import fromstring
sys.path.append(os.path.join(os.path.dirname(__file__),'lib'))

# internal
import config
import keys
from twitter import TwitterSearch
import utils
from utils import info
import domains
from models import *

# external
import webapp2
import jinja2
from google.appengine.api import memcache
from google.appengine.api import logservice
from google.appengine.ext import deferred
logservice.AUTOFLUSH_ENABLED = True
logservice.AUTOFLUSH_EVERY_SECONDS = 5
logservice.AUTOFLUSH_EVERY_BYTES = None

# global vars
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
							   autoescape = True)

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

	def setLatestContentCache(self):
		''' Sets memcache['latest_content'] with latest DB Content data
		and returns dictionary of Content entity data.'''
		latest = {}

		info('DB QUERY in setLatestContentCache')
		q = Content.gql('ORDER BY created_on DESC LIMIT 1')
		latest = q.get()
		if latest:
			latest = {'data':latest.content,
					  'html':latest.content_html,
					  'html_edit':latest.content_edit}

			memcache.delete('latest_content')
			memcache.set('latest_content',latest,time=config.LASTFETCHEDTIMEOUT)
		return latest

	def getResponse(self, reset_cache=True, q = config.SEARCH):
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
		response = twsearch.search(q,fetch_until=fetch_until,count=config.SEARCHCOUNT)

		# Update memcache
		if response and reset_cache:
			memcache.set('last_status_fetched_id', response.get('statuses')[0].get('id'),time=config.LASTFETCHEDTIMEOUT*2)
			memcache.set('last_status_fetched_on', time.time(),time=config.LASTFETCHEDTIMEOUT*2)

		return (response,memcache.get('last_status_fetched_id'),memcache.get('last_status_fetched_on'),fetch_until)

class MainPage(Handler):
	def get(self):
		# Get latest content
		latest_content = memcache.get('latest_content')
		if not latest_content:
			latest_content = self.setLatestContentCache()

		self.write(latest_content['html'])

app = webapp2.WSGIApplication([('/',MainPage)], debug=True)