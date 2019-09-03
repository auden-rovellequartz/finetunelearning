# -*- coding: utf-8 -*-

########## <PAGE RENDERING FUNCTIONS - BEGIN> #######################################

def add_student():
	session_manager(request)
	home = get_home_link()
	form = "NO CLASSES AVAILABLE"
	classrooms_rows = db(
		(db.classrooms.id > 0)
		).select(
			db.classrooms.class_id, 
			db.classrooms.name, 
			distinct = True,
			)
	available_classes = [""]
	available_classes_list = []
	current_classes_list = []
	if (len(classrooms_rows) > 0):
		classrooms_rows_01 = db(db.classrooms.student_id == session.student_id).select()
		for x in classrooms_rows_01:
			current_classes_list.append(x.class_id + ": " + x.name)
		for x in classrooms_rows:
			if ((x.class_id + ": " + x.name) not in current_classes_list):
				available_classes.append(x.class_id + ": " + x.name)
				available_classes_list.append(x.class_id + ": " + x.name)
		form = FORM(
			DIV(
				"Pick a Class",
				_style = "padding-left:350px;height:20px;padding-bottom:25px;",
				),
			DIV(
				SELECT(
					available_classes,
					_name = "available_class",
					_style = "width:400px;height:40px;",
					requires = [
						IS_IN_SET(available_classes_list),
						]
					),
				_align = "right",
				_style = "padding-right:400px;height:20px;padding-bottom:70px;",
				),
			DIV(
				INPUT(
					_type = "submit",
					_value = "Enroll in this Class",
					_style = "width:400px",
					),
				_align = "right",
				_style = "padding-right:400px;",
				),
			)
		if (form.process().accepted):
			class_id = form.vars.available_class[:8]
			name = form.vars.available_class[10:]
			classrooms_rows_02 = db(
				(db.classrooms.class_id == class_id)
				&
				(db.classrooms.student_id == "NONE_ENROLLED")
				).select()
			classrooms_rows_03 = db(
				(db.classrooms.class_id == class_id)
				).select(db.classrooms.teacher_id, distinct = True)
			if (len(classrooms_rows_03) == 0):
				system_error("data corruption! - expected class_id no longer found in database")
			else:
				teacher_id = classrooms_rows_03[0].teacher_id
			if (len(classrooms_rows_02) > 1):
				system_error(
					"data corruption! - only up to a maximum of ONE record of "
					+						
					"a specific class_id can have its student_id field set to NONE_ENROLLED"
					)
			else:
				if (len(classrooms_rows_02) == 1):
					classrooms_rows_02[0].update_record(student_id = session.student_id)
					db.commit()
				else:
					db.classrooms.insert(
						class_id = class_id,
						name = name,
						student_id = session.student_id,
						teacher_id = teacher_id,
						)
					db.commit()
				db.total_grades.insert(
					student_id = session.student_id,
					class_id = class_id,
					)
				db.commit()
			quizzes_assigned_rows = db(db.quizzes_assigned.class_id == class_id).select()
			for x in quizzes_assigned_rows:
				quiz_contents_rows = db(db.quiz_contents.quiz_id == x.quiz_id).select()
				for y in quiz_contents_rows:
					db.quizzes_in_progress.insert(
						quiz_id = y.quiz_id,
						student_id = session.student_id,
						question_id = y.question_id,
						)
					db.commit()
			redirect(
				URL(
					a = "school",
					c = "default",
					f = "student_dashboard",
					)
				)
	return dict(
		form = form,
		home = home,
		)
def add_question_to_quiz():
	session_manager(request)
	home = get_home_link()
	form = FORM(
		DIV(
			LABEL(
				session.quiz_under_development,
				_style = "padding-right:25px",
				),
			_align = "right",
			_style = "padding-right:400px;",
			),
		DIV(
			LABEL(
				"Enter Question:",
				_style = "padding-right:25px",
				),
			TEXTAREA(
				_name = "question",
				_style = "width:400px;height:100px",
				requires = IS_NOT_EMPTY(error_message = "enter a question")
				),
			_align = "right",
			_style = "padding-right:400px;",
			),
		DIV(
			LABEL(
				"Specify Points for Question:",
				_style = "padding-right:25px",
				),
			INPUT(
				_type = "text",
				_name = "points",
				_autocomplete = "off",
				_style = "width:400px",
				requires = IS_NOT_EMPTY(error_message = "specify a points value")
				),
			_align = "right",
			_style = "padding-right:400px;",
			),
		DIV(
			LABEL(
				"Specify Option (A):",
				_style = "padding-right:25px",
				),
			INPUT(
				_type = "text",
				_name = "option_a",
				_autocomplete = "off",
				_style = "width:400px",
				requires = IS_NOT_EMPTY(error_message = "specify an option")
				),
			_align = "right",
			_style = "padding-right:400px;",
			),
		DIV(
			LABEL(
				"Specify Option (B):",
				_style = "padding-right:25px",
				),
			INPUT(
				_type = "text",
				_name = "option_b",
				_autocomplete = "off",
				_style = "width:400px",
				requires = IS_NOT_EMPTY(error_message = "specify an option")
				),
			_align = "right",
			_style = "padding-right:400px;",
			),
		DIV(
			LABEL(
				"Specify Option (C):",
				_style = "padding-right:25px",
				),
			INPUT(
				_type = "text",
				_name = "option_c",
				_autocomplete = "off",
				_style = "width:400px",
				requires = IS_NOT_EMPTY(error_message = "specify an option")
				),
			_align = "right",
			_style = "padding-right:400px;",
			),
		DIV(
			LABEL(
				"Specify Option (D):",
				_style = "padding-right:25px",
				),
			INPUT(
				_type = "text",
				_name = "option_d",
				_autocomplete = "off",
				_style = "width:400px",
				requires = IS_NOT_EMPTY(error_message = "specify an option")
				),
			_align = "right",
			_style = "padding-right:400px;",
			),
		DIV(
			LABEL(
				"Specify Option (E):",
				_style = "padding-right:25px",
				),
			INPUT(
				_type = "text",
				_name = "option_e",
				_autocomplete = "off",
				_style = "width:400px",
				requires = IS_NOT_EMPTY(error_message = "specify an option")
				),
			_align = "right",
			_style = "padding-right:400px;",
			),
		DIV(
			LABEL(
				"Specify Correct Option",
				_style = "padding-right:25px",
				),
			SELECT(
				["specify the correct answer", "(A)", "(B)", "(C)", "(D)", "(E)"],
				_name = "answer",
				_style = "width:400px",
				requires = [
					IS_IN_SET(["(A)", "(B)", "(C)", "(D)", "(E)"]),
					]
				),
			_align = "right",
			_style = "padding-right:400px;",
			),
		DIV(
			LABEL(
				"Specify if This is the Last Question",
				_style = "padding-right:25px",
				),
			INPUT(
				_type = "checkbox",
				_name = "the_last_question",
				_style = "width:400px",
				),
			_align = "right",
			_style = "padding-right:400px;",
			),
		DIV(
			INPUT(
				_type = "submit",
				_value = "Add This Question to Quiz",
				_style = "width:400px",
				),
			_align = "right",
			_style = "padding-right:400px;",
			),
		)
	if (form.process().accepted):
		db.quiz_contents.insert(
			quiz_id = session.quiz_under_development,
			question_id = create_id("QUIZ_QUESTION"),
			question = form.vars.question,
			option_a = form.vars.option_a,
			option_b = form.vars.option_b,
			option_c = form.vars.option_c,
			option_d = form.vars.option_d,
			option_e = form.vars.option_e,
			answer = form.vars.answer,
			points = form.vars.points,
			)
		db.commit()
		if (form.vars.the_last_question == "on"):
			session.quiz_under_development = None
		redirect(
			URL(
				a = "school",
				c = "default",
				f= "add_question_to_quiz",
				)
			)
	return dict(
		form = form,
		home = home,
		)
def admin_login():
	session_manager(request)
	home = get_home_link()
	form = FORM(
		DIV(
			LABEL(
				"Your administrator key:",
				_style = "padding-right:25px",
				),
			INPUT(
				_type = "text",
				_name = "admin_key",
				),
			),
		DIV(
			INPUT(
				_type = "submit",
				_value = "Submit",
				),
			),
		)
	if (form.process().accepted):
		admins_rows = db().select(db.admins.ALL)
		for x in admins_rows:
			if (form.vars.admin_key == x.admin_key):
				session.login_type = "ADMINISTRATOR"
				session.portal_user = x.administrator
				redirect(
					URL(
						a = "school",
						c = "default",
						f = "view_admin_dashboard",
						)
					)
		system_error("a correct administrator key was not provided!")
	return dict(
		home = home,
		form = form,
		)
def create_classroom():
	session_manager(request)
	home = get_home_link()
	form = FORM(
		DIV(
			LABEL(
				"Enter Course Name:",
				_style = "padding-right:25px",
				),
			INPUT(
				_type = "text",
				_name = "name",
				_style = "width:400px",
				),
			_align = "right",
			_style = "padding-right:400px;",
			),
		DIV(
			INPUT(
				_type = "submit",
				_value = "Register Course",
				_style = "width:400px",
				),
			_align = "right",
			_style = "padding-right:400px;",
			),
		)
	if (form.process().accepted):
		db.classrooms.insert(
			class_id = create_id("CLASSROOM"),
			name = form.vars.name,
			teacher_id = session.teacher_id,
			)
		db.commit()
	return dict(
		form = form,
		home = home,
		)
def create_quiz():
	session_manager(request)
	home = get_home_link()
	form = FORM(
		DIV(
			LABEL(
				"Enter Quiz Name:",
				_style = "padding-right:25px",
				),
			INPUT(
				_type = "text",
				_name = "name",
				_autocomplete = "off",
				_style = "width:400px",
				requires = IS_NOT_EMPTY("enter a name for this new quiz")
				),
			_align = "right",
			_style = "padding-right:400px;",
			),
		DIV(
			LABEL(
				"Enter Question:",
				_style = "padding-right:25px",
				),
			TEXTAREA(
				_name = "question",
				_style = "width:400px;height:100px",
				requires = IS_NOT_EMPTY(error_message = "enter a question")
				),
			_align = "right",
			_style = "padding-right:400px;",
			),
		DIV(
			LABEL(
				"Specify Points for Question:",
				_style = "padding-right:25px",
				),
			INPUT(
				_type = "text",
				_name = "points",
				_autocomplete = "off",
				_style = "width:400px",
				requires = IS_NOT_EMPTY(error_message = "specify a points value")
				),
			_align = "right",
			_style = "padding-right:400px;",
			),
		DIV(
			LABEL(
				"Specify Option (A):",
				_style = "padding-right:25px",
				),
			INPUT(
				_type = "text",
				_name = "option_a",
				_autocomplete = "off",
				_style = "width:400px",
				requires = IS_NOT_EMPTY(error_message = "specify an option")
				),
			_align = "right",
			_style = "padding-right:400px;",
			),
		DIV(
			LABEL(
				"Specify Option (B):",
				_style = "padding-right:25px",
				),
			INPUT(
				_type = "text",
				_name = "option_b",
				_autocomplete = "off",
				_style = "width:400px",
				requires = IS_NOT_EMPTY(error_message = "specify an option")
				),
			_align = "right",
			_style = "padding-right:400px;",
			),
		DIV(
			LABEL(
				"Specify Option (C):",
				_style = "padding-right:25px",
				),
			INPUT(
				_type = "text",
				_name = "option_c",
				_autocomplete = "off",
				_style = "width:400px",
				requires = IS_NOT_EMPTY(error_message = "specify an option")
				),
			_align = "right",
			_style = "padding-right:400px;",
			),
		DIV(
			LABEL(
				"Specify Option (D):",
				_style = "padding-right:25px",
				),
			INPUT(
				_type = "text",
				_name = "option_d",
				_autocomplete = "off",
				_style = "width:400px",
				requires = IS_NOT_EMPTY(error_message = "specify an option")
				),
			_align = "right",
			_style = "padding-right:400px;",
			),
		DIV(
			LABEL(
				"Specify Option (E):",
				_style = "padding-right:25px",
				),
			INPUT(
				_type = "text",
				_name = "option_e",
				_autocomplete = "off",
				_style = "width:400px",
				requires = IS_NOT_EMPTY(error_message = "specify an option")
				),
			_align = "right",
			_style = "padding-right:400px;",
			),
		DIV(
			LABEL(
				"Specify Correct Option",
				_style = "padding-right:25px",
				),
			SELECT(
				["specify correct answer", "(A)", "(B)", "(C)", "(D)", "(E)"],
				_name = "answer",
				_style = "width:400px",
				requires = [
					IS_IN_SET(["(A)", "(B)", "(C)", "(D)", "(E)"]),
					]
				),
			_align = "right",
			_style = "padding-right:400px;",
			),
		DIV(
			LABEL(
				"Specify if This is the Last Question",
				_style = "padding-right:25px",
				),
			INPUT(
				_type = "checkbox",
				_name = "the_last_question",
				_style = "width:400px",
				),
			_align = "right",
			_style = "padding-right:400px;",
			),
		DIV(
			INPUT(
				_type = "submit",
				_value = "Create Quiz",
				_style = "width:400px",
				),
			_align = "right",
			_style = "padding-right:400px;",
			),
		)
	if (form.process().accepted):
		session.quiz_under_development = create_id("QUIZ")
		db.quiz_contents.insert(
			quiz_id = session.quiz_under_development,
			question_id = create_id("QUIZ_QUESTION"),
			question = form.vars.question,
			option_a = form.vars.option_a,
			option_b = form.vars.option_b,
			option_c = form.vars.option_c,
			option_d = form.vars.option_d,
			option_e = form.vars.option_e,
			answer = form.vars.answer,
			points = form.vars.points,
			)
		db.commit()
		db.quizzes_unassigned.insert(
			quiz_id = session.quiz_under_development,
			name = form.vars.name,
			teacher_id = session.teacher_id,
			)
		db.commit()
		if (form.vars.the_last_question == "on"):
			session.quiz_under_development = None
		redirect(
			URL(
				a = "school",
				c = "default",
				f= "add_question_to_quiz",
				)
			)
	return dict(
		form = form,
		home = home,
		)
def drop_student():
	session_manager(request)
	home = get_home_link()
	form = "YOU ARE NOT ENROLLED IN ANY CLASS"
	classrooms_rows = db(db.classrooms.student_id == session.student_id).select()
	enrolled_classes = [""]
	enrolled_classes_list = []
	student_classes = []
	student_quizzes = []
	if (len(classrooms_rows) > 0):
		for x in classrooms_rows:
			enrolled_classes.append(x.class_id + ": " + x.name)
			enrolled_classes_list.append(x.class_id + ": " + x.name)
			student_classes.append(x.class_id)
			quizzes_assigned_rows = db(db.quizzes_assigned.class_id == x.class_id).select()
			for y in quizzes_assigned_rows:
				if (y.quiz_id not in student_quizzes):
					student_quizzes.append(y.quiz_id)
		form = FORM(
			DIV(
				"Pick a Class to drop",
				_style = "padding-left:350px;height:20px;padding-bottom:25px;",
				),
			DIV(
				SELECT(
					enrolled_classes,
					_name = "enrolled_class",
					_style = "width:400px;height:40px;",
					requires = [
						IS_IN_SET(enrolled_classes_list),
						]
					),
				_align = "right",
				_style = "padding-right:400px;height:20px;padding-bottom:70px;",
				),
			DIV(
				INPUT(
					_type = "submit",
					_value = "Drop this Class",
					_style = "width:400px",
					),
				_align = "right",
				_style = "padding-right:400px;",
				),
			)
		if (form.process().accepted):
			class_id = form.vars.enrolled_class[:8]
			classrooms_rows_02 = db(
				(db.classrooms.class_id == class_id)
				&
				(db.classrooms.student_id == session.student_id)
				).select()
			for x in classrooms_rows_02:
				x.delete_record()
				db.commit()
			total_grades_rows = db(
				(db.total_grades.class_id == class_id)
				&
				(db.total_grades.student_id == session.student_id)
				).select()
			for x in total_grades_rows:
				x.delete_record()
				db.commit()
			student_quizzes_single_class = student_quizzes[:]
			for x in student_quizzes:
				class_count = 0
				for y in student_classes:
					quizzes_assigned_rows = db(
						(db.quizzes_assigned.quiz_id == x)
						&
						(db.quizzes_assigned.class_id == y)
						).select()
					if (len(quizzes_assigned_rows) == 1):
						class_count = class_count + 1
					if (class_count > 1):
						student_quizzes_single_class.remove(x)
						break
			for x in student_quizzes_single_class:
				quiz_grades_rows = db(
					(db.quiz_grades.quiz_id == x)
					&
					(db.quiz_grades.student_id == session.student_id)
					).select()
				for y in quiz_grades_rows:
					y.delete_record()
					db.commit()
				quizzes_in_progress_rows = db(
					(db.quizzes_in_progress.quiz_id == x)
					&
					(db.quizzes_in_progress.student_id == session.student_id)
					).select()
				for y in quizzes_in_progress_rows:
					y.delete_record()
					db.commit()
				quizzes_submitted_rows = db(
					(db.quizzes_submitted.quiz_id == x)
					&
					(db.quizzes_submitted.student_id == session.student_id)
					).select()
				for y in quizzes_submitted_rows:
					y.delete_record()
					db.commit()
			redirect(
				URL(
					a = "school",
					c = "default",
					f = "student_dashboard",
					)
				)
	return dict(
		form = form,
		home = home,
		)
def index():
	session.clear()
	session_manager(request)
	teacher_login = A(
		"Instructor Login",
		_href = URL(
			a = "school",
			c = "default",
			f = "teacher_login",
			)
		)
	student_login = A(
		"Student Login",
		_href = URL(
			a = "school",
			c = "default",
			f = "student_login",
			)
		)
	return dict(
		student_login = student_login,
		teacher_login = teacher_login,
		)
def operational_error():
	session_manager(request)
	form = FORM(
		DIV(
			INPUT(
				_type = "submit",
				_value = "OK",
				),
			),
		)
	if (form.process().accepted):
		session.operational_error_token = None
		if (session.login_type == "TEACHER"):
			redirect(
				URL(
					a = "school",
					c = "default",
					f = "teacher_dashboard",
					)
				)
		elif (session.login_type == "STUDENT"):
			redirect(
				URL(
					a = "school",
					c = "default",
					f = "student_dashboard",
					)
				)
		elif (session.login_type == "ADMINISTRATOR"):
			redirect(
				URL(
					a = "school",
					c = "default",
					f = "view_admin_dashboard",
					)
				)
		else:
			redirect(
				URL(
					a = "school",
					c = "default",
					f = "logout",
					)
				)
	return dict(
		form = form,
		)
def quiz_question_teacher_view():
	session_manager(request)
	home = get_home_link()
	question_id = request.vars.question_id
	quiz_id = request.vars.quiz_id
	student_id = request.vars.student_id
	quiz_contents_rows = db(db.quiz_contents.question_id == question_id).select()
	if (len(quiz_contents_rows) != 1):
		system_error(
			"question ID is not unique, or not found in database! (ref:quiz_question_teacher_view)"
			)
	else:
		session.teacher_student_view = "TRUE"
		form = quiz_question_view_only(quiz_contents_rows[0])
	return dict(
		form = form,
		home = home,
		)
