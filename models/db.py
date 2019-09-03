# -*- coding: utf-8 -*-

import os, sys
from gluon.contrib.appconfig import AppConfig
from gluon.html import * 
from gluon.http import HTTP 
from gluon.http import redirect 
from gluon.sql import DAL 
from gluon.sql import Field 
from gluon.sql import SQLDB 
from gluon.sqlhtml import SQLFORM 
from gluon.validators import * 
from gluon import fileutils
from gluon.http import *
from gluon.sqlhtml import *
from gluon.tools import fetch
import datetime
from datetime import timedelta
from datetime import date #

configuration = AppConfig()

db = DAL('sqlite://storage.sqlite')

MIGRATE_SETTING = False

db.define_table("admins", 
	Field("administrator"),
	Field("admin_key", "password"),
	migrate = MIGRATE_SETTING
	)
db.define_table("id_refs", 
	Field("classroom_id_ref", default = "0"),
	Field("quiz_id_ref", default = "0"),
	Field("quiz_question_id_ref", default = "0"),
	Field("student_id_ref", default = "0"),
	Field("teacher_id_ref", default = "0"),
	migrate = MIGRATE_SETTING
	)
db.define_table("teachers", 
	Field("teacher_id"),
	Field("name"),
	Field("handle"),
	Field("portal_pswd", "password"),
	migrate = MIGRATE_SETTING
	)
db.define_table("students", 
	Field("student_id"),
	Field("name"),
	Field("handle"),
	Field("portal_pswd", "password"),
	migrate = MIGRATE_SETTING
	)
db.define_table("classrooms", 
	Field("class_id"),
	Field("name"),
	Field("student_id", default = "NONE_ENROLLED"),
	Field("teacher_id"),
	migrate = MIGRATE_SETTING
	)
db.define_table("quiz_contents", 
	Field("quiz_id"),
	Field("question_id"),
	Field("question", "text"),
	Field("option_a"),
	Field("option_b"),
	Field("option_c"),
	Field("option_d"),
	Field("option_e"),
	Field("answer"),
	Field("points"), #for weighing the grade value of a specific question relative to others questions of the SAME quiz
	migrate = MIGRATE_SETTING
	)
db.define_table("quizzes_unassigned", 
	Field("quiz_id"),
	Field("name"),
	Field("teacher_id"),
	migrate = MIGRATE_SETTING
	)
db.define_table("quizzes_assigned", 
	Field("quiz_id"),
	Field("name"),
	Field("teacher_id"),
	Field("class_id"),
	Field("quiz_points"),	#for weighing the grade value of a specific quiz relative to other quizzes
	migrate = MIGRATE_SETTING
	)
db.define_table("quiz_grades", 
	Field("quiz_id"),
	Field("student_id"),
	Field("quiz_points_earned"),
	Field("quiz_points_max"),
	migrate = MIGRATE_SETTING
	)
db.define_table("quizzes_in_progress", 
	Field("quiz_id"),
	Field("student_id"),
	Field("question_id"),
	Field("current_answer", default = "NOT_ANSWERED"),
	migrate = MIGRATE_SETTING
	)
db.define_table("quizzes_submitted", 
	Field("quiz_id"),
	Field("student_id"),
	Field("question_id"),
	Field("submitted_answer", default = "NOT_ANSWERED"),
	migrate = MIGRATE_SETTING
	)
db.define_table("total_grades", 
	Field("student_id"),
	Field("class_id"),
	Field("total_submitted_points_earned", default = "0"),
	Field("total_submitted_points_max", default = "0"),
	Field("cumulative_grade", default = "UNDEFINED"),
	Field("course_status", default = "COURSE_IN_PROGRESS"),
	migrate = MIGRATE_SETTING
	)
	

