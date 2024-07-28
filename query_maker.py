"""Code to make querrys to univercity database using commands in terminal."""
import os
import sys
import logging
from dotenv import load_dotenv
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

def help_string() -> str:
    """Returns list if commands for script.

    Returns:
        str: Help text
    """
    return "\n'1' - Find 5 students with the highest GPA across all subjects." \
        "\n'2' - Find the student with the highest GPA in a particular subject." \
        "\n'3' - Find the average score in groups for a certain subject." \
        "\n'4' - Find the average score across the entire scoreboard." \
        "\n'5' - Find what courses a particular teacher teaches." \
        "\n'6' - Find a list of students in a specific group." \
        "\n'7' - Find the grades of students in a separate group for " \
            "a specific subject." \
        "\n'8' - Find the avg score given by a certain teacher in his subjects." \
        "\n'9' - Find a list of courses that a particular student is taking." \
        "\n'10' - A list of courses taught to a specific student by a specific teacher."


def main(session) -> None:
    """A command-line interface to interact with a database.

    Args:
        session (_type_): The SQLAlchemy session object used for database operations.

    This program provides a simple command-line interface that allows users to perform various queries on a database using input options. It uses the `session` argument to execute these queries.

    Here's an overview of how the program works:
    1. The function starts by printing a welcome message and indicating it is ready to work.
    2. A while loop is used to continuously prompt the user for query input until they choose to exit.
    3. Users can select from 10 different options, each corresponding to a specific database operation. They are presented with these options in the command line.
    4. Depending on the selected option, the program prompts the user for additional information (e.g., IDs) and calls the appropriate function to execute the query.
    5. If an invalid input is entered, a warning message is displayed, and the help string is printed again.
    6. The loop ends when the user enters 'q' or 'Q', indicating they want to exit the program. A goodbye message is then printed before the program exits.
    """
    run = True
    print("Hello! Ready to work.")
    print(help_string())
    while run:
        query = input(
            "\nSelect query option(1 to 10)." \
            "\nEnter 'h' for query list"
            "\nor enter 'q' to exit." \
            "\n --> :").strip().lower()
        match query:
            case "q":
                print("Bye!")
                run = False
                sys.exit(1)
            case "h" | "help":
                print(help_string())
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
                print(help_string())


if __name__ == '__main__':
    load_dotenv()
    database = os.getenv("DATABASE")
    engine = create_engine(url=database, echo=False)
    Session = sessionmaker(bind=engine)
    q_session = Session()
    try:
        main(q_session)
    except DatabaseError as e:
        logging.error(e)
    finally:
        q_session.close()
