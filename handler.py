import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__),'lib'))

import config
import utils
import webapp2
import jinja2
import datetime
import logging
from models import Content
from utils import info
from google.appengine.api import memcache

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