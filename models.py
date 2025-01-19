from sqlalchemy import Column, Integer, String, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True,unique=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    versions = relationship("Version", back_populates="user")  

class Version(Base):
    __tablename__ = "versions"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True,unique=True)
    minor_version = Column(String,  index=True, nullable=False)
    release_date = Column(Date, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)


    user = relationship("User", back_populates="versions")
   # __table_args__ = (UniqueConstraint('minor_version', name='unique_user_version'))