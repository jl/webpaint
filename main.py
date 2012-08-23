#!/usr/bin/env python
import logging
import webapp2

from webapp2_extras import jinja2


class BaseHandler(webapp2.RequestHandler):
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


app = webapp2.WSGIApplication([('/', MainHandler),
                               (r'/(\d+)', PaintHandler)],
                              debug=True)
