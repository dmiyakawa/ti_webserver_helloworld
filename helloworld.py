# -*- coding: utf-8 -*-
import webapp2
from json import dumps
import logging
from google.appengine.ext import ndb

def course_list_key():
    return ndb.Key('CourseList', 'default_course_list')

class Course(ndb.Model):
    date = ndb.DateTimeProperty()
    title = ndb.StringProperty()
    teacher = ndb.StringProperty()
    detail = ndb.StringProperty()

class MainHandler(webapp2.RequestHandler):
    def get(self):
        course_model_list = Course.query(ancestor=course_list_key()).order(Course.date)
        output = self.request.get('output', 'html')
        if output == 'html':
            lst = ['<html><body>']
            lst.append('<h1>講義数合計: {}</h1>'
                       .format(course_model_list.count()))
            lst.append('<ul>')
            for course_model in course_model_list:
                lst.append('<li>{}, {}, {}</li>'
                           .format(course_model.title,
                                   course_model.teacher,
                                   course_model.detail))
            lst.append('</ul>')
            lst.append('<a href="/create">Create</a>')
            lst.append('</body></html>')
            self.response.headers['Content-Type'] = 'text/html; charset=UTF-8'
            for line in lst:
                logging.info(line)
                self.response.write(line)
        else:
            courses = []
            for course_model in course_model_list:
                single_course = {'date': str(course_model.date),
                                 'title': course_model.title,
                                 'teacher': course_model.teacher,
                                 'detail': course_model.detail}
                courses.append(single_course)
            self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
            self.response.write(dumps({'course': courses}, ensure_ascii=False))

app = webapp2.WSGIApplication([
    ("/", MainHandler),
], debug=True)
