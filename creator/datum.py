"""Genetates test data into tables."""
import logging
from random import randint, choice
from datetime import datetime, timedelta
from faker import Faker
from sqlalchemy.orm import sessionmaker
from psycopg2 import DatabaseError
from creator.structure import Group, Subject, Professor, Student, Grade



def generate_data(engine):
    Session = sessionmaker(bind=engine)
    session = Session()

    fake = Faker()
    try:

        group_ids = []
        for _ in range(randint(30, 40)):
            group = Group(name=fake.word().capitalize())
            session.add(group)
            session.commit()
            group_ids.append(group.group_id)

        subject_ids = []
        for _ in range(randint(10, 15)):
            subject = Subject(name=fake.job().capitalize())
            session.add(subject)
            session.commit()
            subject_ids.append(subject.subject_id)

        professor_ids = []
        for _ in range(randint(20, 25)):
            prof_name = f"Professor {fake.name()}"
            professor = Professor(name=prof_name, subject_id=choice(subject_ids))
            session.add(professor)
            session.commit()
            professor_ids.append(professor.professor_id)

        student_ids = []
        for _ in range(randint(350, 450)):
            student = Student(name=fake.name(), group_id=choice(group_ids))
            session.add(student)
            session.commit()
            student_ids.append(student.student_id)

        start_date = datetime.strptime('2024-01-01', '%Y-%m-%d')
        end_date = datetime.strptime('2024-06-30', '%Y-%m-%d')

        for student in student_ids:
            for _ in range(randint(15, 20)):
                subject = choice(subject_ids)
                grade = randint(50, 100)
                random_days = randint(0, (end_date - start_date).days)
                date_received = start_date + timedelta(days=random_days)
                grade_entry = Grade(
                    student_id=student,
                    subject_id=subject,
                    professor_id=choice(professor_ids),
                    grade=grade,
                    date_received=date_received
                )
                session.add(grade_entry)

        session.commit()

    except DatabaseError as e:
        logging.error(e)
        session.rollback()
    finally:
        session.close()
