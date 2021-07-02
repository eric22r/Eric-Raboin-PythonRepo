#!/usr/bin/env python
# coding: utf-8

# In[1]:


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
    CheckConstraint('quantity >= 0', name='quantity_positive')
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
    Column('shipped', Boolean(), default=False)
)

line_items = Table('line_items', metadata,
    Column('line_items_id', Integer(), primary_key=True),
    Column('order_id', ForeignKey('orders.order_id')),
    Column('cookie_id', ForeignKey('cookies.cookie_id')),
    Column('quantity', Integer()),
    Column('extended_cost', Numeric(12,2))
)

engine = create_engine('sqlite:///:memory:')
metadata.create_all(engine)
connection = engine.connect()


# In[2]:


from sqlalchemy import select, insert, update
ins = insert(users).values(
    username="cookiemon",
    email_address="mon@cookie.com",
    phone="111-111-1111",
    password="password"
)
result = connection.execute(ins)


# In[3]:


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
    }
]
result = connection.execute(ins, inventory_list)


# In[4]:


ins = insert(orders).values(user_id=1, order_id=1)
result = connection.execute(ins)
ins = insert(line_items)
order_items = [
    {
    'order_id': 1,
    'cookie_id': 1,
    'quantity': 9,
    'extended_cost': 4.50
    }
]
result = connection.execute(ins, order_items)


# In[5]:


ins = insert(orders).values(user_id=1, order_id=2)
result = connection.execute(ins)
ins = insert(line_items)
order_items = [
    {
    'order_id': 2,
    'cookie_id': 2,
    'quantity': 1,
    'extended_cost': 1.50
    },
    {
    'order_id': 2,
    'cookie_id': 1,
    'quantity': 4,
    'extended_cost': 4.50
    }
]
result = connection.execute(ins, order_items)


# In[6]:


def ship_it(order_id):
    
    s = select([line_items.c.cookie_id, line_items.c.quantity])
    s = s.where(line_items.c.order_id == order_id)
    cookies_to_ship = connection.execute(s)
    for cookie in cookies_to_ship:
        u = update(cookies).where(cookies.c.cookie_id == cookie.cookie_id)
        u = u.values(quantity = cookies.c.quantity - cookie.quantity)
        result = connection.execute(u)
    u = update(orders).where(orders.c.order_id == order_id)
    u = u.values(shipped=True)
    result = connection.execute(u)
    print("Shipped order ID: {}".format(order_id))


# In[7]:


ship_it(1)


# In[8]:


s = select([cookies.c.cookie_name, cookies.c.quantity])
connection.execute(s).fetchall()


# In[9]:


u = update(cookies).where(cookies.c.cookie_name == 'dark chocolate chip')
u = u.values(quantity = 1)
result = connection.execute(u)


# In[10]:


from sqlalchemy.exc import IntegrityError
def ship_id(order_id):
    s = select([line_items.c.cookie_id, line_items.c.quantity])
    s = s.where(line_items.c.order_id == order_id)
    transaction = connection.begin()
    cookies_to_ship = connection.execute(s).fetchall()
    try:
        for cookie in cookies_to_ship:
            u = update(cookies).where(cookies.c.cookie_id == cookie.cookie_id)
            u = u.values(quantity = cookies.c.quantity-cookie.quantity)
            result = connection.execute(u)
        u = update(orders).where(orders.c.order_id == order_id)
        u = u.values(shipped=True)
        result = connection.execute(u)
        print("Shipped order ID: {}".format(order_id))
        transaction.commit()
    except IntegrityError as error:
        transaction.rollback()
        print(error)


# In[11]:


s = select([cookies.c.cookie_name, cookies.c.quantity])
connection.execute(s).fetchall()


# In[12]:


print("Eric Raboin")


# In[13]:


#Saving data from Python without using a database is very possible in a number of ways. Python makes it easy to export
#files and can be exported in many different formats. By doing that, you can create and then export local informataion without
#having to rely on a database to store and keep the records of it. The disadvantage to that is that it becomes much more 
#difficult for someone to read and interpret the information because Python can sort and show you information automatically.
#Some popular export files are excel, html, and graphs.


# In[ ]:




