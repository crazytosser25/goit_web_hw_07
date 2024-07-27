"""Creating tables structure"""
import logging
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship, DeclarativeBase
from psycopg2 import DatabaseError



class Base(DeclarativeBase):
    """Abstract class for alchemy"""
    __abstract__ = True


class Group(Base):
    __tablename__ = 'groups'
    group_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    students = relationship("Student", back_populates="group")

class Student(Base):
    __tablename__ = 'students'
    student_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    group_id = Column(Integer, ForeignKey('groups.group_id'))
    group = relationship("Group", back_populates='students')
    grades = relationship("Grade", back_populates='student')

class Subject(Base):
    __tablename__ = 'subjects'
    subject_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    professors = relationship("Professor", back_populates="subject")
    grades = relationship("Grade", back_populates='subject')

class Professor(Base):
    __tablename__ = 'professors'
    professor_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    subject_id = Column(
        Integer,
        ForeignKey('subjects.subject_id'),
        nullable=False
    )
    subject = relationship("Subject", back_populates='professors')
    grades = relationship("Grade", back_populates='professor')

class Grade(Base):
    __tablename__ = 'grades'
    grade_id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.student_id'))
    subject_id = Column(Integer, ForeignKey('subjects.subject_id'))
    professor_id = Column(Integer, ForeignKey('professors.professor_id'))
    grade = Column(Integer, nullable=False)
    date_received = Column(Date, nullable=False)
    student = relationship("Student", back_populates='grades')
    subject = relationship("Subject", back_populates='grades')
    professor = relationship("Professor", back_populates='grades')


def create_structure(engine) -> None:
    try:
        Base.metadata.create_all(engine)

    except DatabaseError as e:
        logging.error(e)
