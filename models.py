# builtins
import logging
import datetime
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__),'lib'))

# internal
import utils

# external
from google.appengine.ext import db

class Content(db.Model):
	content = db.TextProperty(required = True)
	content_html = db.TextProperty(required = True)
	content_edit = db.TextProperty()
	created_on = db.DateTimeProperty(required = True)

	@classmethod
	def putContent(cls, content):
		''' Take dict content in form of {'data':data,'html':html,'html_edit':...}
		and puts it to db.'''		
		c = Content(content = str(content['data']),
					content_html = content['html'],
					content_edit = content['html_edit'],
					created_on = datetime.datetime.now())
		c.put()

class Stories(db.Model):
	added_on = db.DateTimeProperty(auto_now_add = True)
	title = db.TextProperty(required = True)
	url_full = db.TextProperty(required = True)
	votes = db.IntegerProperty(required = True, indexed=False)
	score = db.FloatProperty()
	blocked = db.BooleanProperty(indexed=False)
	excerpt = db.TextProperty()
	image_url = db.TextProperty()

	@classmethod
	def topStoriesDict(cls, number=250):
		''' Returns dict of top number of stories sorted by score.
		Dict in form of {'story_key_name':{'property':'value',...}}'''
		stories = {}
		
		query = Stories.gql('ORDER BY score DESC LIMIT 250') # getting more than necessary here to avoid some url.fetches
		
		for item in query:
			if item.blocked != True:
				stories[item.key().name()] = {'added_on':item.added_on,
										   'title':item.title, 
										   'url_full':item.url_full,
										   'votes':item.votes,
										   'score':item.score,
										   'blocked':item.blocked,
										   'excerpt':item.excerpt,
										   'image_url':item.image_url}
		return stories

	@classmethod
	def putStories(cls, batch):
		''' Takes a batch of stories {'story_id':{story_dict}} 
		and either updates existing stories or creates new stories.'''		
		to_put = {}

		# Get existing stories, update, and add to to_put
		for cls_item in cls.get_by_key_name(batch.keys()):
			if cls_item:
				''' Something is wrong here, score not being updated for existing stories. '''
				s = cls(key_name = cls_item.key().name(),
							added_on = cls_item.added_on,
							title = cls_item.title,
							url_full = cls_item.url_full,
							votes = batch[cls_item.key().name()]['votes'],
							score = cls.calcScore(batch[cls_item.key().name()]['votes'],utils.hours_ago_from_date(cls_item.added_on)),
							blocked = cls_item.blocked,
							excerpt = cls_item.excerpt,
							image_url = cls_item.image_url)
				to_put[cls_item.key().name()] = s

		# Create new stories and add to to_put
		for k,v in batch.iteritems():
			if k not in to_put and v.get('title'):
				s = cls(key_name = k,
							title = v['title'],
							url_full = v['url_full'],
							votes = v['votes'],
							score = cls.calcScore(v['votes'],0),
							blocked = v['blocked'],
							excerpt = v['excerpt'],
							image_url = v['image_url'])
				to_put[k] = s

		logging.info('about to put %s'% (len(to_put.values())))

		try:
			db.put(to_put.values())
		except:
			e = sys.exc_info()[1]
			logging.error(e)

	@staticmethod
	def calcScore(votes, hour_age, gravity=1.5):
		return votes / pow((hour_age + 2), gravity)

