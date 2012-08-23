#!/usr/bin/env python

# Standard library imports. These come with Python out of the box.
import logging

# App Engine-specific imports.
import webapp2
from webapp2_extras import jinja2


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
        self.render_template('index.html')


class PaintHandler(BaseHandler):
    def get(self, paint_id):
        logging.info('paint_id is ' + paint_id)
        self.render_template('paint.html')


# Handler is an array of tuples which maps URLs to request handler classes.
HANDLERS = [
    ('/', MainHandler),
    (r'/(\d+)', PaintHandler),
]


# The following global object is expected by the app engine sdk (see app.yaml).
app = webapp2.WSGIApplication(HANDLERS, debug=True)
