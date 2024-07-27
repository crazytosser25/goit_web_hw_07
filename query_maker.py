import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from psycopg2 import DatabaseError

from creator.structure import Group, Subject, Professor, Student, Grade


def query_1(s):
    result = s.query(Student).order_by(Student.name).limit(5)
    return [student.name for student in result]

def main(se) -> None:
    query = input('print "e" for exit')
    match query:
        case "e":
            print("Bye!")
            sys.exit(1)
        case "1":
            print(query_1(se))
        case _:
            print("Wrong input.")


if __name__ == '__main__':
    DATABASE = 'postgresql://postgres:mysecretpassword@localhost:5432'
    engine = create_engine(DATABASE)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        main(session)
    except DatabaseError as e:
        print(e)
    finally:
        session.close()
