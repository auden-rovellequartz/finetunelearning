"""
< 6:00am

temp notepad


>>>>>>>>>>>>>>>
[] a teacher should be able to close out the term
[] when a teacher closes out a term all quizzes for that teacher's class shall automatically transition to "submitted" status and shall be graded
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

[] a student shall be able to see their current cumulative grade from submitted quizzes

[] list quiz points in unassigned quizzes list on student dashboard


[] teacher shall be able to return to quiz from unassigned quiz view
[] administrator shall be able to see list of teachers


************** new for later *********************************************

[] after a teacher assigns a quiz, the view of the quiz should change 
from (assigned = FALSE) to (assigned = TRUE)

[] make student drop class more robust

[] we should enforce unique record entry for student and teacher records
**************************************************************************


=================================================================================

[DONE] add capability for teacher to see summary list of student grades per quiz    < 3:15am
[DONE] add capability for teacher to see detailed results of a quiz for any student

[DONE] a student shall be able to see their current cumulative grade from submitted quizzes
[DONE] a teacher should be able to delete an unassigned quiz

[DONE] when a teacher assigns a quiz, it shall be added to the "quizzes in progress" list of each student currently enrolled in the teacher's class
[DONE] when a student submits a quiz, it shall be graded

[DONE] when student enrolls in a class, all assigned quizzes should be added to his/her "quizzes in progress" list
[DONE] populate (visual elements and logic) student quiz view


[DONE] create link to student quiz view from dashboard
[DONE] populate (visual elements and logic) student quiz question view

[DONE] add a get_quiz_name() function to "AUXILIARY ITEMS" section
[DONE] add student's answer to rows of student quiz view

[DONE] a student shall be able to see the details of their graded quizzes (correct answer versus their submitted answer, quiz points, and cumulative points)
[DONE] add capability for a student to drop a class

[DONE] from teacher quiz view, a teacher should be able to to delete a question from unassigned quizzes.
[DONE] from teacher quiz view, a teacher should be able to add a question to unassigned quizzes


ASSUMPTIONS

>>> this is a web-based application;

>>> quizzes are independent of classrooms; for example, one quiz can be assigned to more than one classrooms if a teacher has multiple classes;

>>> a teacher can modify quizzes that have not been assigned; but once assigned, a quiz cannot be modified;

>>> questions on quizzes do not have to have the same grading points value;

>>> quizzes may have different weighing factors on the final grade;

>>> all multiple choice quiz questions shall have five answer options;

>>> if a student can be in more than one classroom; if so, and 
	if the same quize is assigned twice to the same student, 
	the student shall only need to take the quiz once


"""

	db.teachers.insert(
		teacher_id = create_id("TEACHER"),
		name = "Dr. Robert Robinson",
		portal_pswd = "robert123",
		handle = "robert",
		)
	db.commit()
	db.teachers.insert(
		teacher_id = create_id("TEACHER"),
		name = "Dr. May Howard",
		portal_pswd = "may123",
		handle = "may",
		)
	db.commit()
	db.teachers.insert(
		teacher_id = create_id("TEACHER"),
		name = "Dr. Elisa Campos",
		portal_pswd = "elisa123",
		handle = "elisa",
		)
	db.commit()
	db.teachers.insert(
		teacher_id = create_id("TEACHER"),
		name = "Dr. Tim Smith",
		portal_pswd = "tim123",
		handle = "tim",
		)
	db.commit()
	db.teachers.insert(
		teacher_id = create_id("TEACHER"),
		name = "Dr. Paul Sterling",
		portal_pswd = "paul123",
		handle = "paul",
		)
	db.commit()


	db.students.insert(
		student_id = create_id("STUDENT"),
		name = "Roy Carver",
		portal_pswd = "roy123",
		handle = "roy",
		)
	db.commit()
	db.students.insert(
		student_id = create_id("STUDENT"),
		name = "Blake Wheeler",
		portal_pswd = "blake123",
		handle = "blake",
		)
	db.commit()
	db.students.insert(
		student_id = create_id("STUDENT"),
		name = "Bree Summers",
		portal_pswd = "bree123",
		handle = "bree",
		)
	db.commit()
	db.students.insert(
		student_id = create_id("STUDENT"),
		name = "Claire Robbins",
		portal_pswd = "claire123",
		handle = "claire",
		)
	db.commit()
	db.students.insert(
		student_id = create_id("STUDENT"),
		name = "Carl Roth",
		portal_pswd = "carl123",
		handle = "carl",
		)
	db.commit()
	db.students.insert(
		student_id = create_id("STUDENT"),
		name = "Dee Lloyd",
		portal_pswd = "dee123",
		handle = "dee",
		)
	db.commit()
	db.students.insert(
		student_id = create_id("STUDENT"),
		name = "Drew Keller",
		portal_pswd = "drew123",
		handle = "drew",
		)
	db.commit()
	db.students.insert(
		student_id = create_id("STUDENT"),
		name = "Tom Mitchell",
		portal_pswd = "tom123",
		handle = "tom",
		)
	db.commit()
	db.students.insert(
		student_id = create_id("STUDENT"),
		name = "John Smith",
		portal_pswd = "john123",
		handle = "john",
		)
	db.commit()
	db.students.insert(
		student_id = create_id("STUDENT"),
		name = "Todd Sawyer",
		portal_pswd = "todd123",
		handle = "todd",
		)
	db.commit()
	db.students.insert(
		student_id = create_id("STUDENT"),
		name = "Bill Hendrix",
		portal_pswd = "bill123",
		handle = "bill",
		)
	db.commit()
	db.students.insert(
		student_id = create_id("STUDENT"),
		name = "Jessica Owens",
		portal_pswd = "jessica123",
		handle = "jessica",
		)
	db.commit()
	db.students.insert(
		student_id = create_id("STUDENT"),
		name = "Flo Owens",
		portal_pswd = "flo123",
		handle = "flo",
		)
	db.commit()
	db.students.insert(
		student_id = create_id("STUDENT"),
		name = "Jack Ford",
		portal_pswd = "jack123",
		handle = "jack",
		)
	db.commit()
	db.students.insert(
		student_id = create_id("STUDENT"),
		name = "James Casey",
		portal_pswd = "james123",
		handle = "james",
		)
	db.commit()
	db.students.insert(
		student_id = create_id("STUDENT"),
		name = "Li Ming",
		portal_pswd = "li123",
		handle = "li",
		)
	db.commit()
	db.students.insert(
		student_id = create_id("STUDENT"),
		name = "Su Wei",
		portal_pswd = "su123",
		handle = "su",
		)
	db.commit()
	db.students.insert(
		student_id = create_id("STUDENT"),
		name = "Jiang Qiu",
		portal_pswd = "jiang123",
		handle = "jiang",
		)
	db.commit()
	db.students.insert(
		student_id = create_id("STUDENT"),
		name = "Zhou Wang",
		portal_pswd = "zhou123",
		handle = "zhou",
		)
	db.commit()
	db.students.insert(
		student_id = create_id("STUDENT"),
		name = "Mao Zemin",
		portal_pswd = "mao123",
		handle = "mao",
		)
	db.commit()
	db.students.insert(
		student_id = create_id("STUDENT"),
		name = "Kent Rice",
		portal_pswd = "kent123",
		handle = "kent",
		)
	db.commit()
	db.students.insert(
		student_id = create_id("STUDENT"),
		name = "Joan Franklin",
		portal_pswd = "joan123",
		handle = "joan",
		)
	db.commit()
	db.students.insert(
		student_id = create_id("STUDENT"),
		name = "Luke Shannon",
		portal_pswd = "luke123",
		handle = "luke",
		)
	db.commit()
	db.students.insert(
		student_id = create_id("STUDENT"),
		name = "Mark Dixon",
		portal_pswd = "mark123",
		handle = "mark",
		)
	db.commit()
	db.students.insert(
		student_id = create_id("STUDENT"),
		name = "Pearl Whitnety",
		portal_pswd = "pearl123",
		handle = "pearl",
		)
	db.commit()


