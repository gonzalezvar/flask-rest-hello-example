from .database import db
from sqlalchemy import String, Integer
from typing import List,TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .course import Course

class Teacher(db.Model):
    __tablename__ = "teachers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    last_name: Mapped[str] = mapped_column(String(250), nullable=False)
    courses: Mapped[List['Course']] = relationship(
        back_populates="made_by_teacher"
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