def quiz_submit_authentication():
	session_manager(request)
	home = get_home_link()
	quiz_id = request.vars.quiz_id
	name = get_quiz_name(quiz_id)
	form = FORM(
		DIV(
			LABEL(
				"Your Course Portal Login Password:",
				_style = "padding-right:25px",
				),
			INPUT(
				_type = "password",
				_name = "portal_pswd",
				_style = "width:400px",
				),
			_align = "right",
			_style = "padding-right:400px;",
			),
		DIV(
			INPUT(
				_type = "submit",
				_value = "Login",
				_style = "width:400px",
				),
			_align = "right",
			_style = "padding-right:400px;",
			),
		)
	if (form.process().accepted):
		students_rows = db().select(db.students.ALL)
		for x in students_rows:
			if (form.vars.portal_pswd == x.portal_pswd):
				redirect(
					URL(
						a = "school",
						c = "default",
						f = "grade_quiz",
						vars = dict(quiz_id = quiz_id)
						)
					)
		system_error("incorrect quiz submittal credentials!")
	return dict(
		form = form,
		home = home,
		name = name,
		quiz_id = quiz_id,
		)
def register_student():
	session_manager(request)
	home = get_home_link()
	form = FORM(
		DIV(
			LABEL(
				"Enter Student Name:",
				_style = "padding-right:25px",
				),
			INPUT(
				_type = "text",
				_name = "name",
				_style = "width:400px",
				),
			_align = "right",
			_style = "padding-right:400px;",
			),
		DIV(
			LABEL(
				"Assign to Student a Course Portals Login Handle:",
				_style = "padding-right:25px",
				),
			INPUT(
				_type = "text",
				_name = "handle",
				_style = "width:400px",
				requires = [
					IS_NOT_IN_DB(db, db.students.handle),
					IS_NOT_EMPTY(),
					]
				),
			_align = "right",
			_style = "padding-right:400px;",
			),
		DIV(
			LABEL(
				"Assign to Student a Course Portals Login Password:",
				_style = "padding-right:25px",
				),
			INPUT(
				_type = "text",
				_name = "portal_pswd",
				_style = "width:400px",
				),
			_align = "right",
			_style = "padding-right:400px;",
			),
		DIV(
			INPUT(
				_type = "submit",
				_value = "Admit Student",
				_style = "width:400px",
				),
			_align = "right",
			_style = "padding-right:400px;",
			),
		)
	if (form.process().accepted):
		db.students.insert(
			student_id = create_id("STUDENT"),
			name = form.vars.name,
			handle = form.vars.handle,
			portal_pswd = form.vars.portal_pswd,
			)
		db.commit()
	return dict(
		form = form,
		home = home,
		)
def register_teacher():
	session_manager(request)
	home = get_home_link()
	form = FORM(
		DIV(
			LABEL(
				"Enter Instructor Name:",
				_style = "padding-right:25px",
				),
			INPUT(
				_type = "text",
				_name = "name",
				_style = "width:400px",
				),
			_align = "right",
			_style = "padding-right:400px;",
			),
		DIV(
			LABEL(
				"Assign to Instructor a Course Portals Login Handle:",
				_style = "padding-right:25px",
				),
			INPUT(
				_type = "text",
				_name = "handle",
				_style = "width:400px",
				requires = [
					IS_NOT_IN_DB(db, db.students.handle),
					IS_NOT_EMPTY(),
					]
				),
			_align = "right",
			_style = "padding-right:400px;",
			),
		DIV(
			LABEL(
				"Assign to Instructor a Course Portals Login Password:",
				_style = "padding-right:25px",
				),
			INPUT(
				_type = "text",
				_name = "portal_pswd",
				_style = "width:400px",
				),
			_align = "right",
			_style = "padding-right:400px;",
			),
		DIV(
			INPUT(
				_type = "submit",
				_value = "Hire Instructor",
				_style = "width:400px",
				),
			_align = "right",
			_style = "padding-right:400px;",
			),
		)
	if (form.process().accepted):
		db.teachers.insert(
			teacher_id = create_id("TEACHER"),
			name = form.vars.name,
			handle = form.vars.handle,
			portal_pswd = form.vars.portal_pswd,
			)
		db.commit()
	return dict(
		form = form,
		home = home,
		)
def student_dashboard():
	session_manager(request)
	my_course_list = DIV(
		TR(
			TD("YOU ARE NOT ENROLLED IN ANY COURSES", _colspan = "2")
			)
		)
	my_submitted_quizzes_list = DIV(
		TR(
			TD("YOU HAVE NO SUBMITTED QUIZZES", _colspan = "2")
			)
		)
	my_unsubmitted_quizzes_list = DIV(
		TR(
			TD("YOU HAVE NO UNSUBMITTED QUIZZES", _colspan = "2")
			)
		)
	add_class = A(
		"Add a Class",
		_href = URL(
			a = "school",
			c = "default",
			f = "add_student",
			)
		)
	drop_class = A(
		"Drop a Class",
		_href = URL(
			a = "school",
			c = "default",
			f = "drop_student",
			)
		)
	my_courses = TABLE()
	my_submitted_quizzes = TABLE()
	my_unsubmitted_quizzes = TABLE()
	table_header_courses = TR(
		TH(
			"Course Name", 
			_style = "width:250px;height:40px;",
			),
		TH(
			"Course Section ID",
			_style = "width:250px;height:40px;",
			),
		TH(
			"Course Status",
			_style = "width:250px;height:40px;",
			),
		TH(
			"Cumulative Course Grade",
			_style = "width:250px;height:40px;",
			),
		)
	table_header_quizzes = TR(
		TH(
			"Quiz Name", 
			_style = "width:250px;height:40px;",
			),
		TH(
			"Quiz ID",
			_style = "width:250px;height:40px;",
			),
		)
	my_courses.append(table_header_courses)
	my_submitted_quizzes.append(table_header_quizzes)
	my_unsubmitted_quizzes.append(table_header_quizzes)
	classrooms_rows = db(
		(db.classrooms.student_id == session.student_id)
		).select()
	if (len(classrooms_rows) > 0):
		my_course_list = DIV()
		for x in classrooms_rows:
			total_grades_rows = db(
				(db.total_grades.student_id == session.student_id)
				&
				(db.total_grades.class_id == x.class_id)
				).select()
			if (len(total_grades_rows) > 0):
				course_status = total_grades_rows[0].course_status
				cumulative_grade = total_grades_rows[0].cumulative_grade
			else:
				system_error("data corruption! - no record for cumulative grade found (but it should exist!)")
			table_row = TR(
				TD(
					x.name,
					_style = "height:30px;",
					),
				TD(
					x.class_id,
					),
				TD(
					course_status,
					),
				TD(
					cumulative_grade,
					),
				)
			my_course_list.append(table_row)
	quizzes_in_progress_rows = db(
		(db.quizzes_in_progress.student_id == session.student_id)
		).select(
			db.quizzes_in_progress.quiz_id,
			db.quizzes_in_progress.student_id,
			distinct = True,
			)
	if (len(quizzes_in_progress_rows) > 0):
		my_unsubmitted_quizzes_list = DIV()
		for x in quizzes_in_progress_rows:
			quizzes_assigned_rows = db(db.quizzes_assigned.quiz_id == x.quiz_id).select()
			if (len(quizzes_assigned_rows) == 1):
				name = quizzes_assigned_rows[0].name
			else:
				system_error(
					"data corruption! - there should be exactly "
					+
					"one 'db.quizzes_assigned' record in the table"
					)
			table_row = TR(
				TD(
					name,
					_style = "height:30px;",
					),
				TD(
					A(
						x.quiz_id,
						_href = URL(
							a = "school",
							c = "default",
							f = "student_quiz",
							vars = dict(
								quiz_id = x.quiz_id,
								),
							)
						)
					),
				)
			my_unsubmitted_quizzes_list.append(table_row)
	quizzes_submitted_rows = db(
		(db.quizzes_submitted.student_id == session.student_id)
		).select(
			db.quizzes_submitted.quiz_id,
			db.quizzes_submitted.student_id,
			distinct = True,
			)
	if (len(quizzes_submitted_rows) > 0):
		my_submitted_quizzes_list = DIV()
		for x in quizzes_submitted_rows:
			quizzes_assigned_rows = db(db.quizzes_assigned.quiz_id == x.quiz_id).select()
			if (len(quizzes_assigned_rows) == 1):
				name = quizzes_assigned_rows[0].name
			else:
				system_error(
					"data corruption! - there should be exactly "
					+
					"one 'db.quizzes_assigned' record in the table"
					)
			table_row = TR(
				TD(
					name,
					_style = "height:30px;",
					),
				TD(
					A(
						x.quiz_id,
						_href = URL(
							a = "school",
							c = "default",
							f = "student_quiz",
							vars = dict(
								quiz_id = x.quiz_id,
								),
							)
						)
					),
				)
			my_submitted_quizzes_list.append(table_row)
	my_courses.append(my_course_list)
	my_submitted_quizzes.append(my_submitted_quizzes_list)
	my_unsubmitted_quizzes.append(my_unsubmitted_quizzes_list)
	return dict(
		add_class = add_class,
		drop_class = drop_class,
		my_courses = my_courses,
		my_submitted_quizzes = my_submitted_quizzes,
		my_unsubmitted_quizzes = my_unsubmitted_quizzes,
		)
