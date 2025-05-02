from .database import db
from sqlalchemy import String, Integer, ForeignKey
from typing import List, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .associations import student_course_association

if TYPE_CHECKING:
    from .teacher import Teacher
    from .student import Student


class Course(db.Model):
    __tablename__ = "courses"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    credits: Mapped[int] = mapped_column(Integer, nullable=False)
    teacher_id: Mapped[int] = mapped_column(
        ForeignKey("teachers.id"), nullable=False)
    made_by_teacher: Mapped['Teacher'] = relationship(
        back_populates="courses"
    )
    students: Mapped[List['Student']] = relationship(
        back_populates="courses",
        secondary=student_course_association
    )

    @classmethod
    def get_courses(cls, include_relations=True):
        try:
            list_courses = cls.query.all()
            if not list_courses:
                print("No hay cursor")
                return []

            if include_relations:
                serialized_courses = [course.serialize_with_relations()
                                      for course in list_courses]
            else:
                serialized_courses = [course.serialize()
                                      for course in list_courses]

            return serialized_courses
        except Exception as e:
            print(f"Error {e}")
            raise

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'credits': self.credits
        }

    def serialize_with_relations(self):
        data = self.serialize()
        data['made_by_teacher'] = self.made_by_teacher.serialize()
        data['students'] = [student.serialize() for student in self.students]
        return data
