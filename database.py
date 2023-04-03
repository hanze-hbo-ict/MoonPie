from sqlalchemy import create_engine, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, Column, String, Float, Text
from sqlalchemy.orm import Session

from werkzeug.security import generate_password_hash, check_password_hash


base = declarative_base()
engine = create_engine('sqlite:///minerals_sqlalchemy.sqlite')

class Mineral(base):
   __tablename__='minerals'
   id = Column(Integer, primary_key=True)
   name = Column(String)
   molmass = Column(Float)
   formula = Column(String)
   description = Column(Text)
   price = Column(Float)

   def __init__(self, name, molmass, formula, description, price):
        self.name = name
        self.molmass = molmass
        self.formula = formula
        self.description = description
        self.price = price


from flask_login import UserMixin
class Customer(base, UserMixin):

   __tablename__='customers'
   id = Column(Integer, primary_key=True)
   name = Column(String)
   password = Column(String)
   email = Column(String)

   def __init__(self, name, password, email):
       self.name = name
       self.email = email
       self.password = generate_password_hash(password)

   def check_password(self, pw):
        return check_password_hash(self.password, pw)


   def get_customer_by_id(user_id):
       sess = Session(bind=engine)
       user = sess.query(Customer).filter_by(id=user_id)
       #print (user.first())
       return user.first()

   def get_name(self):
       return f'{self.name} with password {self.password}'
   
   


bestellingen = Table ('bestellingen', base.metadata,
    Column('customer_id', ForeignKey('customers.id'), primary_key=True),
    Column('mineral_id',  ForeignKey('minerals.id'), primary_key=True),
    Column('amount', Integer)
)


def get_minerals():
    sess = Session(bind=engine)
    minerals = sess.query(Mineral).all()
    rv = []
    for min in minerals:
        rv.append(min)
    return rv

def check_user(credentials):
    sess = Session(bind=engine)
    user = sess.query(Customer).filter(
        Customer.name==credentials['u_name']
    ).first()

    if user is None:
        return False

    if  user.check_password(credentials['u_password']) \
        and user is not None:
        return user
    return False

def save_user(data):
    n_user = Customer(name=data['u_name'], password=data['u_pass'], email=data['u_email'])
    sess = Session(bind=engine)
    sess.add(n_user)
    sess.commit()
    print (n_user.id)
    return n_user.id


def get_user_by_id(user_id):
    sess = Session(bind=engine)
    user = sess.query(Customer).filter_by(id=user_id)
    print (user.first())
    return user.first()


if __name__=='__main__':
    base.metadata.create_all(engine)
    minerals = [
        Mineral('diopside', 216.55, 'MgCaSi_2O_6', 'Diopside is a monoclinic pyroxene mineral. It forms variably colored, but typically dull green crystals in the monoclinic prismatic class. It has two distinct prismatic cleavages, typical of the pyroxene series. It is transparent to translucent with indices of refraction.', 1.2),
        Mineral('feldspar', 818.76, 'KAlSi_3O_8 – NaAlSi_3O_8 – CaAl_2Si_2O_8', "Feldspars are a group of rock-forming aluminium tectosilicate minerals, containing sodium, calcium, potassium or barium. The most common members of the feldspar group are the plagioclase (sodium-calcium) feldspars and the alkali feldspars. Feldspars make up about 60% of the Earth's crust.", 2.4),
        Mineral('ilmenite', 151.71, 'FeTiO_3', 'Ilmenite is a titanium-iron oxide mineral. It is a weakly magnetic black or steel-gray solid. It is the most important ore of titanium and the main source of titanium dioxide.', 3.14),
        Mineral('olvine',   203.77, '(Mg,Fe)2SiO4', "Olivine is a magnesium iron silicate with a complex chemical formula. The primary component of the Earth's upper mantle, it is a common mineral in Earth's subsurface, but weathers quickly on the surface.", 4.12)
    ]
    #with Session(engine) as sess:
    #    sess.add_all(minerals)
    #    sess.commit()

    bart = {"u_name":"bart", "u_email":'bart@bart.com', "u_pass":'supergeheim'}
    save_user(bart)
    d = {'u_name':'bart','u_password':'supergeheim'}
    b = check_user(d)
    print (b)
    print (b.name)