def student_grades():
	session_manager(request)
	home = get_home_link()
	student_id = request.vars.student_id
	table = TABLE()
	quiz_grades_rows = db(db.quiz_grades.student_id == student_id).select()
	for x in quiz_grades_rows:
		quizzes_assigned_rows = db(db.quizzes_assigned.quiz_id == x.quiz_id).select()
		if (len(quizzes_assigned_rows) == 1):
			table_row = TR(
				TD(
					A(
						x.quiz_id,
						_href = URL(
							a = "school",
							c = "default",
							f = "student_quiz_teacher_view",
							vars = dict(
								student_id = student_id,
								quiz_id = x.quiz_id,
								)
							)
						)
					),
				TD(x.quiz_points_earned),
				TD(x.quiz_points_max),
				TD(quizzes_assigned_rows[0].quiz_points),
				)
			table.append(table_row)
		else:
			system_error(
				"data corruption! - it should not be possible to have more or less than"
				+
				"exactly one db.quizzes_assigned record for a graded quiz"
				)
	return dict(
		table = table,
		home = home,
		)
def student_login():
	session_manager(request)
	home = get_home_link()
	form = login_form()
	if (form.process().accepted):
		students_rows = db().select(db.students.ALL)
		for x in students_rows:
			if (
				(form.vars.handle == x.handle)
				and
				(form.vars.portal_pswd == x.portal_pswd)
				):
				session.login_type = "STUDENT"
				session.portal_user = x.name
				session.student_id = x.student_id
				redirect(
					URL(
						a = "school",
						c = "default",
						f = "student_dashboard",
						)
					)
		system_error("incorrect login credentials!")
	return dict(
		home = home,
		form = form,
		)
def student_quiz_question():
	session_manager(request)
	home = get_home_link()
	if (session.quiz_id_student == None):
		session.quiz_id_student = request.vars.quiz_id
	if (session.question_id_student == None):
		session.question_id_student = request.vars.question_id
	submitted = request.vars.submitted
	quiz_contents_rows = db(db.quiz_contents.question_id == session.question_id_student).select()
	if (len(quiz_contents_rows) != 1):
		system_error("question ID is not unique, or not found in database!")
	else:
		if (submitted == "FALSE"):
			form = FORM(
				DIV(quiz_contents_rows[0].question),
				DIV(
					LABEL("(A) ", _style = "padding-right:25px;",),
					INPUT(
						_value = "(A)",
						_type = "radio",
						_name = "student_answer",
						),
					quiz_contents_rows[0].option_a,
					_align = "left",
					_style = "min-width:40%;padding-left:40%;",
					),
				DIV(
					LABEL("(B) ", _style = "padding-right:25px;",),
					INPUT(
						_value = "(B)",
						_type = "radio",
						_name = "student_answer",
						),
					quiz_contents_rows[0].option_b,
					_align = "left",
					_style = "min-width:40%;padding-left:40%;",
					),
				DIV(
					LABEL("(C) ", _style = "padding-right:25px;",),
					INPUT(
						_value = "(C)",
						_type = "radio",
						_name = "student_answer",
						),
					quiz_contents_rows[0].option_c,
					_align = "left",
					_style = "min-width:40%;padding-left:40%;",
					),
				DIV(
					LABEL("(D) ", _style = "padding-right:25px;",),
					INPUT(
						_value = "(D)",
						_type = "radio",
						_name = "student_answer",
						),
					quiz_contents_rows[0].option_d,
					_align = "left",
					_style = "min-width:40%;padding-left:40%;",
					),
				DIV(
					LABEL("(E) ", _style = "padding-right:25px;",),
					INPUT(
						_value = "(E)",
						_type = "radio",
						_name = "student_answer",
						),
					quiz_contents_rows[0].option_e,
					_align = "left",
					_style = "min-width:40%;padding-left:40%;",
					),
				DIV(
					INPUT(
						_type = "submit",
						_value = "Login",
						_style = "width:400px",
						),
					_align = "right",
					_style = "padding-right:40%;",
					),
				)
			if (form.process().accepted):
				question_id = session.question_id_student
				quiz_id = session.quiz_id_student
				quizzes_in_progress_rows = db(
					(db.quizzes_in_progress.question_id == str(question_id))
					&
					(db.quizzes_in_progress.student_id == str(session.student_id))
					).select()
				if (len(quizzes_in_progress_rows) == 1):
					quizzes_in_progress_rows[0].update_record(
						quiz_id = quiz_id,
						student_id = session.student_id,
						question_id = question_id,
						current_answer = form.vars.student_answer,
						)
					db.commit()
					redirect(
						URL(
							a = "school",
							c = "default",
							f = "student_quiz",
							vars = dict(quiz_id = quiz_id),
							)
						)
				else:
					system_error(
						"data corruption! - there should be one and only one "
						+
						"quiz question record for this student"
						)
		else:
			form = quiz_question_view_only(quiz_contents_rows[0])
	return dict(
		form = form,
		home = home,
		)
def student_quiz():
	session_manager(request)
	home = get_home_link()
	quiz_id = request.vars.quiz_id
	name = get_quiz_name(quiz_id)
	submit_quiz = ""
	quizzes_in_progress_rows = db(
		(db.quizzes_in_progress.quiz_id == quiz_id)
		&
		(db.quizzes_in_progress.student_id == session.student_id)
		).select(
			db.quizzes_in_progress.quiz_id,
			db.quizzes_in_progress.student_id,
			distinct = True,
			)
	quizzes_submitted_rows = db(
		(db.quizzes_submitted.quiz_id == quiz_id)
		&
		(db.quizzes_submitted.student_id == session.student_id)
		).select(
			db.quizzes_submitted.quiz_id,
			db.quizzes_submitted.student_id,
			distinct = True,
			)
	length_in_progress = len(quizzes_in_progress_rows)
	length_submitted = len(quizzes_submitted_rows)
	if ((length_in_progress ==1) and (length_submitted == 0)):
		submitted = "FALSE"
	elif ((length_submitted == 1) and (length_in_progress == 0)):
		submitted = "TRUE"
	else:
		system_error(
			"the quiz should be present in one and only one table "
			+
			"(db.quizzes_in_progress, or db.quizzes_submitted)"
			)
	table = TABLE(
		TR(
			TH(
				"Question"
				),
			TH(
				"My Answer",
				),
			TH(),
			)
		)
	quiz_contents_rows = db(db.quiz_contents.quiz_id == quiz_id).select()
	if (len(quiz_contents_rows) == 0):
		system_error("data corruption! - it should not be possible for a quiz to have no questions")
	else:
		for x in quiz_contents_rows:
			if (submitted == "FALSE"):
				quizzes_in_progress_rows = db(
					(db.quizzes_in_progress.question_id == x.question_id)
					&
					(db.quizzes_in_progress.student_id == session.student_id)
					).select()
				submit_quiz = A(
					"SUBMIT QUIZ FOR GRADING",
					_href = URL(
						a = "school",
						c = "default",
						f = "quiz_submit_authentication",
						vars = dict(quiz_id = quiz_id),
						),
					)
				current_answer = quizzes_in_progress_rows[0].current_answer
				quiz_contents_rows = db(db.quiz_contents.question_id == x.question_id).select()
				if (len(quiz_contents_rows) == 0):
					system_error("data corruption! - no quiz contents (ref: student_quiz)")
				if (current_answer == "NOT_ANSWERED"):
					link_anchor = "ANSWER QUESTION"
					my_answer = "NOT ANSWERED"
				else:
					link_anchor = "CHANGE MY ANSWER"
					if (current_answer == "(A)"):
						my_answer = XML(
							"(A)<br><strong><font color = 'purple' size = 4em>" 
							+ 
							quiz_contents_rows[0].option_a 
							+ 
							"</font></strong>"
							)
					elif (current_answer == "(B)"):
						my_answer = XML(
							"(B)<br><strong><font color = 'purple' size = 4em>" 
							+ 
							quiz_contents_rows[0].option_b 
							+ 
							"</font></strong>"
							)
					elif (current_answer == "(C)"):
						my_answer = XML(
							"(C)<br><strong><font color = 'purple' size = 4em>" 
							+ 
							quiz_contents_rows[0].option_c 
							+ 
							"</font></strong>"
							)
					elif (current_answer == "(D)"):
						my_answer = XML(
							"(D)<br><strong><font color = 'purple' size = 4em>" 
							+ 
							quiz_contents_rows[0].option_d 
							+ 
							"</font></strong>"
							)
					elif (current_answer == "(E)"):
						my_answer = XML(
							"(E)<br><strong><font color = 'purple' size = 4em>" 
							+ 
							quiz_contents_rows[0].option_e 
							+ 
							"</font></strong>"
							)
			elif (submitted == "TRUE"):
				quizzes_submitted_rows = db(
					(db.quizzes_submitted.question_id == x.question_id)
					&
					(db.quizzes_submitted.student_id == session.student_id)
					).select()
				submitted_answer = quizzes_submitted_rows[0].submitted_answer
				quiz_contents_rows = db(db.quiz_contents.question_id == x.question_id).select()
				if (len(quiz_contents_rows) == 0):
					system_error("data corruption! - no quiz contents (ref: student_quiz)")
				else:
					if (submitted_answer == "(A)"):
						my_answer = XML(
							"(A)<br><strong><font color = 'purple' size = 4em>" 
							+ 
							quiz_contents_rows[0].option_a 
							+ 
							"</font></strong>"
							)
						if (submitted_answer == quiz_contents_rows[0].answer):
							link_anchor = "CORRECT"
						else:
							link_anchor = "WRONG - should be " + quiz_contents_rows[0].answer
					elif (submitted_answer == "(B)"):
						my_answer = XML(
							"(B)<br><strong><font color = 'purple' size = 4em>" 
							+ 
							quiz_contents_rows[0].option_b 
							+ 
							"</font></strong>"
							)
						if (submitted_answer == quiz_contents_rows[0].answer):
							link_anchor = "CORRECT"
						else:
							link_anchor = "WRONG - should be " + quiz_contents_rows[0].answer
					elif (submitted_answer == "(C)"):
						my_answer = XML(
							"(C)<br><strong><font color = 'purple' size = 4em>" 
							+ 
							quiz_contents_rows[0].option_c 
							+ 
							"</font></strong>"
							)
						if (submitted_answer == quiz_contents_rows[0].answer):
							link_anchor = "CORRECT"
						else:
							link_anchor = "WRONG - should be " + quiz_contents_rows[0].answer
					elif (submitted_answer == "(D)"):
						my_answer = XML(
							"(D)<br><strong><font color = 'purple' size = 4em>" 
							+ 
							quiz_contents_rows[0].option_d 
							+ 
							"</font></strong>"
							)
						if (submitted_answer == quiz_contents_rows[0].answer):
							link_anchor = "CORRECT"
						else:
							link_anchor = "WRONG - should be " + quiz_contents_rows[0].answer
					elif (submitted_answer == "(E)"):
						my_answer = XML(
							"(E)<br><strong><font color = 'purple' size = 4em>" 
							+ 
							quiz_contents_rows[0].option_e 
							+ 
							"</font></strong>"
							)
						if (submitted_answer == quiz_contents_rows[0].answer):
							link_anchor = "CORRECT"
						else:
							link_anchor = "WRONG - should be " + quiz_contents_rows[0].answer
					else:
						my_answer = XML(
							"NOT ANSWERED"
							)
						link_anchor = "WRONG - should be " + quiz_contents_rows[0].answer
			else:
				system_error("the quiz 'submitted' status should be either 'TRUE' or 'FALSE'!")
			table_row = TR(
				TD(
					x.question,
					_style = "padding-bottom:50px;padding-right:50px;",
					),
				TD(
					my_answer,
					_style = "padding-bottom:50px;padding-right:50px;",
					),
				TD(
					A(
						link_anchor,
						_href = URL(
							a = "school",
							c = "default",
							f = "student_quiz_question",
							vars = dict(
								quiz_id = x.quiz_id,
								question_id = x.question_id,
								submitted = submitted,
								)
							)
						),
					_style = "padding-bottom:50px;",
					),
				)
			table.append(table_row)
	return dict(
		home = home,
		table = table,
		name = name,
		quiz_id = quiz_id,
		submit_quiz = submit_quiz,
		)
