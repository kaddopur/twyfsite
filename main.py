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
import webapp2
import jinja2
import os
import logging
import json

from google.appengine.ext import db

class Photo(db.Model):
  image = db.BlobProperty()
  date = db.DateTimeProperty(auto_now_add=True)

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainHandler(webapp2.RequestHandler):
  def get(self):
    template_values = {}
    template = jinja_environment.get_template('index.html')
    self.response.out.write(template.render(template_values))

class TYYC13Handler(webapp2.RequestHandler):
  def get(self):
    template_values = {}
    template = jinja_environment.get_template('2013tyyc_index.html')
    self.response.out.write(template.render(template_values))

class TYYC13PhotoHandler(webapp2.RequestHandler):
  def get(self):
    photo_id = self.request.get('photo_id')
    photo = db.get(photo_id)
    if photo.image:
      self.response.headers['Content-Type'] = 'image'
      self.response.out.write(photo.image)
    else:
      self.response.out.write('no image')

class TYYC13PhotoJsonHandler(webapp2.RequestHandler):
  def get(self):
    photos = Photo.all().order('-date')
    urls = []
    url_base = os.environ['HTTP_HOST'] 
    logging.error(url_base)
    for p in photos:
      urls.append("http://%s/tyyc13/photo?photo_id=%s" % (url_base, p.key()))
    self.response.headers['Content-Type'] = 'application/json'
    self.response.out.write(json.dumps(urls))


class TYYC13PhotoUploadHandler(webapp2.RequestHandler):
  def post(self):
    for image_file in self.request.get_all('files'):
      photo = Photo()
      photo.image = db.Blob(image_file)
      photo.put()
    self.redirect('/tyyc13/photo/uploader')


class TYYC13PhotoUploaderHandler(webapp2.RequestHandler):
  def get(self):
    logging.error(self.request.get_all('files'))
    template_values = {}
    template = jinja_environment.get_template('tyyc13_photo_uploader.html')
    self.response.out.write(template.render(template_values))


app = webapp2.WSGIApplication([('/', TYYC13Handler),
                               ('/tyyc13/', TYYC13Handler),
                               ('/tyyc13/photo', TYYC13PhotoHandler),
                               ('/tyyc13/photo/json', TYYC13PhotoJsonHandler),
                               ('/tyyc13/photo/upload', TYYC13PhotoUploadHandler),
                               ('/tyyc13/photo/uploader', TYYC13PhotoUploaderHandler)],
                              debug=True)
