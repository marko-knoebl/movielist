#!/usr/bin/env python
import os
import jinja2
import webapp2

import models


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        movies = models.Movie.query().fetch()
        return self.render_template(
            "home.html", params={'movies': movies})

class AddHandler(BaseHandler):
    def get(self):
        return self.render_template('add.html')
    def post(self):
        name = self.request.get('name')
        rating = int(self.request.get('rating'))
        image = self.request.get('image')
        movie = models.Movie(name=name, rating=rating, image=image)
        movie.put()
        return self.render_template('add-post.html')

class DeleteHandler(BaseHandler):
    def post(self, movie_id):
        todelete = models.Movie.get_by_id(int(movie_id))
        name = todelete.name
        todelete.key.delete()
        return self.render_template('del-post.html',
                                    params={'name': name})

class EditHandler(BaseHandler):
    def post(self, movie_id):
        toedit = models.Movie.get_by_id(int(movie_id))
        rating = int(self.request.get('rating'))
        toedit.rating = rating
        toedit.put()
        return self.render_template('edit-post.html')

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/add', AddHandler),
    webapp2.Route('/delete/<movie_id:\d+>', DeleteHandler),
    webapp2.Route('/edit/<movie_id:\d+>', EditHandler),
], debug=True)