def student_quiz_teacher_view():
	session_manager(request)
	home = get_home_link()
	student_id = request.vars.student_id
	quiz_id = request.vars.quiz_id
	table = TABLE(
		TR(
			TH(
				"Question"
				),
			TH(
				"My Answer",
				),
			TH(),
			)
		)
	quiz_contents_rows = db(db.quiz_contents.quiz_id == quiz_id).select()
	if (len(quiz_contents_rows) == 0):
		system_error("data corruption! - it should not be possible for a quiz to have no questions")
	else:
		for x in quiz_contents_rows:
			quizzes_submitted_rows = db(
				(db.quizzes_submitted.question_id == x.question_id)
				&
				(db.quizzes_submitted.student_id == student_id)
				).select()
			submitted_answer = quizzes_submitted_rows[0].submitted_answer
			quiz_contents_rows = db(db.quiz_contents.question_id == x.question_id).select()
			if (len(quiz_contents_rows) == 0):
				system_error(
					"data corruption! - no quiz contents "
					+
					"(ref: student_quiz_teacher_view)"
					)
			else:
				if (submitted_answer == "(A)"):
					student_answer = XML(
						"(A)<br><strong><font color = 'purple' size = 4em>" 
						+ 
						quiz_contents_rows[0].option_a 
						+ 
						"</font></strong>"
						)
					if (submitted_answer == quiz_contents_rows[0].answer):
						link_anchor = "CORRECT"
					else:
						link_anchor = "WRONG - should be " + quiz_contents_rows[0].answer
				elif (submitted_answer == "(B)"):
					student_answer = XML(
						"(B)<br><strong><font color = 'purple' size = 4em>" 
						+ 
						quiz_contents_rows[0].option_b 
						+ 
						"</font></strong>"
						)
					if (submitted_answer == quiz_contents_rows[0].answer):
						link_anchor = "CORRECT"
					else:
						link_anchor = "WRONG - should be " + quiz_contents_rows[0].answer
				elif (submitted_answer == "(C)"):
					student_answer = XML(
						"(C)<br><strong><font color = 'purple' size = 4em>" 
						+ 
						quiz_contents_rows[0].option_c 
						+ 
						"</font></strong>"
						)
					if (submitted_answer == quiz_contents_rows[0].answer):
						link_anchor = "CORRECT"
					else:
						link_anchor = "WRONG - should be " + quiz_contents_rows[0].answer
				elif (submitted_answer == "(D)"):
					student_answer = XML(
						"(D)<br><strong><font color = 'purple' size = 4em>" 
						+ 
						quiz_contents_rows[0].option_d 
						+ 
						"</font></strong>"
						)
					if (submitted_answer == quiz_contents_rows[0].answer):
						link_anchor = "CORRECT"
					else:
						link_anchor = "WRONG - should be " + quiz_contents_rows[0].answer
				elif (submitted_answer == "(E)"):
					student_answer = XML(
						"(E)<br><strong><font color = 'purple' size = 4em>" 
						+ 
						quiz_contents_rows[0].option_e 
						+ 
						"</font></strong>"
						)
					if (submitted_answer == quiz_contents_rows[0].answer):
						link_anchor = "CORRECT"
					else:
						link_anchor = "WRONG - should be " + quiz_contents_rows[0].answer
				else:
					student_answer = XML(
						"NOT ANSWERED"
						)
					link_anchor = "WRONG - should be " + quiz_contents_rows[0].answer
			table_row = TR(
				TD(
					x.question,
					_style = "padding-bottom:50px;padding-right:50px;",
					),
				TD(
					student_answer,
					_style = "padding-bottom:50px;padding-right:50px;",
					),
				TD(
					A(
						link_anchor,
						_href = URL(
							a = "school",
							c = "default",
							f = "quiz_question_teacher_view",
							vars = dict(
								question_id = x.question_id,
								student_id = student_id,
								quiz_id = quiz_id,
								)
							)
						),
					_style = "padding-bottom:50px;",
					),
				)
			table.append(table_row)
	return dict(
		home = home,
		table = table,
		)
def students_in_course():
	session_manager(request)
	home = get_home_link()
	class_id = request.vars.class_id
	table = TABLE()
	classrooms_rows = db(
		(db.classrooms.class_id == class_id)
		&
		(db.classrooms.student_id != "NONE_ENROLLED")
		).select()
	if (len(classrooms_rows) > 0):
		for x in classrooms_rows:
			students_rows = db(db.students.student_id == x.student_id).select()
			if (len(students_rows) == 1):
				total_grades_rows = db(
					(db.total_grades.class_id == x.class_id)
					&
					(db.total_grades.student_id == x.student_id)
					).select()
				if (len(total_grades_rows) == 1):
					student = students_rows[0].name
					grade = total_grades_rows[0].cumulative_grade
					if (grade != "UNDEFINED"):
						grade = grade[(len(grade) - 1):]
				else:
					system_error(
						"data corruption! - one and only one db.total_grades record"
						+
						" should exist for this student/class combination"
						)
				table.append(
					TR(
						TD(
							A(
								student,
								_href = URL(
									a = "school",
									c = "default",
									f = "student_grades",
									vars = dict(student_id = x.student_id),
									)
								)
							),
						TD(grade),
						)
					)
			else:
				system_error(
					"data corruption! - one and only one a record "
					+
					"in the db.students table should exist for this student id"
					)
	else:
		table = "NO STUDENTS ARE CURRENTLY ENROLLED IN THIS CLASS"
	return dict(
		home = home,
		table = table,
		)
