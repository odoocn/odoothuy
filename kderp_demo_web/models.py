# -*- coding: utf-8 -*-
from openerp import models, fields, api
# Storing data
class Teacher(models.Model):
    _name = 'kderp_demo_web.teachers'
    
    name = fields.Char()
    biography = fields.Html()

class Courses(models.Model):
    _name = 'kderp_demo_web.courses'
    
    name = fields.Char()
    teacher_id = fields.Many2one('kderp_demo_web.teachers', string="Teacher")