#!/usr/bin/env python
# coding: utf-8

# In[1]:


from datetime import datetime

from sqlalchemy import (MetaData, Table, Column, Integer, Numeric, String,
                       DateTime, ForeignKey, Boolean, create_engine)
metadata = MetaData()

cookies = Table('cookies', metadata,
               Column('cookie_id', Integer, primary_key=True),
               Column('cookie_name', String(50), index=True),
               Column('cookie_recipe_url', String(255)),
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


# In[2]:


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
                  Column('extended_cost', Numeric(12, 2)) 
                )

engine = create_engine('sqlite:///:memory:')
metadata.create_all(engine)


# In[3]:


connection = engine.connect()


# In[4]:


ins = cookies.insert().values(
    cookie_name="chocolate chip",
    cookie_recipe_url="http://some.aweso.me/cookie/recipe.html",
    cookie_sku="CC01",
    quantity="12",
    unit_cost="0.50"
)
print(str(ins))


# In[5]:


ins.compile().params


# In[6]:


result = connection.execute(ins)


# In[7]:


result.inserted_primary_key


# In[8]:


from sqlalchemy import insert
ins = insert(cookies).values(
        cookie_name="chocolate chip",
        cookie_recipe_url="http://some.aweso.me/cookie/recipe.html",
        cookie_sku="CC01",
        quantity="12",
        unit_cost="0.50"
)
str(ins)


# In[10]:


ins = cookies.insert()
result = connection.execute(ins, cookie_name="dark chocolate chip",
        cookie_recipe_url="http://some.aweso.me/cookie/recipe_dark.html",
        cookie_sku="CC02",
        quantity="1",
        unit_cost="0.75")


# In[11]:


result.inserted_primary_key


# In[12]:


inventory_list = [
    {
        'cookie_name': 'peanut butter',
        'cookie_recipe_url': 'http://some.aweso.me/cookie/peanut.html',
        'cookie)sku': 'PB01',
        'quantity': '24',
        'unit_cost': '0.25'
    },
    {
        'cookie_name': 'oatmeal raisin',
        'cookie_recipe_url': 'http://some.aweso.me/cookie/raisin.html',
        'cookie)sku': 'EWW01',
        'quantity': '100',
        'unit_cost': '1.00'
    }
]


# In[13]:


result = connection.execute(ins, inventory_list)


# In[14]:


from sqlalchemy.sql import select


# In[15]:


s = select([cookies])


# In[16]:


str(s)


# In[17]:


rp = connection.execute(s)


# In[18]:


results = rp.fetchall()


# In[19]:


first_row = results[0]


# In[20]:


first_row[1]


# In[21]:


first_row.cookie_name


# In[22]:


first_row[cookies.c.cookie_name]


# In[23]:


s = cookies.select()


# In[24]:


rp = connection.execute(s)


# In[25]:


for record in rp:
    print(record.cookie_name)


# In[26]:


s = select([cookies.c.cookie_name, cookies.c.quantity])
rp = connection.execute(s)
print(rp.keys())
results = rp.fetchall()


# In[27]:


results


# In[28]:


s = select([cookies.c.cookie_name, cookies.c.quantity])
s = s.order_by(cookies.c.quantity, cookies.c.cookie_name)
rp = connection.execute(s)
for cookie in rp:
    print('{} - {}'.format(cookie.quantity, cookie.cookie_name))


# In[35]:


from sqlalchemy import desc
s = select([cookies.c.cookie_name, cookies.c.quantity])
s = s.order_by(desc(cookies.c.quantity))
rp = connection.execute(s)
for cookie in rp:
    print('{} - {}'.format(cookie.quantity, cookie.cookie_name))


# In[37]:


from sqlalchemy.sql import func


# In[38]:


s = select([func.count(cookies.c.cookie_name)])
rp = connection.execute(s)
record = rp.first()
print(record.keys())
print(record.count_1)


# In[39]:


s = select([func.count(cookies.c.cookie_name).label('inventory_count')])
rp = connection.execute(s)
record = rp.first()
print(record.keys())
print(record.inventory_count)


# In[40]:


s = select([cookies]).where(cookies.c.cookie_name == 'chocolate chip')
rp = connection.execute(s)
record = rp.first()
print(record.items())


# In[41]:


s = select([cookies]).where(cookies.c.cookie_name.like('%chocolate%')).where(cookies.c.quantity == 12)
rp = connection.execute(s)
for record in rp.fetchall():
        print(record.cookie_name)


# In[42]:


str(s)


# In[43]:


s=cookies.select(limit=1)


# In[44]:


for row in connection.execute(s):
    print(row)


# In[45]:


s= select([cookies.c.cookie_name, 'SKU-' + cookies.c.cookie_sku])
for row in connection.execute(s):
    print(row)


# In[46]:


s= select([cookies.c.cookie_name, cookies.c.quantity * cookies.c.unit_cost])
for row in connection.execute(s):
    print('{} - {}'.format(row.cookie_name, row.anon_1))


# In[47]:


from sqlalchemy import cast
s= select([cookies.c.cookie_name, cast((cookies.c.quantity * cookies.c.unit_cost), Numeric(12, 2)).label('inv_cost')])
for row in connection.execute(s):
    print('{} - {}'.format(row.cookie_name, row.inv_cost))


# In[48]:


from sqlalchemy import and_, or_, not_
s = select([cookies]).where(and_(
    cookies.c.quantity > 23,
    cookies.c.unit_cost < 0.40
))
for row in connection.execute(s):
    print(row.cookie_name)


# In[49]:


from sqlalchemy import and_, or_, not_
s = select([cookies]).where(or_(
    cookies.c.quantity.between(10, 50),
    cookies.c.cookie_name.contains('chip')
))
for row in connection.execute(s):
    print(row.cookie_name)


