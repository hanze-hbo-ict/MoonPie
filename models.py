from datetime import datetime
from typing import List
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Table, Text, select
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from sqlalchemy import create_engine
from flask_login import UserMixin
engine = create_engine("sqlite:///minerals.sqlite3", echo=True)

class Base(DeclarativeBase):
    pass

class Mineral(Base):
    __tablename__ = 'minerals'

    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(30))
    mollmass:Mapped[float] = mapped_column(Float)
    formula:Mapped[str] = mapped_column(String(30))
    description:Mapped[str] = mapped_column(Text)
    price:Mapped[float] = mapped_column(Float)

    @classmethod
    def find_all(cls):
        result = []
        with Session(engine) as session:
            stmt = select(cls)
            for mineral in session.scalars(stmt):
                result.append(mineral)
            
        return result



class User(Base, UserMixin):
    __tablename__ = 'users'
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str]= mapped_column(String(50))
    email:Mapped[str]= mapped_column(String(50))
    password:Mapped[str]= mapped_column(String(50))
    
    bestellingen:Mapped[List['Bestelling']] = relationship()
    is_active = True

    def get_id(self):
        return self.id

    def save(self):
        with Session(engine) as session:
            session.add(self)
            session.commit()
            session.refresh(self)

    def __str__(self):
        return f'User({self.name=} <{self.email=}>, {self.id=}'

    @classmethod
    def find(cls, credentials):
        with Session(engine) as session:
           user = session.query(User).where(User.name == credentials['u_name']).first()

           if user is None:
              return False
    
        return True

    @classmethod
    def get_user_by_name(cls, username):
        with Session(engine) as session:
            user = session.query(User).where(
                User.name == username).first()
            return user

    @classmethod
    def get_user_by_id(cls, id):
        with Session(engine) as session:
            user = session.query(User).where(
                User.id == id).first()
            return user


class Bestelling(Base):
    __tablename__ = 'bestellingen'
    user_id:Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    mineral_id:Mapped[int] = mapped_column(ForeignKey('minerals.id'), primary_key=True)
    datum:Mapped[datetime] = mapped_column(DateTime)
    aantal:Mapped[int] = mapped_column(Integer)


if __name__=='__main__':
    data = [ ('diopside', 216.55, 'MgCaSi_2O_6', 'Diopside is a monoclinic pyroxene mineral. It forms variably colored, but typically dull green crystals in the monoclinic prismatic class. It has two distinct prismatic cleavages, typical of the pyroxene series. It is transparent to translucent with indices of refraction.', 1.2),
        ('feldspar', 818.76, 'KAlSi_3O_8 – NaAlSi_3O_8 – CaAl_2Si_2O_8', "Feldspars are a group of rock-forming aluminium tectosilicate minerals, containing sodium, calcium, potassium or barium. The most common members of the feldspar group are the plagioclase (sodium-calcium) feldspars and the alkali feldspars. Feldspars make up about 60% of the Earth's crust.", 2.4),
        ('ilmenite', 151.71, 'FeTiO_3', 'Ilmenite is a titanium-iron oxide mineral. It is a weakly magnetic black or steel-gray solid. It is the most important ore of titanium and the main source of titanium dioxide.', 3.14),
        ('olvine',   203.77, '(Mg,Fe)2SiO4', "Olivine is a magnesium iron silicate with a complex chemical formula. The primary component of the Earth's upper mantle, it is a common mineral in Earth's subsurface, but weathers quickly on the surface.", 4.12) ]

    Base.metadata.create_all(engine)
    # with Session(engine) as session:
    #     for x in data:
    #         mineral = Mineral(name=x[0], mollmass=x[1], formula=x[2], description=x[3], price=x[4] )
    #         print(mineral)
    #         session.add(mineral)
    #     session.commit()

    print(User.get_user_by_name('piet'))