def teacher_dashboard():
	session_manager(request)
	my_course_list = DIV(
		TR(
			TD("CURRENTLY NOT TEACHING ANY COURSES", _colspan = "2")
			)
		)
	my_assigned_quizzes_list = DIV(
		TR(
			TD("CURRENTLY THERE ARE NO ASSIGNED QUIZZES", _colspan = "2")
			)
		)
	my_unassigned_quizzes_list = DIV(
		TR(
			TD("CURRENTLY THERE ARE NO UNASSIGNED QUIZZES", _colspan = "2")
			)
		)
	create_classroom = A(
		"Register New Classroom",
		_href = URL(
			a = "school",
			c = "default",
			f = "create_classroom",
			)
		)
	create_quiz = A(
		"Create a Quiz",
		_href = URL(
			a = "school",
			c = "default",
			f = "create_quiz",
			)
		)
	my_courses = TABLE()
	my_assigned_quizzes = TABLE()
	my_unassigned_quizzes = TABLE()
	table_header_courses = TR(
		TH(
			"Course Name", 
			_style = "width:250px;height:40px;",
			),
		TH(
			"Course Section ID",
			_style = "width:250px;height:40px;",
			),
		)
	table_header_quizzes = TR(
		TH(
			"Quiz Name", 
			_style = "width:250px;height:40px;",
			),
		TH(
			"Quiz ID",
			_style = "width:250px;height:40px;",
			),
		)
	my_courses.append(table_header_courses)
	my_assigned_quizzes.append(table_header_quizzes)
	my_unassigned_quizzes.append(table_header_quizzes)
	classrooms_rows = db(
		(db.classrooms.teacher_id == session.teacher_id)
		).select(
			db.classrooms.class_id, 
			db.classrooms.name, 
			distinct = True,
			)
	if (len(classrooms_rows) > 0):
		my_course_list = DIV()
		for x in classrooms_rows:
			table_row = TR(
				TD(
					x.name,
					_style = "height:30px;",
					),
				TD(
					A(
						x.class_id,
						_href = URL(
							a = "school",
							c = "default",
							f = "students_in_course",
							vars = dict(class_id = x.class_id),
							)
						)
					),
				)
			my_course_list.append(table_row)
	quizzes_unassigned_rows = db(db.quizzes_unassigned.teacher_id == session.teacher_id).select()
	if (len(quizzes_unassigned_rows) > 0):
		my_unassigned_quizzes_list = DIV()
		for x in quizzes_unassigned_rows:
			table_row = TR(
				TD(
					x.name,
					_style = "height:30px;",
					),
				TD(
					A(
						x.quiz_id,
						_href = URL(
							a = "school",
							c = "default",
							f = "teacher_quiz",
							vars = dict(quiz_id = x.quiz_id),
							)
						),
					),
				)
			my_unassigned_quizzes_list.append(table_row)
	quizzes_assigned_rows = db(
		(db.quizzes_assigned.teacher_id == session.teacher_id)
		).select(
			db.quizzes_assigned.quiz_id,
			db.quizzes_assigned.name,
			distinct = True,
			)
	if (len(quizzes_assigned_rows) > 0):
		my_assigned_quizzes_list = DIV()
		for x in quizzes_assigned_rows:
			table_row = TR(
				TD(
					x.name,
					_style = "height:30px;",
					),
				TD(
					A(
						x.quiz_id,
						_href = URL(
							a = "school",
							c = "default",
							f = "teacher_quiz",
							vars = dict(quiz_id = x.quiz_id),
							)
						),
					),
				)
			my_assigned_quizzes_list.append(table_row)
	my_courses.append(my_course_list)
	my_assigned_quizzes.append(my_assigned_quizzes_list)
	my_unassigned_quizzes.append(my_unassigned_quizzes_list)
	return dict(
		create_classroom = create_classroom,
		create_quiz = create_quiz,
		my_courses = my_courses,
		my_assigned_quizzes = my_assigned_quizzes,
		my_unassigned_quizzes = my_unassigned_quizzes,
		)
def teacher_login():
	session_manager(request)
	home = get_home_link()
	form = login_form()
	if (form.process().accepted):
		teachers_rows = db().select(db.teachers.ALL)
		for x in teachers_rows:
			if (
				(form.vars.handle == x.handle)
				and
				(form.vars.portal_pswd == x.portal_pswd)
				):
				session.login_type = "TEACHER"
				session.portal_user = x.name
				session.teacher_id = x.teacher_id
				redirect(
					URL(
						a = "school",
						c = "default",
						f = "teacher_dashboard",
						)
					)
		system_error("incorrect login credentials!")
	return dict(
		home = home,
		form = form,
		)
def teacher_quiz_question():
	session_manager(request)
	home = get_home_link()
	quiz_id = request.vars.quiz_id
	question_id = request.vars.question_id
	assigned = request.vars.assigned
	quiz_contents_rows = db(db.quiz_contents.question_id == question_id).select()
	if (len(quiz_contents_rows) != 1):
		system_error("question ID is not unique, or not found in database!")
	else:
		if (assigned == "TRUE"):
			table = quiz_question_view_only(quiz_contents_rows[0])
			delete_question = ""
		else:
			table = FORM(
				DIV(
					LABEL(
						"Enter Question:",
						_style = "padding-right:25px",
						),
					TEXTAREA(
						_name = "question",
						_placeholder = quiz_contents_rows[0].question,
						_style = "width:400px;height:100px",
						requires = IS_NOT_EMPTY(error_message = "enter a question")
						),
					_align = "right",
					_style = "padding-right:400px;",
					),
				DIV(
					LABEL(
						"Specify Points for Question:",
						_style = "padding-right:25px",
						),
					INPUT(
						_type = "text",
						_name = "points",
						_placeholder = quiz_contents_rows[0].points,
						_style = "width:400px",
						requires = IS_NOT_EMPTY(error_message = "specify a points value")
						),
					_align = "right",
					_style = "padding-right:400px;",
					),
				DIV(
					LABEL(
						"Specify Option (A):",
						_style = "padding-right:25px",
						),
					INPUT(
						_type = "text",
						_name = "option_a",
						_placeholder = quiz_contents_rows[0].option_a,
						_style = "width:400px",
						requires = IS_NOT_EMPTY(error_message = "specify an option")
						),
					_align = "right",
					_style = "padding-right:400px;",
					),
				DIV(
					LABEL(
						"Specify Option (B):",
						_style = "padding-right:25px",
						),
					INPUT(
						_type = "text",
						_name = "option_b",
						_placeholder = quiz_contents_rows[0].option_b,
						_style = "width:400px",
						requires = IS_NOT_EMPTY(error_message = "specify an option")
						),
					_align = "right",
					_style = "padding-right:400px;",
					),
				DIV(
					LABEL(
						"Specify Option (C):",
						_style = "padding-right:25px",
						),
					INPUT(
						_type = "text",
						_name = "option_c",
						_placeholder = quiz_contents_rows[0].option_c,
						_style = "width:400px",
						requires = IS_NOT_EMPTY(error_message = "specify an option")
						),
					_align = "right",
					_style = "padding-right:400px;",
					),
				DIV(
					LABEL(
						"Specify Option (D):",
						_style = "padding-right:25px",
						),
					INPUT(
						_type = "text",
						_name = "option_d",
						_placeholder = quiz_contents_rows[0].option_d,
						_style = "width:400px",
						requires = IS_NOT_EMPTY(error_message = "specify an option")
						),
					_align = "right",
					_style = "padding-right:400px;",
					),
				DIV(
					LABEL(
						"Specify Option (E):",
						_style = "padding-right:25px",
						),
					INPUT(
						_type = "text",
						_name = "option_e",
						_placeholder = quiz_contents_rows[0].option_e,
						_style = "width:400px",
						requires = IS_NOT_EMPTY(error_message = "specify an option")
						),
					_align = "right",
					_style = "padding-right:400px;",
					),
				DIV(
					LABEL(
						"Specify Correct Option",
						_style = "padding-right:25px",
						),
					SELECT(
						["specify the correct answer", "(A)", "(B)", "(C)", "(D)", "(E)"],
						_name = "answer",
						value = quiz_contents_rows[0].answer,
						_style = "width:400px",
						requires = [
							IS_IN_SET(["(A)", "(B)", "(C)", "(D)", "(E)"]),
							]
						),
					_align = "right",
					_style = "padding-right:400px;",
					),
				DIV(
					INPUT(
						_type = "submit",
						_value = "Update Question",
						_style = "width:400px",
						),
					_align = "right",
					_style = "padding-right:400px;",
					),
				)
			delete_question = A(
				"DELETE THIS QUESTION FROM QUIZ",
				_href = URL(
					a = "school",
					c = "default",
					f = "delete_quiz_question",
					vars = dict(
						question_id = question_id,
						quiz_id = quiz_id,
						),
					)
				)	
	quiz_link = A(
		"Quiz ID: " + quiz_id,
		_href = URL(
			a = "school",
			c = "default",
			f = "teacher_quiz",
			vars = dict(quiz_id = quiz_id)
			)
		)
	return dict(
		delete_question = delete_question,
		home = home,
		quiz_link = quiz_link,
		table = table,
		)
