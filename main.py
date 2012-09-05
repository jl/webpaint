#!/usr/bin/env python

# Standard library imports. These come with Python out of the box.
import logging
import random

# App Engine-specific imports.
import webapp2
from google.appengine.ext import db
from webapp2_extras import jinja2

# Imports for our own code.
import util


class Layer(db.Model):
    paint_id = db.StringProperty()
    layer_id = db.StringProperty()
    data_url = db.BlobProperty()
    created = db.DateTimeProperty(auto_now_add=True)


class BaseHandler(webapp2.RequestHandler):
    """Base handler for all web requests.

    Enables access to the jinja templating system.
    """
    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(app=self.app)

    def render_template(self, template, **context):
        self.response.write(self.jinja2.render_template(template, **context))


class MainHandler(BaseHandler):
    def get(self):
        paint_id = util.random_alphanum(6)
        self.render_template('index.html', paint_id=paint_id)


class PaintHandler(BaseHandler):
    def get(self, paint_id):
        logging.info('paint_id is ' + paint_id)
        qry = Layer.all()
        qry.filter('paint_id =', paint_id)
        layers = []
        for layer in qry:
            layers.append(layer)
        self.render_template('paint.html', paint_id=paint_id, layers=layers)


class LayerHandler(BaseHandler):
    def put(self, paint_id, layer_id):
        logging.info('layer put: %s %s %s %d',
            paint_id, layer_id,
            self.request.headers['Content-Type'],
            len(self.request.body))
        data_url = self.request.body
        if not data_url.startswith('data:image/png;base64,'):
            self.error(400)
            return
        layer = Layer(paint_id=paint_id, layer_id=layer_id,
                      data_url=self.request.body)
        layer.put()


# Handler is an array of tuples which maps URLs to request handler classes.
HANDLERS = [
    ('/', MainHandler),
    # The following regular expression only matches paint id's after /p/
    # composed entirely of letters, numbers, dash, or underscore, and with a
    # length between 3 and 100.
    (r'/p/(\w{,50})/', PaintHandler),
    (r'/p/(\w{,50})/layer/([0-9.]{,20})', LayerHandler),
]


# The following global object is expected by the app engine sdk (see app.yaml).
app = webapp2.WSGIApplication(HANDLERS, debug=True)
