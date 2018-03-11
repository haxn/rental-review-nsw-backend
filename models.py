from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base, DeferredReflection
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, func, String, Float
from database import Base, engine
import datetime


class UserModel(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    email = Column(Text)
    fbId = Column(Text, unique=True)
    profilePicture = Column(Text, default='https://s3-ap-southeast-2.amazonaws.com/rental-review-profile-pics/default.jpeg')
    created_date = Column(DateTime, default=datetime.datetime.utcnow)

class ReviewModel(Base):
    __tablename__ = 'review'
    id = Column(Integer, primary_key=True)
    property = relationship("PropertyModel", cascade="all")
    user = relationship("UserModel", cascade="all")

    property_id = Column(Integer, ForeignKey("property.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)

class PropertyModel(Base):
    __tablename__ = 'property'
    id = Column(Integer, primary_key=True)
    agent = relationship("AgentModel", cascade="all")
    company = relationship("CompanyModel", cascade="all")
    address_string = Column(Text)
    lat = Column(Float)
    lng = Column(Float)
    google_maps_id = Column(Text)
    current_agent = Column(Integer, ForeignKey("agent.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    current_company = Column(Integer, ForeignKey("company.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    current_owner = Column(Text)
    last_known_sold_date = Column(DateTime)


class AgentModel(Base):
    __tablename__ = 'agent'
    id = Column(Integer, primary_key=True)
    company = relationship("CompanyModel", cascade="all")
    name = Column(Text)
    company_id = Column(Integer, ForeignKey("company.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    rating = Column(Float)


class CompanyModel(Base):
    __tablename__ = 'company'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    rating = Column(Float)