def teacher_quiz():
	session_manager(request)
	home = get_home_link()
	if (session.quiz_id_teacher == None):
		session.quiz_id_teacher = request.vars.quiz_id
	quizzes_assigned_rows = db(db.quizzes_assigned.quiz_id == session.quiz_id_teacher).select()
	quizzes_unassigned_rows = db(db.quizzes_unassigned.quiz_id == session.quiz_id_teacher).select()
	length_assigned = len(quizzes_assigned_rows)
	length_unassigned = len(quizzes_unassigned_rows)
	if ((length_unassigned == 0) and (length_assigned > 0)):
		quiz_is_assigned = "TRUE"
		name = quizzes_assigned_rows[0].name
		assign_form = ""
		delete_quiz = ""
		add_question = ""
		session.quiz_under_development = None
	elif((length_unassigned == 1) and (length_assigned == 0)):
		quiz_is_assigned = "FALSE"
		delete_quiz = A(
			"DELETE THIS QUIZ",
			_href = URL(
				a = "school",
				c = "default",
				f = "delete_quiz",
				vars = dict(
					quiz_id = session.quiz_id_teacher,
					),
				)
			)	
		session.quiz_under_development = session.quiz_id_teacher
		add_question = A(
			"ADD A QUESTION",
			_href = URL(
				a = "school",
				c = "default",
				f = "add_question_to_quiz",
				)
			)	
		name = quizzes_unassigned_rows[0].name
		teacher_classes = [""]
		teacher_classes_list = []
		classrooms_rows = db(
			(db.classrooms.teacher_id == session.teacher_id)
			).select(
				db.classrooms.class_id, 
				db.classrooms.name, 
				distinct = True,
				)
		if (len(classrooms_rows) > 0):
			for x in classrooms_rows:
				teacher_classes.append(x.class_id + ": " + x.name)
				teacher_classes_list.append(x.class_id + ": " + x.name)
			assign_form = FORM(
				DIV(
					"Select a Classroom",
					_style = "padding-left:400px;height:20px;padding-bottom:25px;",
					),
				DIV(
					SELECT(
						teacher_classes,
						_name = "teacher_class",
						_style = "width:400px;height:40px;",
						requires = [
							IS_IN_SET(teacher_classes_list),
							]
						),
					_align = "right",
					_style = "padding-right:400px;height:20px;padding-bottom:70px;",
					),
				DIV(
					"Specify Grade Weight Points for this Quiz",
					_style = "padding-left:550px;height:20px;padding-bottom:25px;",
					),
				DIV(
					INPUT(
						_type = "text",
						_name = "points",
						_style = "width:400px;height:40px;",
						requires = IS_NOT_EMPTY(),
						),
					_align = "right",
					_style = "padding-right:400px;height:20px;padding-bottom:70px;",
					),
				DIV(
					INPUT(
						_type = "submit",
						_value = "Assign this Quiz to a Classroom",
						_style = "width:400px",
						),
					_align = "right",
					_style = "padding-right:400px;",
					),
				)
			if (assign_form.process().accepted):
				quizzes_unassigned_rows[0].delete_record()
				db.commit()
				db.quizzes_assigned.insert(
					quiz_id = session.quiz_id_teacher,
					name = name,
					teacher_id = session.teacher_id,
					class_id = assign_form.vars.teacher_class[:8],
					quiz_points = assign_form.vars.points,
					)
				db.commit()
				classrooms_rows = db(
					(db.classrooms.class_id == assign_form.vars.teacher_class[:8])
					).select()
				quiz_contents_rows = db(
					(db.quiz_contents.quiz_id == session.quiz_id_teacher)
					).select()
				for x in classrooms_rows:
					if (x.student_id != "NONE_ENROLLED"):
						for y in quiz_contents_rows:
							db.quizzes_in_progress.insert(
								quiz_id = session.quiz_id_teacher,
								student_id = x.student_id,
								question_id = y.question_id
								)
							db.commit()
		else:
			assign_form = ""
	else:
		system_error(
			"data corruption! - no more than one record should be in db.quizzes_unassigned, "
			+
			"and a quiz should be either assigned or unassigned"
			)
	table = TABLE(
		TR(
			TH(
				"Question"
				),
			TH(
				"View Answer Options"
				),
			)
		)
	quiz_contents_rows = db(db.quiz_contents.quiz_id == session.quiz_id_teacher).select()
	if (len(quiz_contents_rows) == 0):
		system_error("data corruption! - it should not be possible for a quiz to have no questions")
	else:
		for x in quiz_contents_rows:
			table_row = TR(
				TD(
					x.question,
					),
				TD(
					A(
						x.question_id,
						_href = URL(
							a = "school",
							c = "default",
							f = "teacher_quiz_question",
							vars = dict(
								quiz_id = x.quiz_id,
								question_id = x.question_id,
								assigned = quiz_is_assigned,
								)
							)
						)
					),
				)
			table.append(table_row)
	return dict(
		add_question = add_question,
		assign_form = assign_form,
		delete_quiz = delete_quiz,
		home = home,
		name = name,
		quiz_id = session.quiz_id_teacher,
		table = table,
		)
def view_admin_dashboard():
	session_manager(request)
	home = get_home_link()
	register_student = A(
		"Student Admissions",
		_href = URL(
			a = "school",
			c = "default",
			f = "register_student",
			)
		)
	register_teacher = A(
		"Instructor Hiring Portal",
		_href = URL(
			a = "school",
			c = "default",
			f = "register_teacher",
			)
		)
	return dict(
		register_student = register_student,
		register_teacher = register_teacher,
		home = home,
		)
		
# ------------------------ </PAGE RENDERING FUNCTIONS - END> ------------------------



########## <AUXILIARY ITEMS & FUNCTIONS> ############################################

BASE_ID_OFFSET = 1000000	#facilitates alphanumeric ordering up to any number less than 1,000,000
GRADE_THRESHOLD_A = 90
GRADE_THRESHOLD_B = 80
GRADE_THRESHOLD_C = 70
GRADE_THRESHOLD_D = 60
page_headings = {
	"add_student":"Class Enrollment",
	"admin_login":"Administrator Login",
	"create_classroom":"Create Class Section",
	"create_quiz":"Create Class Quiz",
	"add_question_to_quiz":"Add Question to Quiz",
	"drop_student":"Drop a Class",
	"quiz_question_teacher_view":"View Question",
	"quiz_submit_authentication":"Confirm Quiz Submittal",
	"index":"Portals - Public Homepage",
	"operational_error":"Error Message",
	"register_student":"Student Registration",
	"register_teacher":"Teacher Registration",
	"student_dashboard":"Student Homepage Dashboard",
	"student_login":"Student Login",
	"student_quiz":"View Quiz",
	"student_quiz_teacher_view":"Student Quiz Answers",
	"student_quiz_question":"View Question",
	"student_grades":"View Student Grades",
	"students_in_course":"Enrolled Students",
	"take_quiz":"Work on Quiz",
	"teacher_dashboard":"Teacher Homepage Dashboard",
	"teacher_login":"Instructor Login",
	"teacher_quiz":"View Quiz",
	"teacher_quiz_question":"View Question",
	"view_admin_dashboard":"Admin Panel",
	}
administrator_pages = [
	"register_student",
	"register_teacher",
	"view_admin_dashboard",
	"operational_error",
	]
public_pages = [
	"admin_login",
	"index",
	"student_login",
	"teacher_login",
	"operational_error",
	]
student_pages = [
	"add_student",
	"drop_student",
	"operational_error",
	"quiz_submit_authentication",
	"student_dashboard",
	"student_quiz",
	"student_quiz_question",
	"take_quiz",
	]
teacher_pages = [
	"create_classroom",
	"create_quiz",
	"add_question_to_quiz",
	"operational_error",
	"quiz_question_teacher_view",
	"student_grades",
	"student_quiz_teacher_view",
	"students_in_course",
	"teacher_dashboard",
	"teacher_quiz",
	"teacher_quiz_question",
	]
def create_id(role):
	id = "ERROR"
	try:
		id_refs_rows = db().select(db.id_refs.ALL)
		if (len(id_refs_rows) == 0):
			db.id_refs.insert()
			db.commit()
			id_refs_rows = db().select(db.id_refs.ALL)
		if (role == "STUDENT"):
			ref = int(id_refs_rows[0].student_id_ref) + 1
			id_refs_rows[0].update_record(student_id_ref = str(ref))
			id = "S-"+ str(BASE_ID_OFFSET + ref)[1:]
		elif (role == "TEACHER"):
			ref = int(id_refs_rows[0].teacher_id_ref) + 1
			id_refs_rows[0].update_record(teacher_id_ref = str(ref))
			id = "T-"+ str(BASE_ID_OFFSET + ref)[1:]
		elif (role == "QUIZ"):
			ref = int(id_refs_rows[0].quiz_id_ref) + 1
			id_refs_rows[0].update_record(quiz_id_ref = str(ref))
			id = "QZ-"+ str(BASE_ID_OFFSET + ref)[1:]
		elif (role == "QUIZ_QUESTION"):
			ref = int(id_refs_rows[0].quiz_question_id_ref) + 1
			id_refs_rows[0].update_record(quiz_question_id_ref = str(ref))
			id = "QN-"+ str(BASE_ID_OFFSET + ref)[1:]
		elif (role == "CLASSROOM"):
			ref = int(id_refs_rows[0].classroom_id_ref) + 1
			id_refs_rows[0].update_record(classroom_id_ref = str(ref))
			id = "C-"+ str(BASE_ID_OFFSET + ref)[1:]
		else:
			system_error("unspecified case! - a " + role + " id could not be obtained")
	except:
		system_error("execution error! - a " + role + " id could not be obtained")
	return (id)
def delete_quiz():
	session.quiz_id_teacher = None
	quiz_id = request.vars.quiz_id
	quiz_contents_rows = db(db.quiz_contents.quiz_id == quiz_id).select()
	for x in quiz_contents_rows:
		x.delete_record()
		db.commit()
	quizzes_unassigned_rows = db(db.quizzes_unassigned.quiz_id == quiz_id).select()
	for x in quizzes_unassigned_rows:
		x.delete_record()
		db.commit()
	redirect(
		URL(
			a = "school",
			c = "default",
			f = "teacher_dashboard",
			vars = dict(quiz_id = quiz_id),
			)
		)
	return ()
def delete_quiz_question():
	question_id = request.vars.question_id
	quiz_id = request.vars.quiz_id
	quiz_contents_rows = db(db.quiz_contents.question_id == question_id).select()
	for x in quiz_contents_rows:
		x.delete_record()
		db.commit()
	quiz_contents_rows = db(db.quiz_contents.quiz_id == quiz_id).select()
	if (len(quiz_contents_rows) == 0):
		redirect(
			URL(
				a = "school",
				c = "default",
				f = "delete_quiz",
				vars = dict(
					quiz_id = quiz_id,
					),
				)
			)
	else:
		redirect(
			URL(
				a = "school",
				c = "default",
				f = "teacher_quiz",
				vars = dict(quiz_id = quiz_id),
				)
			)
	return ()
def get_home_link():
	if (session.login_type == "STUDENT"):
		home_link = A(
			"home",
			_href = URL(
				a = "school",
				c = "default",
				f = "student_dashboard",
				)
			)
	elif (session.login_type == "TEACHER"):
		home_link = A(
			"home",
			_href = URL(
				a = "school",
				c = "default",
				f = "teacher_dashboard",
				)
			)
	elif (session.login_type == "ADMINISTRATOR"):
		home_link = A(
			"home",
			_href = URL(
				a = "school",
				c = "default",
				f = "view_admin_dashboard",
				)
			)
	else:
		home_link = A(
			"home",
			_href = URL(
				a = "school",
				c = "default",
				f = "index",
				)
			)
	return (home_link)
