from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Date, Float, Text
from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy import select
from sqlalchemy.orm import relationship, Session

base = declarative_base()
engine = create_engine('sqlite:///moonpie.sqlite')

class Mineral(base):
   __tablename__='minerals'
   id = Column(Integer, primary_key=True)
   name = Column(String, nullable=False)
   mollmass = Column(Float)
   formula = Column(String)
   description = Column(Text)
   price = Column(Float)

user_bestellingen = Table('user_bestelling', base.metadata,
     Column('user_id', ForeignKey('user.id'), primary_key=True),
     Column('bestelling_id', ForeignKey('bestelling.id'), primary_key=True)
)

class User(base):
   __tablename__='user'
   id = Column(Integer, primary_key=True)
   name = Column(String, nullable=False)
   password = Column(String, nullable=False)
   email = Column(String, nullable=False)

   bestellingen = relationship("Bestelling", secondary=user_bestellingen, 
                               back_populates='users')
   
   def save(self):
      sess = Session(engine)
      print (sess)
      sess.add(self)
      sess.commit()

class Bestelling(base):
   __tablename__ = 'bestelling'
   id = Column(Integer, primary_key=True)
   datum = Column(Date)
   aantal = Column(Integer)

   users = relationship("User", secondary=user_bestellingen, 
                               back_populates='bestellingen')

data = [ ('diopside', 216.55, 'MgCaSi_2O_6', 'Diopside is a monoclinic pyroxene mineral. It forms variably colored, but typically dull green crystals in the monoclinic prismatic class. It has two distinct prismatic cleavages, typical of the pyroxene series. It is transparent to translucent with indices of refraction.', 1.2),
    ('feldspar', 818.76, 'KAlSi_3O_8 – NaAlSi_3O_8 – CaAl_2Si_2O_8', "Feldspars are a group of rock-forming aluminium tectosilicate minerals, containing sodium, calcium, potassium or barium. The most common members of the feldspar group are the plagioclase (sodium-calcium) feldspars and the alkali feldspars. Feldspars make up about 60% of the Earth's crust.", 2.4),
    ('ilmenite', 151.71, 'FeTiO_3', 'Ilmenite is a titanium-iron oxide mineral. It is a weakly magnetic black or steel-gray solid. It is the most important ore of titanium and the main source of titanium dioxide.', 3.14),
    ('olvine',   203.77, '(Mg,Fe)2SiO4', "Olivine is a magnesium iron silicate with a complex chemical formula. The primary component of the Earth's upper mantle, it is a common mineral in Earth's subsurface, but weathers quickly on the surface.", 4.12) ]

if __name__=='__main__':
   base.metadata.create_all(engine)