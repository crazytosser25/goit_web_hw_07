import sys
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from psycopg2 import DatabaseError

from creator.structure import Group, Subject, Professor, Student, Grade


def query_0(s):
    """test query"""
    result = s.query(Student).all()
    return result


def query_1(s):
    result = (
        s.query(
            Student.name.label('student_name'),
            func.avg(Grade.grade).label('avg_grade')
        )
        .join(Grade, Student.student_id == Grade.student_id)
        .group_by(Student.student_id)
        .order_by(func.avg(Grade.grade).desc())
        .limit(5)
        .all()
    )
    output = ""
    for i in result:
        output += f"Students name: {i.student_name}, Avg grade: {i.avg_grade}\n"
    return output

def main(sess) -> None:
    query = input('print "e" for exit: ')
    match query:
        case "e":
            print("Bye!")
            sys.exit(1)
        case "0":
            print(query_0(sess))
        case "1":
            print(query_1(sess))
        case _:
            print("Wrong input.")


if __name__ == '__main__':
    DATABASE = 'postgresql://postgres:mysecretpassword@localhost:5432'
    engine = create_engine(url=DATABASE, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        main(session)
    except DatabaseError as e:
        print(e)
    finally:
        session.close()