def get_quiz_name(quiz_id):
	quizzes_unassigned_rows = db(db.quizzes_unassigned.quiz_id == quiz_id).select()
	if (len(quizzes_unassigned_rows) > 0):
		quiz_name = quizzes_unassigned_rows[0].name
	else:
		quizzes_assigned_rows = db(db.quizzes_assigned.quiz_id == quiz_id).select()
		if (len(quizzes_assigned_rows) > 0):
			quiz_name = quizzes_assigned_rows[0].name
		else:
			system_error("quiz should be either assigned or unassigned (ref: get_quiz_name)")
	return (quiz_name)
def grade_quiz():
	quiz_id = request.vars.quiz_id
	quizzes_in_progress_rows = db(
		(db.quizzes_in_progress.quiz_id == quiz_id)
		&
		(db.quizzes_in_progress.student_id == session.student_id)
		).select()
	if (len(quizzes_in_progress_rows) > 0):
		quiz_points_earned = 0
		quiz_points_max = 0
		for x in quizzes_in_progress_rows:
			quiz_contents_rows = db(db.quiz_contents.question_id == x.question_id).select()
			if (len(quiz_contents_rows) == 1):
				quiz_points_max = quiz_points_max + int(quiz_contents_rows[0].points)
				if (quiz_contents_rows[0].answer == x.current_answer):
					quiz_points_earned = quiz_points_earned + int(quiz_contents_rows[0].points)
			else:
				system_error(
					"one and only record should exist for this question "
					+
					"(ref: db.quiz_contents.)"
					)
			db.quizzes_submitted.insert(
				quiz_id = quiz_id,
				student_id = session.student_id,
				question_id = x.question_id,
				submitted_answer = x.current_answer,
				)
			db.commit()
			x.delete_record()
			db.commit()
		db.quiz_grades.insert(
			quiz_id = quiz_id,
			student_id = session.student_id,
			quiz_points_earned = quiz_points_earned,
			quiz_points_max = quiz_points_max,
			)
		db.commit()
		quizzes_assigned_rows = db(db.quizzes_assigned.quiz_id == quiz_id).select()
		if (len(quizzes_assigned_rows) > 0):
			for x in quizzes_assigned_rows:
				classrooms_rows = db(
					(db.classrooms.class_id == x.class_id)
					&
					(db.classrooms.student_id == session.student_id)
					).select()
				if (len(classrooms_rows) == 1):
					total_grades_rows = db(
					(db.total_grades.class_id == x.class_id)
					&
					(db.total_grades.student_id == session.student_id)
						).select()
					if (len(total_grades_rows) == 1):
						submitted_points_earned = int(quiz_points_earned) * int(x.quiz_points)
						submitted_points_max = int(quiz_points_max) * int(x.quiz_points)
						total_submitted_points_earned = str(
							int(total_grades_rows[0].total_submitted_points_earned)
							+
							submitted_points_earned
							)
						total_submitted_points_max = str(
							int(total_grades_rows[0].total_submitted_points_max)
							+
							submitted_points_max
							)
						percentage_grade = (
							float(total_submitted_points_earned) 
							/ 
							float(total_submitted_points_max)
							) * 100
						if (percentage_grade >= GRADE_THRESHOLD_A):
							cumulative_grade = (
								"you have earned " 
								+
								format(percentage_grade, ".2f") 
								+
								"% of total points. Your course grade is: A"
								)
						elif (percentage_grade >= GRADE_THRESHOLD_B):
							cumulative_grade = (
								"you have earned " 
								+
								format(percentage_grade, ".2f") 
								+
								"% of total points. Your course grade is: B"
								)
						elif (percentage_grade >= GRADE_THRESHOLD_C):
							cumulative_grade = (
								"you have earned " 
								+
								format(percentage_grade, ".2f") 
								+
								"% of total points. Your course grade is: C"
								)
						elif (percentage_grade >= GRADE_THRESHOLD_D):
							cumulative_grade = (
								"you have earned " 
								+
								format(percentage_grade, ".2f") 
								+
								"% of total points. Your course grade is: D"
								)
						else:
							cumulative_grade = (
								"you have earned " 
								+
								format(percentage_grade, ".2f") 
								+
								"% of total points. Your course grade is: F"
								)
						total_grades_rows[0].update_record(
							total_submitted_points_earned = total_submitted_points_earned,
							total_submitted_points_max = total_submitted_points_max,
							cumulative_grade = cumulative_grade,
							)
						db.commit()
					else:
						system_error(
							"data corruption! one, and only one "
							+
							"db.total_grades record should exist"
							)
				else:
					system_error(
						"data corruption! - a quiz cannot be submitted for grading without "
						+
						"being in a class; there should be one, and only one record for that"
						)
		else:
			system_error(
				"data corruption - quiz submitted is not in db.quizzes_assigned table; "
				+
				"that should not be possible"
				)
		redirect(
			URL(
				a = "school",
				c = "default",
				f = "student_dashboard",
				)
			)
	else:
		system_error("required quiz records do not exist! (ref: db.quizzes_in_progress)")
	return ()
def login_form():
	form = FORM(
		DIV(
			LABEL(
				"Your Course Portal Login Handle:",
				_style = "padding-right:25px",
				),
			INPUT(
				_type = "text",
				_name = "handle",
				_style = "width:400px",
				),
			_align = "right",
			_style = "padding-right:400px;",
			),
		DIV(
			LABEL(
				"Your Course Portal Login Password:",
				_style = "padding-right:25px",
				),
			INPUT(
				_type = "password",
				_name = "portal_pswd",
				_style = "width:400px",
				),
			_align = "right",
			_style = "padding-right:400px;",
			),
		DIV(
			INPUT(
				_type = "submit",
				_value = "Login",
				_style = "width:400px",
				),
			_align = "right",
			_style = "padding-right:400px;",
			),
		)
	return (form)
def logout():
	session.clear()
	redirect(
		URL(
			a = "school",
			c = "default",
			f = "index",
			)
		)
	return ()
def quiz_question_view_only(question_row):
	student_id = request.vars.student_id
	if (session.login_type == "TEACHER"):
		if (session.teacher_student_view == "TRUE"):
			back_to_quiz = "student_quiz_teacher_view"
			return_link_anchor = "back to student answers"
		else:
			back_to_quiz = "teacher_quiz"
			return_link_anchor = "back to quiz"
	elif (session.login_type == "STUDENT"):
		back_to_quiz = "student_quiz"
		return_link_anchor = "back to quiz"
	else:
		system_error("role should be either 'STUDENT' or 'TEACHER'")
	question_view = TABLE(
		TR(
			TD(question_row.question, _colspan = "2"),
			),
		TR(
			TD(
				"(A) ",
				),
			TD(
				question_row.option_a,
				),
			),
		TR(
			TD(
				"(B) ",
				),
			TD(
				question_row.option_b,
				),
			),
		TR(
			TD(
				"(C) ",
				),
			TD(
				question_row.option_c,
				),
			),
		TR(
			TD(
				"(D) ",
				),
			TD(
				question_row.option_d,
				),
			),
		TR(
			TD(
				"(E) ",
				),
			TD(
				question_row.option_e,
				),
			),
		TR(
			TD(
				A(
					return_link_anchor,
					_href = URL(
						a = "school",
						c = "default",
						f = back_to_quiz,
						vars = dict(
							quiz_id = question_row.quiz_id,
							student_id = student_id,
							),
						)
					), 
				_colspan = "2",
				),
			),
		)
	return (question_view)
def session_manager(instance):
	if (
		(
			(session.login_type == None)
			and
			(instance.function not in public_pages)
			)
		or
		(
			(session.login_type == "STUDENT")
			and
			(instance.function not in student_pages)
			)
		or
		(
			(session.login_type == "TEACHER")
			and
			(instance.function not in teacher_pages)
			)
		or
		(
			(session.login_type == "ADMINISTRATOR")
			and
			(instance.function not in administrator_pages)
			)
		):
		logout()
	if (session.portal_user == None):
		session.portal_user = ""
		session.portal_greeting = ""
	session.page_heading = page_headings[instance.function]
	if (session.portal_user != ""):
		session.portal_greeting = "Hello, "
		session.exit_option = A(
			"Log Out",
			_href = URL(
				a = "school",
				c = "default",
				f = "logout",
				)
			)
	else:
		session.exit_option = ""
	if (instance.function != "operational_error"):
		session.operational_error = ""
	else:
		if (session.operational_error_token != True):
			redirect(
				URL(
					a = "school",
					c = "default",
					f = "logout",
					)
				)
	if (instance.function == "create_quiz"):
		if (session.quiz_under_development != None):
			redirect(
				URL(
					a = "school",
					c = "default",
					f = "add_question_to_quiz",
					)
				)
	if (instance.function == "add_question_to_quiz"):
		if (session.quiz_under_development == None):
			redirect(
				URL(
					a = "school",
					c = "default",
					f = "teacher_dashboard",
					)
				)
	if (instance.function != "student_quiz_question"):
		session.question_id_student = None
		session.quiz_id_student = None
	if (instance.function != "student_quiz_question"):
		session.question_id_student = None
		session.quiz_id_student = None
	if (instance.function != "teacher_quiz"):
		session.quiz_id_teacher = None
	if (instance.function != "quiz_question_teacher_view"):
		session.teacher_student_view = None
	if (instance.function not in ["add_question_to_quiz", "teacher_quiz"]):
		session.quiz_under_development = None
	return ()
def system_error(error_message):
	session.operational_error_token = True
	session.operational_error = error_message
	redirect(
		URL(
			a = "school",
			c = "default",
			f = "operational_error",
			)
		)
	return ()
def clear_database():
	for table in db.tables:
		if (table != "admins"):
			db[table].truncate()
			db.commit()
	redirect(
		URL(
			a = "school",
			c = "default",
			f = "index",
			)
		)
	return ()

# ------------------------ </AUXILIARY ITEMS & FUNCTIONS - END> ---------------------


