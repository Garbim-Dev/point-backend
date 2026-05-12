from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

# --- SCHEMAS BASES (Para as tabelas de apoio) ---

class LoginRequest(BaseModel):
    email: str
    senha: str

class EmpresaCreate(BaseModel):
    nome: str
    telefone: Optional[str] = None

class EmpresaResponse(EmpresaCreate):
    id: int
    class Config: from_attributes = True

class GestorCreate(BaseModel):
    nome: str
    funcao: str
    email: str
    telefone: Optional[str] = None
    senha: str

class GestorResponse(BaseModel):
    id: int # Código do Gestor
    nome: str
    funcao: str
    email: str
    telefone: Optional[str] = None
    # Note que NÃO devolvemos a senha aqui por segurança!

    class Config: 
        from_attributes = True

class ProfessorCreate(BaseModel):
    nome: str
    matricula: Optional[str] = None
    area_atuacao: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None

class ProfessorResponse(ProfessorCreate):
    id: int
    class Config: from_attributes = True

class SalaCreate(BaseModel):
    nome: str
    capacidade: Optional[int] = None
    # NOVO CAMPO: Identifica a localização física (Bloco A, 2º Andar, etc)
    bloco_andar: Optional[str] = None

class SalaResponse(SalaCreate):
    id: int
    class Config: from_attributes = True

class CursoCreate(BaseModel):
    nome: str
    carga_horaria: Optional[int] = None

class CursoResponse(CursoCreate):
    id: int
    class Config: from_attributes = True

class DisciplinaCreate(BaseModel):
    nome: str
    carga_horaria: Optional[int] = None

class DisciplinaResponse(DisciplinaCreate):
    id: int
    class Config: from_attributes = True

class ModalidadeCreate(BaseModel):
    nome: str

class ModalidadeResponse(ModalidadeCreate):
    id: int
    class Config: from_attributes = True

class TurnoCreate(BaseModel):
    nome: str

class TurnoResponse(TurnoCreate):
    id: int
    class Config: from_attributes = True

# --- SCHEMAS DA ALOCAÇÃO ---

# Dados que o Coordenador vai enviar na hora de cadastrar
class AlocacaoCreate(BaseModel):
    quant_alunos: int
    data_ini_dic: date
    data_fim_dic: date
    sala_id: int
    curso_id: int
    disciplina_id: int
    professor_id: int
    empresa_id: int
    turno_id: int
    modalidade_id: int

# Dados que o Backend vai devolver para o React
class AlocacaoResponse(BaseModel):
    id: int
    quant_alunos: int
    modalidade: ModalidadeResponse
    data_criacao: datetime
    data_ini_dic: date
    data_fim_dic: date
    
    # Objetos completos para facilitar a exibição nos cards
    sala: SalaResponse
    curso: CursoResponse
    disciplina: DisciplinaResponse
    professor: ProfessorResponse
    empresa: EmpresaResponse
    turno: TurnoResponse

    class Config: from_attributes = True

class MudarSenhaRequest(BaseModel):
    email: str
    senha_atual: str
    nova_senha: str