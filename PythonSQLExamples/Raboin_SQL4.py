print("Eric Raboin")
Eric Raboin
#You can utilize this example program to create a wide array of innovative programs and apps. You can use this to quickly load
#in massive amounts of data almost instantaneously and organize it however the user would like. For example, you could use this
#with a grocery list app to sory products alphabetically, by category, or even take a meal and tell you what ingredients you 
#need to make it. You can essentially use this to make any type of database and sort or search for information pertaining to it.

from datetime import datetime

from sqlalchemy import (MetaData, Table, Column, Integer, Numeric, String, 
                        DateTime, ForeignKey, Boolean, create_engine, CheckConstraint)

metadata = MetaData()

cookies = Table('cookies', metadata,
               Column('cookie_id', Integer(), primary_key=True),
               Column('cookie_name', String(50), index=True),
               Column('cookie_recipe_url', String(255)),
               Column('cookie_sku', String(55)),
               Column('quantity', Integer()),
               Column('unit_cost', Numeric(12, 2)),
               CheckConstraint('quantity > 0', name='quantity_positive')
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
              Column('order_id', Integer()),
              Column('user_id', ForeignKey('users.user_id')),
              Column('shipped', Boolean(), default=False)
              )

line_items = Table('line_items', metadata,
                  Column('line_items_id', Integer(), primary_key=True),
                  Column('order_id', ForeignKey('orders.order_id')),
                  Column('cookie_id', ForeignKey('cookies.cookie_id')),
                  Column('quantity', Integer()),
                  Column('extended_cost', Numeric(12, 2))
                  )

engine = create_engine('sqlite:///:memory:')
metadata.create_all(engine)
connection = engine.connect()
from sqlalchemy import select, insert
ins = insert(users).values(
    username="cookiemon",
    email_address="mon@cookie.com",
    phone="111-111-1111",
    password="password"
)
result = connection.execute(ins)
s = select([users.c.username])
results = connection.execute(s)
for result in results:
    print(result.username)
    print(result.password)
cookiemon
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
<ipython-input-3-32dc1538af4d> in <module>
      3 for result in results:
      4     print(result.username)
----> 5     print(result.password)

AttributeError: Could not locate column in row for column 'password'
ins = insert(users).values(
    username="cookiemon",
    email_address="damon@cookie.com",
    phone="111-111-1111",
    password="password"
)
result = connection.execute(ins)

ins = insert(users).values(
    username="cookiemon",
    email_address="damon@cookie.com",
    phone="111-111-1111",
    password="password"
)
try:
    result = connection.execute(ins)
except IntegrityError as error:
    print(error.args, error.params)
('(sqlite3.IntegrityError) UNIQUE constraint failed: users.username',) ('cookiemon', 'damon@cookie.com', '111-111-1111', 'password', '2020-01-24 14:00:00.537837', '2020-01-24 14:00:00.537837')
ins = cookies.insert()
inventory_list = [
    {
        'cookie_name': 'chocolate chip',
        'cookie_recipe_url': 'http://some.aweso.me/cookie/recipe.html',
        'cookie_sku': 'CC01',
        'quantity': '12',
        'unit_cost': '0.50'
    },
    {
        'cookie_name': 'dark chocolate chip',
        'cookie_recipe_url': 'http://some.aweso.me/cookie/recipe_dark.html',
        'cookie_sku': 'CC02',
        'quantity': '1',
        'unit_cost': '0.75'
    },
    {
        'cookie_name': 'peanut butter',
        'cookie_recipe_url': 'http://some.aweso.me/cookie/peanut.html',
        'cookie_sku': 'PB01',
        'quantity': '24',
        'unit_cost': '0.25'
    },
    {
        'cookie_name': 'oatmeal raisin',
        'cookie_recipe_url': 'http://some.aweso.me/cookie/raisin.html',
        'cookie_sku': 'EWW01',
        'quantity': '100',
        'unit_cost': '1.00'
    }
]
result = connection.execute(ins, inventory_list)
result.rowcount
4

 
