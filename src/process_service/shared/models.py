from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class FileData(Base):
    __tablename__ = 'file_data'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

    def __repr__(self):
        return f"FileData(id={self.id}, name='{self.name}', email='{self.email}')"
