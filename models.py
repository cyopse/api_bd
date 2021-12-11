from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import delete
from sqlalchemy.sql.schema import ForeignKey


engine = create_engine('sqlite:///medicos.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

class Medicos(Base):
    __tablename__='medicos'
    id = Column(Integer, primary_key=True)
    nome = Column(String(30), index=True)
    idade = Column(Integer)

    def __repr__(self):
        return '<Medico {}>'.format(self.nome)

    def salvar(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

class Especializacoes(Base):
    __tablename__='especializacoes'
    id = Column(Integer, primary_key=True)
    nome = Column(String(80))
    medico_id = Column(Integer, ForeignKey('medicos.id'))
    medico = relationship("Medicos")

    def __repr__(self):
        return '<Especializacoes {}>'.format(self.nome)

    def salvar(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

class Usuarios(Base):
    __tablename__='usuarios'
    id = Column(Integer, primary_key=True)
    login = Column(String(20), unique=True)
    senha = Column(String(20))

    def __repr__(self):
        return '<Usuario {}>'.format(self.login)

    def salvar(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    init_db()
