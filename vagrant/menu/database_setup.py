# sys module for functions and variables to manipulate different parts
# of the python runtime environment
import sys

# Import handy classes for mapper code
from sqlalchemy import Column, ForeignKey, Integer, String

# Used in configuration and class code
from sqlalchemy.ext.declarative import declarative_base

# When we write up our mapper, used to create foreign key relationships
from sqlalchemy.orm import relationship

# Used in configuration code at end of file
from sqlalchemy import create_engine

# Lets SQLAlchemy know that our classes are special SQL classes
Base = declarative_base()

class Restaurant(Base):
    __tablename__ = 'restaurant'
    name = Column(
        String(80),
        nullable = False,
    )
    id = Column(
        Integer,
        primary_key = True
    )

class MenuItem(Base):
    __tablename__ = 'menu_item'
    name = Column(
        String(80),
        nullable = False,
    )
    id = Column(
        Integer,
        primary_key = True
    )
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(80))
    restaurant_id = Column(
        Integer,
        ForeignKey('restaurant.id')
    )
    restaurant = relationship(Restaurant)

## Insert at End of File ##
engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.create_all(engine)