# In[50]:


from sqlalchemy import update
u = update(cookies).where(cookies.c.cookie_name == "chocolate chip")
u = u.values(quantity=(cookies.c.quantity + 120))
result = connection.execute(u)
print(result.rowcount)


# In[51]:


s = select([cookies]).where(cookies.c.cookie_name == "chocolate chip")
result = connection.execute(s).first()
for key in result.keys():
    print('{:>20}: {}'.format(key, result[key]))


# In[52]:


from sqlalchemy import delete
u = delete(cookies).where(cookies.c.cookie_name == "dark chocolate chip")
result = connection.execute(u)
print(result.rowcount)
s = select([cookies]).where(cookies.c.cookie_name == "dark chocolate chip")
result = connection.execute(s).fetchall()
print(len(result))


# In[53]:


print(result)


# In[54]:


customer_list = [
    {
        'username': "cookiemon",
        'email_address': "mon@cookie.com",
        'phone': "111-111-1111",
        'password': "password"
    },
        {
        'username': "cakeeater",
        'email_address': "cakeeater@cake.com",
        'phone': "222-222-2222",
        'password': "password"
    },
        {
        'username': "pieguy",
        'email_address': "guy@pie.com",
        'phone': "333-333-3333",
        'password': "password"
    }
]


# In[55]:


ins = users.insert()
result = connection.execute(ins, customer_list)


# In[56]:


ins = insert(orders).values(user_id=1, order_id=1)
result = connection.execute(ins)


# In[57]:


ins = insert(line_items)
order_items = [
    {
        'order_id': 1,
        'cookie_id': 1,
        'quantity': 2,
        'extended_cost': 1.00
    },
    {
        'order_id': 1,
        'cookie_id': 3,
        'quantity': 12,
        'extended_cost': 3.00
    }
]
result = connection.execute(ins, order_items)


# In[58]:


ins = insert(orders).values(user_id=2, order_id=2)
result = connection.execute(ins)


# In[59]:


ins = insert(line_items)
order_items = [
    {
        'order_id': 2,
        'cookie_id': 1,
        'quantity': 24,
        'extended_cost': 12.00
    },
    {
        'order_id': 2,
        'cookie_id': 4,
        'quantity': 6,
        'extended_cost': 6.00
    }
]
result = connection.execute(ins, order_items)


# In[60]:


columns = [orders.c.order_id, users.c.username, users.c.phone, cookies.c.cookie_name,
          line_items.c.quantity, line_items.c.extended_cost]
cookiemon_orders = select(columns)
cookiemon_orders = cookiemon_orders.select_from(users.join(orders).join(line_items).join(cookies)).where(users.c.username == 'cookiemon')
result = connection.execute(cookiemon_orders).fetchall()
for row in result:
    print(row)


# In[61]:


str(cookiemon_orders)


# In[62]:


columns = [users.c.username, orders.c.order_id]
all_orders = select(columns)
all_orders = all_orders.select_from(users.outerjoin(orders))
result = connection.execute(all_orders).fetchall()
for row in result:
    print(row)


# In[63]:


columns = [users.c.username, func.count(orders.c.order_id)]
all_orders = select(columns)
all_orders = all_orders.select_from(users.outerjoin(orders)).group_by(users.c.username)
print(str(all_orders))
result = connection.execute(all_orders).fetchall()
for row in result:
    print(row)


# In[64]:


def get_orders_by_customer(cust_name):
    columns = [orders.c.order_id, users.c.username, users.c.phone, cookies.c.cookie_name, line_items.c.quantity, line_items.c.extended_cost]
    cust_orders = select(columns)
    cust_orders = cust_orders.select_from(users.join(orders).join(line_items).join(cookies)).where(users.c.username == cust_name)
    result = connection.execute(cust_orders).fetchall()
    return result


# In[65]:


get_orders_by_customer('cakeeater')


# In[66]:


def get_orders_by_customer(cust_name, shipped=None, details=False):
    columns = [orders.c.order_id, users.c.username, users.c.phone]
    joins = users.join(orders)
    if details:
        columns.extend([cookies.c.cookie_name, line_items.c.quantity, line_items.c.extended_cost])
        joins=joins.join(line_items).join(cookies)
    cust_orders = select(columns)
    cust_orders = cust_orders.select_from(joins).where(users.c.username == cust_name)
    if shipped is not None:
        cust_orders = cust_orders.where(orders.c.shipped == shipped)
    result = connection.execute(cust_orders).fetchall()
    return result


# In[67]:


get_orders_by_customer('cakeeater')


# In[68]:


get_orders_by_customer('cakeeater', details=True)


# In[69]:


get_orders_by_customer('cakeeater', shipped=True)


# In[70]:


get_orders_by_customer('cakeeater', shipped=False)


# In[71]:


get_orders_by_customer('cakeeater', shipped=False, details=True)


# In[72]:


result = connection.execute("select * from orders").fetchall()
print(result)


# In[73]:


from sqlalchemy import text
stmt = select([users]).where(text('username="cookiemon"'))
print(connection.execute(stmt).fetchall())


# In[74]:


# There are several similarities between sending SQL requests between Python vs 
# other programming languages, however, there are also key differences as well.
# For starters, the python languages seems much more friendly in a sense
# that it is fairly easy for people to read and understand the information in the code.
# Using a language such as C# which is static means it is a build and compile language whereas
# python is more dynamic. The syntax of python also seems more consistant than C#. Both languages operate
# similarly in the way and method that they request the SQL information, however python has become very popular
# due to its readability, dynamic abilities, and consistent syntax.


# In[75]:


print("Eric Raboin SQL2")


# In[ ]:




