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
import base64
import os
import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.ext.ndb import Key

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=["jinja2.ext.autoescape"],
    autoescape=True)


class Mensaje (ndb.Model):
    contenido = ndb.StringProperty(required=True)
    autor = ndb.StringProperty(required=True)
    timeStamp = ndb.DateTimeProperty(auto_now_add=True)
    hijos = ndb.StructuredProperty(str, repeated=True)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        messages = Mensaje.query().order(Mensaje.timeStamp);
        template_values = {'messages': messages}
        template = JINJA_ENVIRONMENT.get_template("html/index.html")
        self.response.write(template.render(template_values));


class NuevoMensajeHandler(webapp2.RequestHandler):
    def post(self):
        aux = self.request.get("padre", None)

        if aux is not None:
            aux = Key(urlsafe=aux)
            nuevo_mensaje = Mensaje(parent=aux)
        else:
            nuevo_mensaje = Mensaje()
        nuevo_mensaje.contenido = self.request.get("contenido")
        nuevo_mensaje.autor = self.request.get("autor", "anonimo")
        nuevo_mensaje.put()
        self.redirect("/messageSent")


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/postMessage', NuevoMensajeHandler)
], debug=True)
