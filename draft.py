import psycopg2 as pg


def create_db():  # создает таблицы

	global cur

	cur.execute('''
	create table if not exists
	Student4(
	id serial PRIMARY KEY,
	name varchar(100) not null,
	gpa numeric(10,2),
	birth TIMESTAMPTZ
	);
	''')

	cur.execute('''
	create table if not exists
	Course4(
	id serial PRIMARY KEY,
	name varchar(100) not null
	);
	''')

	cur.execute('''
	create table if not exists
	StudentCourse4(
	student_id INTEGER REFERENCES Student3(id),
	course_id INTEGER REFERENCES  Course3(id)
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


def add_students(course, values: list):

	global cur

	cur.executemany("""INSERT INTO Student4(id, name, gpa, birth) 
	VALUES (%(id)s, 
	%(name)s, 
	%(gpa)s, 
	%(birth)s)""",
	values)

	for student in values:
		sid = student.get('id')
		cur.execute("""INSERT INTO StudentInfo2(id, name) 
			VALUES (%s,	%s)""",	(sid, course))


with pg.connect(database='riabowdb1', user='riabowdb1', password='1234567890',
				host='pg.codecontrol.ru', port=59432) as conn:

	cur = conn.cursor()

	# cur.execute('''
	# drop table Student3 CASCADE;
	# drop table Course3 CASCADE;
	# drop table StudentCourse3 CASCADE;
	# ''')

	create_db()

	courses = [{'course': 'python'}, {'course': 'java-script'}, {'course': 'PHP'}]

	# cur.executemany("""INSERT INTO Course4(name)
	# 	VALUES (%(course)s)""",	courses)


	student1 = {'name': 'petya1', 'gpa': '66666666.66', 'birth': '01.01.2666'}
	student2 = {'name': 'petya2', 'gpa': '66666666.66', 'birth': '01.01.2666'}
	student3 = {'name': 'petya3', 'gpa': '66666666.66', 'birth': '01.01.2666'}
	student4 = {'name': 'petya4', 'gpa': '66666666.66', 'birth': '01.01.2666'}
	students = [student1, student2, student3, student4]
	add_students('2', students)
	vasya = {'name': 'vasya', 'gpa': '55555555.55', 'birth': '01.01.2666'}
	add_student(vasya)


	# cur.execute('''
	# select * from Student3;
	# ''')
	#
	# for s in cur.fetchall():
	# 	print(s)

	# cur.execute('''
	# select * from Course3;
	# ''')
	#
	# for s in cur.fetchall():
	# 	print(s)

	# cur.execute('''
	# select * from StudentCourse3;
	# ''')
	#
	# for s in cur.fetchall():
	# 	print(s)
