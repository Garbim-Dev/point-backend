from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Empresa(Base):
    __tablename__ = "empresas"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    telefone = Column(String)
    alocacoes = relationship("Alocacao", back_populates="empresa")

class Gestor(Base):
    __tablename__ = "gestores"
    
    id = Column(Integer, primary_key=True, index=True) # Este é o Código do Gestor
    nome = Column(String, nullable=False)
    funcao = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False) # unique=True impede e-mails duplicados
    telefone = Column(String, nullable=True)
    senha = Column(String, nullable=False) # Essencial para o Login!

class Professor(Base):
    __tablename__ = "professores"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    matricula = Column(String, unique=True)
    area_atuacao = Column(String)
    email = Column(String)
    telefone = Column(String)
    alocacoes = relationship("Alocacao", back_populates="professor")

class Sala(Base):
    __tablename__ = "salas"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    bloco_andar = Column(String, nullable=True)
    capacidade = Column(Integer)
    alocacoes = relationship("Alocacao", back_populates="sala")

class Curso(Base):
    __tablename__ = "cursos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    carga_horaria = Column(Integer)
    alocacoes = relationship("Alocacao", back_populates="curso")

class Modalidade(Base):
    __tablename__ = "modalidades"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    # AQUI: Deve apontar para "modalidade" (o nome da variável na classe Alocacao)
    alocacoes = relationship("Alocacao", back_populates="modalidade")

class Disciplina(Base):
    __tablename__ = "disciplinas"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    carga_horaria = Column(Integer)
    alocacoes = relationship("Alocacao", back_populates="disciplina")

class Turno(Base):
    __tablename__ = "turnos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False) # Manhã, Tarde, Noite, Integral
    alocacoes = relationship("Alocacao", back_populates="turno")

class Aluno(Base): # Tabela em Stand-by
    __tablename__ = "alunos"
    matricula = Column(String, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String)
    telefone = Column(String)

class Alocacao(Base):
    __tablename__ = "alocacoes"
    id = Column(Integer, primary_key=True, index=True)
    quant_alunos = Column(Integer)
    modalidade_id = Column(Integer, ForeignKey("modalidades.id"))
    modalidade = relationship("Modalidade", back_populates="alocacoes")
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    data_ini_dic = Column(Date)
    data_fim_dic = Column(Date)

    # CHAVES ESTRANGEIRAS (Os IDs das outras tabelas)
    sala_id = Column(Integer, ForeignKey("salas.id"))
    curso_id = Column(Integer, ForeignKey("cursos.id"))
    disciplina_id = Column(Integer, ForeignKey("disciplinas.id"))
    professor_id = Column(Integer, ForeignKey("professores.id"))
    empresa_id = Column(Integer, ForeignKey("empresas.id"))
    turno_id = Column(Integer, ForeignKey("turnos.id"))

    # RELACIONAMENTOS (Para o FastAPI conseguir puxar os nomes em vez de só os IDs)
    sala = relationship("Sala", back_populates="alocacoes")
    curso = relationship("Curso", back_populates="alocacoes")
    disciplina = relationship("Disciplina", back_populates="alocacoes")
    professor = relationship("Professor", back_populates="alocacoes")
    empresa = relationship("Empresa", back_populates="alocacoes")
    turno = relationship("Turno", back_populates="alocacoes")

