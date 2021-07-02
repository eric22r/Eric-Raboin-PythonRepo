#!/usr/bin/env python
# coding: utf-8

# In[1]:


from datetime import datetime

from sqlalchemy import (MetaData, Table, Column, Integer, Numeric, String,
                       DateTime, ForeignKey, Boolean, create_engine)
metadata = MetaData()

cookies = Table('cookies', metadata,
               Column('cookie_id', Integer(), primary_key=True),
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


# In[2]:


connection = engine.connect()


# In[3]:


ins = cookies.insert().values(
    cookie_name = "chocolate chip",
    cookie_recipe_url="http://some.aweso.me/cookie/recipe.html",
    cookie_sku="CC01",
    quantity="12",
    unit_cost="0.50"
)
print(str(ins))


# In[4]:


ins.compile().params


# In[5]:


result = connection.execute(ins)


# In[6]:


result.inserted_primary_key


# In[7]:


from sqlalchemy import insert
ins = insert(cookies).values(
    cookie_name = "chocolate chip",
    cookie_recipe_url="http://some.aweso.me/cookie/recipe.html",
    cookie_sku="CC01",
    quantity="12",
    unit_cost="0.50"
)
str(ins)


# In[8]:


ins = cookies.insert()
result = connection.execute(ins, cookie_name='dark chocolate chip',
                           cookie_recipe_url='http://some.aweso.me/cookie/recipe_dark.html',
                           cookie_sku='CC02',
                           quantity='1',
                           unit_cost='0.75')


# In[9]:


result.inserted_primary_key


# In[10]:


inventory_list = [
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


# In[11]:


result = connection.execute(ins, inventory_list)


# In[12]:


from sqlalchemy.sql import select


# In[13]:


s = select([cookies])


# In[14]:


str(s)


# In[15]:


rp = connection.execute(s)


# In[16]:


results = rp.fetchall()


# In[17]:


first_row = results[0]


# In[18]:


first_row[1]


# In[19]:


first_row.cookie_name


# In[20]:


first_row[cookies.c.cookie_name]


# In[21]:


s = cookies.select()


# In[22]:


rp = connection.execute(s)


# In[23]:


for record in rp:
    print(record.cookie_name)


# In[24]:


s = select([cookies.c.cookie_name, cookies.c.quantity])
rp = connection.execute(s)
print(rp.keys())
results = rp.fetchall()


# In[25]:


results


# In[26]:


s = select([cookies.c.cookie_name, cookies.c.quantity])
s = s.order_by(cookies.c.quantity, cookies.c.cookie_name)
rp = connection.execute(s)
for cookie in rp:
    print('{} - {}'.format(cookie.quantity, cookie.cookie_name))


# In[27]:


from sqlalchemy import desc
s = select([cookies.c.cookie_name, cookies.c.quantity])
s = s.order_by(desc(cookies.c.quantity))
rp = connection.execute(s)
for cookie in rp:
    print('{} - {}'.format(cookie.quantity, cookie.cookie_name))


# In[28]:


s = select([cookies.c.cookie_name, cookies.c.quantity])
s = s.order_by(cookies.c.quantity)
s = s.limit(2)
rp = connection.execute(s)
print([result.cookie_name for result in rp])


# In[29]:


from sqlalchemy import func


# In[30]:


s = select([func.count(cookies.c.cookie_name)])
rp = connection.execute(s)
record = rp.first()
print(record.keys())
print(record.count_1)


# In[31]:


s = select([func.count(cookies.c.cookie_name).label('inventory_count')])
rp = connection.execute(s)
record = rp.first()
print(record.keys())
print(record.inventory_count)


# In[32]:


s = select([cookies]).where(cookies.c.cookie_name == 'chocolate chip')
rp = connection.execute(s)
for record in rp.fetchall():
    print(record.cookie_name)


# In[33]:


str(s)


# In[34]:


s=cookies.select(limit=1)


# In[35]:


for row in connection.execute(s):
    print(row)


# In[36]:


s= select([cookies.c.cookie_name, 'SKU-' + cookies.c.cookie_sku])
for row in connection.execute(s):
    print(row)


# In[37]:


s= select([cookies.c.cookie_name, cookies.c.quantity * cookies.c.unit_cost])
for row in connection.execute(s):
    print('{} - {}'.format(row.cookie_name, row.anon_1))


# In[38]:


from sqlalchemy import cast
s= select([cookies.c.cookie_name, cast((cookies.c.quantity * cookies.c.unit_cost), Numeric(12,2)).label('inv_cost')])
for row in connection.execute(s):
    print('{} - {}'.format(row.cookie_name, row.inv_cost))


# In[39]:


from sqlalchemy import cast
s= select([cookies.c.cookie_name, (cookies.c.quantity * cookies.c.unit_cost).label('inv_cost')])
for row in connection.execute(s):
    print('{:<25} - {:.2f}'.format(row.cookie_name, row.inv_cost))


# In[40]:


from sqlalchemy import and_, or_, not_
s = select([cookies]).where(and_(
    cookies.c.quantity > 23,
    cookies.c.unit_cost < 0.40
))
for row in connection.execute(s):
    print(row.cookie_name)


# In[41]:


from sqlalchemy import and_, or_, not_
s = select([cookies]).where(or_(
    cookies.c.quantity.between(10,50),
    cookies.c.cookie_name.contains('chip')
))
for row in connection.execute(s):
    print(row.cookie_name)


# In[42]:


from sqlalchemy import update
u = update(cookies).where(cookies.c.cookie_name == "chocolate chip")
u = u.values(quantity=(cookies.c.quantity + 120))
result = connection.execute(u)
print(result.rowcount)


# In[43]:


s = select([cookies]).where(cookies.c.cookie_name == "chocolate chip")
result = connection.execute(s).first()
for key in result.keys():
    print('{:>20}: {}'.format(key, result[key]))


# In[44]:


from sqlalchemy import delete
u = delete(cookies).where(cookies.c.cookie_name == "dark chocolate chip")
result = connection.execute(u)
print(result.rowcount)
s = select([cookies]).where(cookies.c.cookie_name == "dark chocolate chip")
result = connection.execute(s).fetchall()
print(len(result))


# In[45]:


print(result)


# In[46]:


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


# In[47]:


ins = users.insert()
result = connection.execute(ins, customer_list)


# In[48]:


ins = insert(orders).values(user_id=1, order_id=1)
result = connection.execute(ins)


# In[49]:


ins = insert(line_items)
order_items = [
    {
        'order_id': 1,
        'cookie_id': 1,
        'quantity' : 2,
        'extended_cost': 1.00
    },
    {
        'order_id': 1,
        'cookie_id': 3,
        'quantity' : 12,
        'extended_cost': 3.00
    }
]
result = connection.execute(ins, order_items)


# In[50]:


ins = insert(orders).values(user_id=2, order_id=2)
result = connection.execute(ins)


# In[51]:


ins = insert(line_items)
order_items = [
    {
        'order_id': 2,
        'cookie_id': 1,
        'quantity' : 24,
        'extended_cost': 12.00
    },
    {
        'order_id': 2,
        'cookie_id': 4,
        'quantity' : 6,
        'extended_cost': 6.00
    }
]
result = connection.execute(ins, order_items)


# In[52]:


columns = [orders.c.order_id, users.c.username, users.c.phone, cookies.c.cookie_name,
          line_items.c.quantity, line_items.c.extended_cost]

cookiemon_orders = select(columns)
cookiemon_orders = cookiemon_orders.select_from(users.join(orders).join(line_items).join(cookies)).where(users.c.username == 'cookiemon')

result = connection.execute(cookiemon_orders).fetchall()
for row in result:
    print(row)


# In[53]:


str(cookiemon_orders)


# In[54]:


columns = [users.c.username, orders.c.order_id]
all_orders = select(columns)
all_orders = all_orders.select_from(users.outerjoin(orders))
result = connection.execute(all_orders).fetchall()
for row in result:
    print(row)


# In[55]:


columns = [users.c.username, func.count(orders.c.order_id)]
all_orders = select(columns)
all_orders = all_orders.select_from(users.outerjoin(orders)).group_by(users.c.username)
print(str(all_orders))
result = connection.execute(all_orders).fetchall()
for row in result:
    print(row)


# In[56]:


def get_orders_by_customer(cust_name):
    columns = [orders.c.order_id, users.c.username, users.c.phone, cookies.c.cookie_name,
              line_items.c.quantity, line_items.c.extended_cost]
    cust_orders = select(columns)
    cust_orders = cust_orders.select_from(users.join(orders).join(line_items).join(cookies)).where(users.c.username == cust_name)
    result = connection.execute(cust_orders).fetchall()
    return result


# In[57]:


get_orders_by_customer('cakeeater')


# In[58]:


def get_orders_by_customer(cust_name, shipped=None, details=False):
    columns = [orders.c.order_id, users.c.username, users.c.phone]
    joins = users.join(orders)
    if details:
        columns.extend([cookies.c.cookie_name,line_items.c.quantity, line_items.c.extended_cost])
        joins=joins.join(line_items).join(cookies)
    cust_orders = select(columns)
    cust_orders = cust_orders.select_from(joins).where(users.c.username == cust_name)
    if shipped is not None:
        cust_orders = cust_orders.where(orders.c.shipped == shipped)
    result = connection.execute(cust_orders).fetchall()
    return result


# In[59]:


get_orders_by_customer('cakeeater')


# In[60]:


get_orders_by_customer('cakeeater', details=True)


# In[61]:


get_orders_by_customer('cakeeater', shipped=True)


# In[62]:


get_orders_by_customer('cakeeater', details=False)


# In[63]:


get_orders_by_customer('cakeeater', shipped=False, details=True)


# In[64]:


result = connection.execute("select * from orders").fetchall()
print(result)


# In[65]:


from sqlalchemy import text
stmt = select([users]).where(text('username="cookiemon"'))
print(connection.execute(stmt).fetchall())


# In[66]:


print("Eric Raboin")


# In[ ]:




