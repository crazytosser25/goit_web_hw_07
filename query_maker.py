import sys
import logging
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from psycopg2 import DatabaseError

from creator.structure import Group, Subject, Professor, Student, Grade


logging.basicConfig(level=logging.ERROR)


def query_0(s):
    """test query 1"""
    result = s.query(Student).all()
    # result = s.query(Professor).all()
    # result = s.query(Subject).all()
    # result = s.query(Group).all()
    for i in result:
        print(f" : {i.name}, {i.group_id}")
    """test query 2"""
    # result = (
    #     s.query(
    #         Student.name.label('student_name')
    #     )
    #     .join(Group, Student.group_id == Group.group_id)
    #     .filter(Group.group_id == 2)
    # )
    # logging.debug(str(result))
    # result = result.all()
    # if not result:
    #     print("No results found.")
    # else:
    #     for i in result:
    #         print(f"Student Name: {i.student_name}")


def query_1(s):
    logging.debug("Executing query_1...")
    result = (
        s.query(
            Student.name.label('student_name'),
            func.avg(Grade.grade).label('avg_grade')
        )
        .join(Grade, Student.student_id == Grade.student_id)
        .group_by(Student.student_id)
        .order_by(func.avg(Grade.grade).desc())
        .limit(5)
    )
    logging.debug(str(result))
    result = result.all()

    if not result:
        print("No results found.")
    else:
        for i in result:
            print(f"Student Name: {i.student_name}, Average Grade: {i.avg_grade}")


def query_2(s, subject_id):
    logging.debug("Executing query_2 for subject ID %s...", subject_id)
    result = (
        s.query(
            Student.name.label('student_name'),
            Subject.name.label('subject_name'),
            func.avg(Grade.grade).label('avg_grade')
        )
        .join(Grade, Student.student_id == Grade.student_id)
        .join(Subject, Grade.subject_id == Subject.subject_id)
        .filter(Grade.subject_id == subject_id)
        .group_by(Student.student_id, Subject.name)
        .order_by(func.avg(Grade.grade).desc())
        .limit(1)
    )
    logging.debug(str(result))
    result = result.all()

    if not result:
        print("No results found.")
    else:
        for i in result:
            print(f"Student Name: {i.student_name}, Subject: {i.subject_name}" \
                f", Average Grade: {i.avg_grade}")


def main(sess) -> None:
    query = input('print "e" for exit: ')
    match query:
        case "e":
            print("Bye!")
            sys.exit(1)
        case "0":
            query_0(sess)
        case "1":
            query_1(sess)
        case "2":
            subject_id = int(input('Enter subject ID: '))
            query_2(sess, subject_id)
        case _:
            print("Wrong input.")


if __name__ == '__main__':
    DATABASE = 'postgresql://postgres:mysecretpassword@localhost:5432'
    engine = create_engine(url=DATABASE, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        main(session)
    except DatabaseError as e:
        logging.error(e)
    finally:
        session.close()
