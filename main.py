#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import cgi
import webapp2
import random
import os
from google.appengine.ext.webapp import template
import datetime
#import urllib
from google.appengine.ext import db
from google.appengine.ext import webapp
#from google.appengine.ext.webapp.util import run_wsgi_app
import logging
import re

# Define Model
class Post(db.Model):
    english = db.StringProperty(multiline=True)
    nick_name = db.StringProperty(multiline=False)
    url_key = db.IntegerProperty()
    touched = db.IntegerProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    ip_address = db.StringProperty(multiline=False)
    lol = db.IntegerProperty()
    rofl = db.IntegerProperty()
    meh = db.IntegerProperty()
    dislike = db.IntegerProperty()


# ---------------------------------------------------------------------
# Contact function
# ---------------------------------------------------------------------
class ContactPage(webapp2.RequestHandler):
	def get(self):	
		path = os.path.join(os.path.dirname(__file__), 'contact.html')
		self.response.out.write(template.render(path, {}))
		
# ---------------------------------------------------------------------
# Landing function
# ---------------------------------------------------------------------
class MainPage(webapp2.RequestHandler):
	def get(self,urlKey):	
		
		if(urlKey == 'rofl'):
			orderBy = '-rofl'
		elif(urlKey == 'lol'):
			orderBy = '-lol'
		elif(urlKey == 'meh'):
			orderBy = '-meh'
		elif(urlKey == 'dislike'):
			orderBy = '-dislike'
		elif(urlKey == 'popular'):
			orderBy = '-lol'					
		else:
			orderBy = '-date'
		
		posts = Post.all().order(orderBy)
		templateValues = {'placeholder':'Why did you defriend them?','posts':posts}
		path = os.path.join(os.path.dirname(__file__), 'main.html')
		self.response.out.write(template.render(path, templateValues))

	def post(self,urlKey):
		logging.info('main GET called')

# ---------------------------------------------------------------------
# Submit function
# ---------------------------------------------------------------------
class SubmitPage(webapp2.RequestHandler):
	def get(self):	
		logging.info('submit GET called')

	def post(self):
		logging.info('submit POST called')

		createPost(self.request.get('phrase'),self.request.get('nickname'),self.request.remote_addr)
	#	translation = Post.get_by_id(newUrlKey)
		posts = Post.all()

# ---------------------------------------------------------------------
# Permalink function
# ---------------------------------------------------------------------
class SpecificPage(webapp2.RequestHandler):
	def get(self,urlKey):	
		# pulling in the urlKey has a '/' prefix
		match = re.search(r'\/(.*)', urlKey)
		key = match.group(1) 
		post = db.get(key)
		
		templateValues = {'post':post,'key':key}
		path = os.path.join(os.path.dirname(__file__), 'specific.html')
		self.response.out.write(template.render(path, templateValues))

# ---------------------------------------------------------------------
# Vote function
# ---------------------------------------------------------------------
class UpvotePage(webapp2.RequestHandler):
	def post(self):	

		elementId = cgi.escape(self.request.get('elementId'))
		match = re.search(r'(lol|rofl|dislike|meh)\-(.*)', elementId)
		vote = match.group(1) 
		key = match.group(2) 
		
		# if vote != lol or rofl or dislike, log an erro
		if(vote != 'lol' and vote != 'rofl' and vote != 'dislike' and vote != 'meh'):
			logging.error('vote-key REGEX FAILED')
			logging.error('vote = '+vote)
			logging.error('key = '+key)
		
		elif(vote == 'lol'):
			post = db.get(key)
			lol = post.lol
			lol = lol + 1
			post.lol = lol
			post.put()
		elif(vote == 'rofl'):
			post = db.get(key)
			rofl = post.rofl
			rofl = rofl + 1
			post.rofl = rofl
			post.put()
		elif(vote == 'meh'):
			post = db.get(key)
			meh = post.meh
			meh = meh + 1
			post.meh = meh
			post.put()				
		elif(vote == 'dislike'):
			post = db.get(key)
			dislike = post.dislike
			dislike = dislike + 1
			post.dislike = dislike
			post.put()			
		

# ---------------------------------------------------------------------

app = webapp2.WSGIApplication([
								('/submit', SubmitPage),
								('/contact', ContactPage),
								('/upvote', UpvotePage),
								('/specifically(.*)', SpecificPage),
							  	('/(.*)', MainPage)],
                              	debug=False)

# ---------------------------------------------------------------------

def createPost(userInput,userName,ip):
	if not userName:
		userName = "Anonymous"

	newPost = Post(
		english = userInput, 
		nick_name = userName, 
		ip_address = ip,
		lol=0,
		rofl=0,
		dislike=0,
		meh=0
	).put()
	
	#newCorrectUrlKey = int(newPost.key().id())
	#return newCorrectUrlKey




