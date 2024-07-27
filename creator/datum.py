"""Genetates test data into tables."""
import logging
from random import randint
from datetime import datetime, timedelta
from faker import Faker
from psycopg2 import DatabaseError

from creator.structure import Group, Subject, Professor, Student, Grade



def generate_data(session):
    fake = Faker()
    try:

        group_ids = []
        for _ in range(randint(30, 40)):
            group = Group(name=fake.word().capitalize())
            group_ids.append(group.group_id)
            session.add(group)

        session.commit()

        subject_ids = []
        for _ in range(randint(10, 15)):
            subject = Subject(name=fake.job().capitalize())
            subject_ids.append(subject.subject_id)
            session.add(subject)

        session.commit()

        professor_ids = []
        for _ in range(randint(20, 25)):
            prof_name = f"Professor {fake.name()}"
            if len(professor_ids) < len(subject_ids):
                subj_id = len(professor_ids) + 1
            else:
                subj_id = randint(1, len(subject_ids))
            professor = Professor(subject_id=subj_id, name=prof_name)
            professor_ids.append(professor.professor_id)
            session.add(professor)

        session.commit()

        student_ids = []
        for _ in range(randint(350, 450)):
            group = randint(1, len(group_ids))
            student = Student(name=fake.name(), group_id=group)
            student_ids.append(student.student_id)
            session.add(student)

        session.commit()

        start_date = datetime.strptime('2024-01-01', '%Y-%m-%d')
        end_date = datetime.strptime('2024-06-30', '%Y-%m-%d')

        for _ in range(randint(15, 20)):
            for student in range(1, len(student_ids)):
                subject = randint(1, len(subject_ids))
                proff = randint(1, len(professor_ids))
                grade = randint(50, 100)
                random_days = randint(0, (end_date - start_date).days)
                date_received = start_date + timedelta(days=random_days)
                grade_entry = Grade(
                    student_id=student,
                    subject_id=subject,
                    professor_id=proff,
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
