from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from config import config

Base = declarative_base()

class Domain(Base):
    __tablename__ = 'domains'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    registrar = Column(String)
    records = relationship("DNSRecord", back_populates="domain")

class DNSRecord(Base):
    __tablename__ = 'dns_records'

    id = Column(Integer, primary_key=True)
    domain_id = Column(Integer, ForeignKey('domains.id'))
    type = Column(String)
    name = Column(String)
    content = Column(String)
    ttl = Column(Integer)

    domain = relationship("Domain", back_populates="records")

def get_session():
    engine = create_engine(config.DATABASE_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()