import sys
import logging
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from psycopg2 import DatabaseError

from creator.structure import Group, Subject, Professor, Student, Grade


logging.basicConfig(level=logging.ERROR)


def select_1(s):
    """Знайти 5 студентів із найбільшим середнім балом з усіх предметів."""
    logging.debug("Executing select_1.")
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
            print(
                f"Student name: {i.student_name}\t" \
                f"Avg grade: {round(i.avg_grade, 2)}"
            )


def select_2(s, subject_id):
    """Знайти студента із найвищим середнім балом з певного предмета."""
    logging.debug("Executing select_2 for subject ID %s.", subject_id)
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
            print(f"Student name: {i.student_name}\n" \
                f"Subject: {i.subject_name}\n" \
                f"Avg grade: {round(i.avg_grade, 2)}")

def select_3(s, subject_id):
    """Знайти середній бал у групах з певного предмета."""
    logging.debug("Executing select_3 for subject ID %s.", subject_id)
    result = (
        s.query(
                Group.name.label('group_name'),
                func.avg(Grade.grade).label('avg_grade')
            )
            .join(Student, Student.group_id == Group.group_id)
            .join(Grade, Grade.student_id == Student.student_id)
            .join(Subject, Grade.subject_id == Subject.subject_id)
            .filter(Subject.subject_id == subject_id)
            .group_by(Group.name)
    )
    logging.debug(str(result))
    result = result.all()

    if not result:
        print("No results found.")
    else:
        for i in result:
            print(f"Group: {i.group_name}\t" \
                f"Avg grade: {round(i.avg_grade, 2)}")

def select_4(s):
    """Знайти середній бал на потоці (по всій таблиці оцінок)."""
    logging.debug("Executing select_4.")
    result = (s.query(func.avg(Grade.grade).label('average_grade')).scalar())
    logging.debug(str(result))

    if not result:
        print("No results found.")
    else:
        print(f"Avg grade: {round(result, 3)}")

def select_5(s, professor_id):
    """Знайти які курси читає певний викладач."""
    logging.debug("Executing select_5 for professor ID %s.", professor_id)

    result = (
        s.query(Subject.name.label('course_name'))
            .join(Professor, Subject.subject_id == Professor.subject_id)
            .filter(Professor.professor_id == professor_id)
        ).all()

    logging.debug("SQL Query Result: %s", result)
    if not result:
        print("No courses found for this professor.")
    else:
        print(f"Subjects taught by professor with ID {professor_id}:")
        for i in result:
            print(f"- {i.course_name}")

def select_6(s, group_id):
    """Знайти список студентів у певній групі."""
    logging.debug("Executing select_6 for group ID %s.", group_id)

    result = (
        s.query(Student.name.label('student_name'))
            .filter(Student.group_id == group_id)
        ).all()

    logging.debug("SQL Query Result: %s", result)
    if not result:
        print("No groups found for this ID.")
    else:
        print(f"Students in group with ID {group_id}:")
        for i in result:
            print(f"- {i.student_name}")

def select_7(s, group_id, subject_id):
    """Знайти оцінки студентів у певній групі з певного предмета."""
    logging.debug(
        "Executing select_7 for group ID %s and subj ID %s.",
        group_id,
        subject_id
    )

    result = (
        s.query(
            Student.name.label('student_name'),
            func.avg(Grade.grade).label('avg_grade')
        )
        .join(Group, Student.group_id == Group.group_id)
        .join(Grade, Student.student_id == Grade.student_id)
        .join(Subject, Grade.subject_id == Subject.subject_id)
        .filter(Group.group_id == group_id)
        .filter(Subject.subject_id == subject_id)
        .group_by(Student.name)
    ).all()

    logging.debug("SQL Query Result: %s", result)

    if not result:
        print("No grades found for this group and subject.")
    else:
        print(f"Grades for students in group {group_id} for subj {subject_id}:")
        for i in result:
            print(f"Student: {i.student_name},\tGrade: {round(i.avg_grade, 2)}")

def select_8(s, professor_id):
    """Знайти середній бал, який ставить певний викладач зі своїх предметів."""
    logging.debug("Executing select_8 for professor ID %s.", professor_id)
    result = (
        s.query(func.avg(Grade.grade).label('average_grade'))
        .join(Professor, Grade.professor_id == Professor.professor_id)
        .filter(Professor.professor_id == professor_id)
        .scalar()
    )

    logging.debug("SQL Query Result: %s", result)

    if result is None:
        print("No grades found for this professor.")
    else:
        print(f"Average grade from professor is: {round(result, 3)}")

def select_9(s, student_id):
    """Знайти список курсів, які відвідує певний студент."""
    logging.debug("Executing select_8 for student ID %s.", student_id)

    result = (
        s.query(Subject.name.label('course_name'))
        .join(Grade, Subject.subject_id == Grade.subject_id)
        .join(Student, Grade.student_id == Student.student_id)
        .filter(Student.student_id == student_id)
        .distinct()
    ).all()
    logging.debug("SQL Query Result: %s", result)

    if not result:
        print("No courses found for this student.")
    else:
        print(f"Courses attended by student with ID {student_id}:")
        for i in result:
            print(f"- {i.course_name}")

def select_10(s, student_id, professor_id):
    """Знайти список курсів, які певному студенту читає певний викладач."""
    logging.debug(
        "Executing select_7 for student ID %s and proff ID %s.",
        student_id,
        professor_id
    )

    result = (
        s.query(Subject.name.label('course_name'))
        .join(Grade, Subject.subject_id == Grade.subject_id)
        .join(Student, Grade.student_id == Student.student_id)
        .join(Professor, Grade.professor_id == Professor.professor_id)
        .filter(Student.student_id == student_id)
        .filter(Professor.professor_id == professor_id)
        .distinct()
    ).all()
    logging.debug("SQL Query Result: %s", result)

    if not result:
        print("No courses found for this student taught by this professor.")
    else:
        print(f"Courses for student with ID {student_id}" \
            f" by professor with ID {professor_id}:"
        )
        for i in result:
            print(f"- {i.course_name}")


def main(session) -> None:
    RUN = True
    while RUN:
        query = input('\nSelect query option(1 to 10)\nor enter "q" to exit:  ')
        match query:
            case "q":
                print("Bye!")
                RUN = False
                sys.exit(1)
            case "1":
                select_1(session)
            case "2":
                subject_id = int(input('Enter subject ID: '))
                select_2(session, subject_id)
            case "3":
                subject_id = int(input('Enter subject ID: '))
                select_3(session, subject_id)
            case "4":
                select_4(session)
            case "5":
                professor_id = int(input('Enter professor ID: '))
                select_5(session, professor_id)
            case "6":
                group_id = int(input('Enter group ID: '))
                select_6(session, group_id)
            case "7":
                group_id = int(input('Enter group ID: '))
                subject_id = int(input('Enter subject ID: '))
                select_7(session, group_id, subject_id)
            case "8":
                professor_id = int(input('Enter professor ID: '))
                select_8(session, professor_id)
            case "9":
                student_id = int(input('Enter student ID: '))
                select_9(session, student_id)
            case "10":
                student_id = int(input('Enter student ID: '))
                professor_id = int(input('Enter professor ID: '))
                select_10(session, student_id, professor_id)
            case _:
                print("Wrong input.")


if __name__ == '__main__':
    DATABASE = 'postgresql://postgres:mysecretpassword@localhost:5432'
    engine = create_engine(url=DATABASE, echo=False)
    Session = sessionmaker(bind=engine)
    q_session = Session()
    try:
        main(q_session)
    except DatabaseError as e:
        logging.error(e)
    finally:
        q_session.close()
