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

class MainPage(webapp2.RequestHandler):
    def get(self):
        course_model_list = Course.query(ancestor=course_list_key()).order(Course.date)
        courses = []  # 空のリスト
        for course_model in course_model_list:
            single_course = {'date': str(course_model.date),
                             'title': course_model.title,
                             'teacher': course_model.teacher,
                             'detail': course_model.detail}
            courses.append(single_course)
        self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
        self.response.write(dumps({'course': courses}, ensure_ascii=False))

application = webapp2.WSGIApplication([
    ("/", MainPage),
], debug=True)
