# The code is essentially creating a database of cookie sale information. It begins by importing all the 
# needed libraries and metadata. It is composed of a series of tables such as cookies, users, orders, 
# and line items, and within those tables are fields dedicated to table specific information. After 
# the declared table name, it specifies what type of data will be held by the field and then if it is
# a primary or foreign key it is specified. There is another field for timestamps, datetime.now and 
# also declaring something as 'nullable=False' states that the field can not be left blank or empty.
print("Eric Raboin - SQL1")
Eric Raboin - SQL1


from sqlalchemy import MetaData
metadata = MetaData()
from datetime import datetime
from sqlalchemy import Table, Column, Integer, Numeric, String, ForeignKey, DateTime
from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:')
cookies = Table('cookies', metadata,
               Column('cookie_id', Integer(), primary_key=True),
               Column('cookie_name', String(50), index=True),
               Column('cookie_recipe_url', String(225)),
               Column('cookie_sku', String(55)),
               Column('quantity', Integer()),
               Column('unit_cost', Numeric(12, 2)) 
            )
users = Table('users', metadata,
             Column('user_id', Integer(), primary_key=True),
             Column('username', String(15), nullable=False, unique=True),
             Column('email_address', String(255), nullable=False),
             Column('phone', String(20), nullable=False),
             Column('password', String(25), nullable=False),
             Column('created_on', DateTime(), default=datetime.now),
             Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now) 
             )
orders = Table('orders', metadata,
              Column('order_id', Integer(), primary_key=True),
              Column('user_id', ForeignKey('users.user_id')),
            )
line_items = Table('line_items', metadata,
                  Column('line_items_id', Integer(), primary_key=True),
                  Column('order_id', ForeignKey('orders.order_id')),
                  Column('cookie_id', ForeignKey('cookies.cookie_id')),
                  Column('quantity', Integer()),
                  Column('extended_cost', Numeric(12, 2)) 
                )
metadata.create_all(engine)

 
