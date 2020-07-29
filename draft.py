import psycopg2 as pg


def create_db():  # создает таблицы

	global cur

	cur.execute('''
	create table if not exists
	Student4(
	id integer primary key,
	name varchar(100) not null,
	gpa numeric(10,2),
	birth TIMESTAMPTZ
	);
	''')

	cur.execute('''
	create table if not exists
	Course4(
	id integer primary key,
	name varchar(100) not null
	);
	''')

	cur.execute('''
	create table if not exists
	StudentCourse4(
	id serial primary key,
	student_id INTEGER REFERENCES Student4(id),
	course_id INTEGER REFERENCES  Course4(id)
	);
	''')


def add_student(values: dict):

	global cur

	cur.execute("""INSERT INTO Student4(id, name, gpa, birth) 
	VALUES (%(id)s, 
	%(name)s, 
	%(gpa)s, 
	%(birth)s)""",
	values)


def add_students(course_id, values: list):

	global cur

	cur.executemany("""INSERT INTO Student4(id, name, gpa, birth) 
	VALUES (%(id)s, 
	%(name)s, 
	%(gpa)s, 
	%(birth)s)""",
	values)

	for student in values:
		student_id = student.get('id')
		cur.execute("""INSERT INTO StudentCourse4(student_id, course_id) 
			VALUES (%s,	%s)""",	(student_id, course_id))


def drop_bd():
	cur.execute('''
	drop table if exists Student4 CASCADE;
	drop table if exists Course4 CASCADE;
	drop table if exists StudentCourse4 CASCADE;
	''')


with pg.connect(database='riabowdb1', user='riabowdb1', password='1234567890',
				host='pg.codecontrol.ru', port=59432) as conn:

	cur = conn.cursor()

	# drop_bd()

	# create_db()

	courses = [{'id': '1', 'course': 'python'}, {'id': '2', 'course': 'java-script'}, {'id': '3', 'course': 'PHP'}]
	# cur.executemany("""INSERT INTO Course4(id, name)
	# 	VALUES (%(id)s, %(course)s)""",	courses)
	student1 = {'id': '1', 'name': 'petya1', 'gpa': '66666666.66', 'birth': '01.01.2666'}
	student2 = {'id': '2', 'name': 'petya2', 'gpa': '66666666.66', 'birth': '01.01.2666'}
	student3 = {'id': '3', 'name': 'petya3', 'gpa': '66666666.66', 'birth': '01.01.2666'}
	student4 = {'id': '4', 'name': 'petya4', 'gpa': '66666666.66', 'birth': '01.01.2666'}
	students1 = [student1, student2]
	students2 = [student3, student4]
	# add_students('1', students1)
	add_students('2', students2)
	vasya = {'id': '10', 'name': 'vasya', 'gpa': '55555555.55', 'birth': '01.01.2666'}
	# add_student(vasya)


	cur.execute('''
	select * from Student4;
	''')

	for s in cur.fetchall():
		print(s)

	cur.execute('''
	select * from Course4;
	''')

	for s in cur.fetchall():
		print(s)

	cur.execute('''
	select * from StudentCourse4;
	''')

	for s in cur.fetchall():
		print(s)
