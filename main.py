import psycopg2 as pg


def create_db():  # создает таблицы

	global cur

	cur.execute('''
	create table if not exists
	Student(
	id integer primary key,
	name varchar(100) not null,
	gpa numeric(10,2),
	birth TIMESTAMPTZ
	);
	''')

	cur.execute('''
	create table if not exists
	Course(
	id integer primary key,
	name varchar(100) not null
	);
	''')

	cur.execute('''
	create table if not exists
	StudentCourse(
	id serial primary key,
	student_id INTEGER REFERENCES Student(id),
	course_id INTEGER REFERENCES  Course(id)
	);
	''')


def add_student(values: dict):

	global cur

	cur.execute("""INSERT INTO Student(id, name, gpa, birth) 
	VALUES (%(id)s, 
	%(name)s, 
	%(gpa)s, 
	%(birth)s)""",
	values)


def add_students(course_id, values: list):

	global cur

	cur.executemany("""INSERT INTO Student(id, name, gpa, birth) 
	VALUES (%(id)s, 
	%(name)s, 
	%(gpa)s, 
	%(birth)s)""",
	values)

	for student in values:
		student_id = student.get('id')
		cur.execute("""INSERT INTO StudentCourse(student_id, course_id) 
			VALUES (%s,	%s)""",	(student_id, course_id))


def get_student(sid):

	global cur

	cur.execute('''
	select * from Student;
	''')

	for s in cur.fetchall():
		if s[0] == sid:
			print(s)


def get_students(course_id):

	global cur

	cur.execute("""
	select s.id, s.name, c.name, c.id from StudentCourse sc
	join Student s on s.id = sc.student_id
	join Course c on c.id = sc.course_id
	""")

	for s in cur.fetchall():
		if s[3] == course_id:
			print(s)


def drop_bd():
	cur.execute('''
	drop table if exists Student CASCADE;
	drop table if exists Course CASCADE;
	drop table if exists StudentCourse CASCADE;
	''')


with pg.connect(database='riabovhomework',
				user='riabovhomework',
				password='1234567890',
				host='pg.codecontrol.ru',
				port=59432) as conn:

	cur = conn.cursor()

	drop_bd()

	create_db()

	courses = [{'id': '1', 'course': 'python'}, {'id': '2', 'course': 'java-script'}, {'id': '3', 'course': 'PHP'}]

	cur.executemany("""INSERT INTO Course(id, name)
	VALUES (%(id)s, %(course)s)""",	courses)

	student1 = {'id': '1', 'name': 'Леша', 'gpa': '66666666.66', 'birth': '01.01.2003'}
	student2 = {'id': '2', 'name': 'Петя', 'gpa': '66666666.66', 'birth': '01.01.2004'}
	student3 = {'id': '3', 'name': 'Настя', 'gpa': '66666666.66', 'birth': '01.01.2002'}
	student4 = {'id': '4', 'name': 'Маша', 'gpa': '66666666.66', 'birth': '01.01.2001'}
	students1 = [student1, student2]
	students2 = [student3, student4]
	vasya = {'id': '10', 'name': 'Энокентий', 'gpa': '55555555.55', 'birth': '01.01.1955'}

	add_student(vasya)  # функция создания студента

	add_students('1', students1)  # функция создания студентов и добавления их на курс
	add_students('2', students2)

	print('*Student table --------------------------')
	cur.execute('''
	select * from Student;
	''')
	for s in cur.fetchall():
		print(s)
	print('*Course table ---------------------------')
	cur.execute('''
	select * from Course;
	''')
	for s in cur.fetchall():
		print(s)
	print('*StudentCourse table --------------------')
	cur.execute('''
	select * from StudentCourse;
	''')
	for s in cur.fetchall():
		print(s)
	print('*Get_students() -------------------------')
	get_students(1)  # выводим всех студентов с конкретного курса
	print('*Get_student() --------------------------')
	get_student(10)  # находим одного студента по его id
