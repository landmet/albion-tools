from sqlalchemy import Column, Boolean, Integer, String, create_engine, ForeignKey, Table, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///albion_items.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class ItemManager:
    def build_db(self):
        Base.metadata.create_all(engine)


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    item_type_id = Column(String)
    prices = relationship("ItemPrice")


class ItemPrice(Base):
    __tablename__ = "itemprices"
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('items.id'))
    item = relationship("Item", back_populates="prices")
    created = Column(DateTime)
    expires = Column(DateTime)
    auction_id = Column(String)
    amount = Column(Integer)
    unit_silver = Column(Integer)
