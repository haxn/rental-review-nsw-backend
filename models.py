from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base, DeferredReflection
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, func, String, Float, DateTime, Boolean, Table
from database import Base, engine
import datetime


class UserModel(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    email = Column(Text)
    fbId = Column(Text, unique=True)
    profilePicture = Column(
        Text, default='https://s3-ap-southeast-2.amazonaws.com/rental-review-profile-pics/default.jpeg')
    createdDate = Column(DateTime, default=datetime.datetime.utcnow)


class ReviewModel(Base):
    __tablename__ = 'review'
    id = Column(Integer, primary_key=True)
    property = relationship("PropertyModel", cascade="all")
    user = relationship("UserModel", cascade="all")
    propertyId = Column(Integer, ForeignKey(
        "property.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    userId = Column(Integer, ForeignKey(
        "user.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    startDate = Column(DateTime)
    endDate = Column(DateTime)
    weeklyRent = Column(Float)
    bond = Column(Float)
    bondReturned = Column(Boolean)
    propertyRating = Column(Float)
    neighbourRating = Column(Float)
    phoneReception = Column(Float)
    comments = Column(Text)


class PropertyModel(Base):
    __tablename__ = 'property'
    id = Column(Integer, primary_key=True)
    agent = relationship("AgentModel", cascade="all")
    company = relationship("AgencyModel", cascade="all")
    addressString = Column(Text)
    lat = Column(Float)
    lng = Column(Float)
    googlePlacesId = Column(Text)
    currentAgent = Column(Integer, ForeignKey(
        "agent.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=True)
    currentAgency = Column(Integer, ForeignKey(
        "agency.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=True)


agent_identifier = Table('agent_identifier',
                         Base.metadata,
                         Column('agentId', Integer,
                                ForeignKey('agent.id')),
                         Column('agencyId', Integer,
                                ForeignKey('agency.id'))
                         )


class AgentModel(Base):
    __tablename__ = 'agent'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    agentAvatarUrl = Column(Text)
    brandColour = Column(Text)
    emailAddress = Column(Text)
    phoneNumber = Column(Text)
    domainProfileUrl = Column(Text)
    domainId = Column(Text, unique=True)


class AgentRatingModel(Base):
    __tablename__ = 'agentRating'
    id = Column(Integer, primary_key=True)
    agent = relationship("AgentModel", cascade="all")
    agentId = Column(Integer, ForeignKey(
        "agent.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    rating = Column(Float)


class AgencyModel(Base):
    __tablename__ = 'agency'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    suburb = Column(Text)
    countryName = Column(Text)
    address1 = Column(Text)
    address2 = Column(Text)
    telephone = Column(Text)
    rentalTelephone = Column(Text)
    mobile = Column(Text)
    fax = Column(Text)
    state = Column(Text)
    description = Column(Text)
    email = Column(Text)
    rentalEmail = Column(Text)
    numberForRent = Column(Text)
    domainUrl = Column(Text)
    agencyLogoUrl = Column(Text)
    domainId = Column(Text)
    agentIds = relationship("AgentModel", cascade="all",
                            secondary=agent_identifier)
