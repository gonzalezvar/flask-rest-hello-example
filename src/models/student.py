from .database import db
from sqlalchemy import String, Integer
from typing import List, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .associations import student_course_association

if TYPE_CHECKING:
    from .course import Course

class Student(db.Model):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    last_name: Mapped[str] = mapped_column(String(250), nullable=False)
    courses: Mapped[List['Course']] = relationship(
        back_populates="students",
        secondary=student_course_association
    )

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'last_name': self.last_name
        }

    def serialize_with_relations(self):
        data = self.serialize()
        data['courses'] = [course.serialize() for course in self.courses]
        return data