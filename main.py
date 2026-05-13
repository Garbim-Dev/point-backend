from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError # Importação crucial para tratamento de erros
from sqlalchemy import or_
from database import engine, Base, get_db
from models import models
from schemas import alocacao as schemas

# Cria todas as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Point API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://point-app-sigma.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# ROTA DE AUTENTICAÇÃO (LOGIN)
# ==========================================
@app.post("/auth/login")
def login(credenciais: schemas.LoginRequest, db: Session = Depends(get_db)):
    gestor = db.query(models.Gestor).filter(models.Gestor.email == credenciais.email).first()
    if not gestor or gestor.senha != credenciais.senha:
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos")
    return {
        "mensagem": "Login aprovado", 
        "gestor_id": gestor.id, 
        "nome": gestor.nome,
        "funcao": gestor.funcao
    }

@app.put("/auth/mudar-senha")
def mudar_senha(dados: schemas.MudarSenhaRequest, db: Session = Depends(get_db)):
    # Busca o gestor
    gestor = db.query(models.Gestor).filter(models.Gestor.email == dados.email).first()
    
    # Valida se o email existe e se a senha antiga bate
    if not gestor or gestor.senha != dados.senha_atual:
        raise HTTPException(status_code=400, detail="E-mail ou senha atual incorretos.")
    
    # Atualiza a senha e salva
    gestor.senha = dados.nova_senha
    db.commit()
    
    return {"mensagem": "Senha atualizada com sucesso!"}

# ==========================================
# 1. GESTORES
# ==========================================
@app.get("/gestores/", response_model=list[schemas.GestorResponse])
def listar_gestores(db: Session = Depends(get_db)):
    return db.query(models.Gestor).all()

@app.post("/gestores/", response_model=schemas.GestorResponse)
def criar_gestor(gestor: schemas.GestorCreate, db: Session = Depends(get_db)):
    db_gestor = models.Gestor(**gestor.model_dump())
    db.add(db_gestor); db.commit(); db.refresh(db_gestor)
    return db_gestor

@app.put("/gestores/{id}", response_model=schemas.GestorResponse)
def atualizar_gestor(id: int, obj: schemas.GestorCreate, db: Session = Depends(get_db)):
    db_obj = db.query(models.Gestor).filter(models.Gestor.id == id).first()
    if not db_obj: raise HTTPException(status_code=404, detail="Não encontrado")
    for k, v in obj.model_dump().items(): setattr(db_obj, k, v)
    db.commit(); db.refresh(db_obj); return db_obj

@app.delete("/gestores/{id}")
def deletar_gestor(id: int, db: Session = Depends(get_db)):
    db_obj = db.query(models.Gestor).filter(models.Gestor.id == id).first()
    if not db_obj: raise HTTPException(status_code=404, detail="Não encontrado")
    try:
        db.delete(db_obj); db.commit()
        return {"ok": True}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Não é possível excluir este Gestor.")

# ==========================================
# 2. PROFESSORES
# ==========================================
@app.get("/professores/", response_model=list[schemas.ProfessorResponse])
def listar_professores(db: Session = Depends(get_db)):
    return db.query(models.Professor).all()

@app.post("/professores/", response_model=schemas.ProfessorResponse)
def criar_professor(obj: schemas.ProfessorCreate, db: Session = Depends(get_db)):
    db_obj = models.Professor(**obj.model_dump())
    db.add(db_obj); db.commit(); db.refresh(db_obj)
    return db_obj

@app.put("/professores/{id}", response_model=schemas.ProfessorResponse)
def atualizar_professor(id: int, obj: schemas.ProfessorCreate, db: Session = Depends(get_db)):
    db_obj = db.query(models.Professor).filter(models.Professor.id == id).first()
    if not db_obj: raise HTTPException(status_code=404, detail="Não encontrado")
    for k, v in obj.model_dump().items(): setattr(db_obj, k, v)
    db.commit(); db.refresh(db_obj); return db_obj

@app.delete("/professores/{id}")
def deletar_professor(id: int, db: Session = Depends(get_db)):
    db_obj = db.query(models.Professor).filter(models.Professor.id == id).first()
    if not db_obj: raise HTTPException(status_code=404, detail="Não encontrado")
    try:
        db.delete(db_obj); db.commit()
        return {"ok": True}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Não é possível excluir: Professor vinculado a uma turma.")

# ==========================================
# 3. SALAS
# ==========================================
@app.get("/salas/", response_model=list[schemas.SalaResponse])
def listar_salas(db: Session = Depends(get_db)):
    return db.query(models.Sala).all()

@app.post("/salas/", response_model=schemas.SalaResponse)
def criar_sala(obj: schemas.SalaCreate, db: Session = Depends(get_db)):
    db_obj = models.Sala(**obj.model_dump())
    db.add(db_obj); db.commit(); db.refresh(db_obj)
    return db_obj

@app.put("/salas/{id}", response_model=schemas.SalaResponse)
def atualizar_sala(id: int, obj: schemas.SalaCreate, db: Session = Depends(get_db)):
    db_obj = db.query(models.Sala).filter(models.Sala.id == id).first()
    if not db_obj: raise HTTPException(status_code=404, detail="Não encontrado")
    for k, v in obj.model_dump().items(): setattr(db_obj, k, v)
    db.commit(); db.refresh(db_obj); return db_obj

@app.delete("/salas/{id}")
def deletar_sala(id: int, db: Session = Depends(get_db)):
    db_obj = db.query(models.Sala).filter(models.Sala.id == id).first()
    if not db_obj: raise HTTPException(status_code=404, detail="Não encontrado")
    try:
        db.delete(db_obj); db.commit()
        return {"ok": True}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Não é possível excluir: Sala vinculada a uma turma.")

# ==========================================
# 4. CURSOS
# ==========================================
@app.get("/cursos/", response_model=list[schemas.CursoResponse])
def listar_cursos(db: Session = Depends(get_db)):
    return db.query(models.Curso).all()

@app.post("/cursos/", response_model=schemas.CursoResponse)
def criar_curso(obj: schemas.CursoCreate, db: Session = Depends(get_db)):
    db_obj = models.Curso(**obj.model_dump())
    db.add(db_obj); db.commit(); db.refresh(db_obj)
    return db_obj

@app.put("/cursos/{id}", response_model=schemas.CursoResponse)
def atualizar_curso(id: int, obj: schemas.CursoCreate, db: Session = Depends(get_db)):
    db_obj = db.query(models.Curso).filter(models.Curso.id == id).first()
    if not db_obj: raise HTTPException(status_code=404, detail="Não encontrado")
    for k, v in obj.model_dump().items(): setattr(db_obj, k, v)
    db.commit(); db.refresh(db_obj); return db_obj

@app.delete("/cursos/{id}")
def deletar_curso(id: int, db: Session = Depends(get_db)):
    db_obj = db.query(models.Curso).filter(models.Curso.id == id).first()
    if not db_obj: raise HTTPException(status_code=404, detail="Não encontrado")
    try:
        db.delete(db_obj); db.commit()
        return {"ok": True}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Não é possível excluir: Curso vinculado a uma turma.")

# ==========================================
# 5. DISCIPLINAS
# ==========================================
@app.get("/disciplinas/", response_model=list[schemas.DisciplinaResponse])
def listar_disciplinas(db: Session = Depends(get_db)):
    return db.query(models.Disciplina).all()

@app.post("/disciplinas/", response_model=schemas.DisciplinaResponse)
def criar_disciplina(obj: schemas.DisciplinaCreate, db: Session = Depends(get_db)):
    db_obj = models.Disciplina(**obj.model_dump())
    db.add(db_obj); db.commit(); db.refresh(db_obj)
    return db_obj

@app.put("/disciplinas/{id}", response_model=schemas.DisciplinaResponse)
def atualizar_disciplina(id: int, obj: schemas.DisciplinaCreate, db: Session = Depends(get_db)):
    db_obj = db.query(models.Disciplina).filter(models.Disciplina.id == id).first()
    if not db_obj: raise HTTPException(status_code=404, detail="Não encontrado")
    for k, v in obj.model_dump().items(): setattr(db_obj, k, v)
    db.commit(); db.refresh(db_obj); return db_obj

@app.delete("/disciplinas/{id}")
def deletar_disciplina(id: int, db: Session = Depends(get_db)):
    db_obj = db.query(models.Disciplina).filter(models.Disciplina.id == id).first()
    if not db_obj: raise HTTPException(status_code=404, detail="Não encontrado")
    try:
        db.delete(db_obj); db.commit()
        return {"ok": True}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Não é possível excluir: Disciplina vinculada a uma turma.")

# ==========================================
# 6. EMPRESAS
# ==========================================
@app.get("/empresas/", response_model=list[schemas.EmpresaResponse])
def listar_empresas(db: Session = Depends(get_db)):
    return db.query(models.Empresa).all()

@app.post("/empresas/", response_model=schemas.EmpresaResponse)
def criar_empresa(obj: schemas.EmpresaCreate, db: Session = Depends(get_db)):
    db_obj = models.Empresa(**obj.model_dump())
    db.add(db_obj); db.commit(); db.refresh(db_obj)
    return db_obj

@app.put("/empresas/{id}", response_model=schemas.EmpresaResponse)
def atualizar_empresa(id: int, obj: schemas.EmpresaCreate, db: Session = Depends(get_db)):
    db_obj = db.query(models.Empresa).filter(models.Empresa.id == id).first()
    if not db_obj: raise HTTPException(status_code=404, detail="Não encontrado")
    for k, v in obj.model_dump().items(): setattr(db_obj, k, v)
    db.commit(); db.refresh(db_obj); return db_obj

@app.delete("/empresas/{id}")
def deletar_empresa(id: int, db: Session = Depends(get_db)):
    db_obj = db.query(models.Empresa).filter(models.Empresa.id == id).first()
    if not db_obj: raise HTTPException(status_code=404, detail="Não encontrado")
    try:
        db.delete(db_obj); db.commit()
        return {"ok": True}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Não é possível excluir: Empresa vinculada a uma turma.")

# ==========================================
# 7. TURNOS
# ==========================================
@app.get("/turnos/", response_model=list[schemas.TurnoResponse])
def listar_turnos(db: Session = Depends(get_db)):
    return db.query(models.Turno).all()

@app.post("/turnos/", response_model=schemas.TurnoResponse)
def criar_turno(obj: schemas.TurnoCreate, db: Session = Depends(get_db)):
    db_obj = models.Turno(**obj.model_dump())
    db.add(db_obj); db.commit(); db.refresh(db_obj)
    return db_obj

@app.put("/turnos/{id}", response_model=schemas.TurnoResponse)
def atualizar_turno(id: int, obj: schemas.TurnoCreate, db: Session = Depends(get_db)):
    db_obj = db.query(models.Turno).filter(models.Turno.id == id).first()
    if not db_obj: raise HTTPException(status_code=404, detail="Não encontrado")
    for k, v in obj.model_dump().items(): setattr(db_obj, k, v)
    db.commit(); db.refresh(db_obj); return db_obj

@app.delete("/turnos/{id}")
def deletar_turno(id: int, db: Session = Depends(get_db)):
    db_obj = db.query(models.Turno).filter(models.Turno.id == id).first()
    if not db_obj: raise HTTPException(status_code=404, detail="Não encontrado")
    try:
        db.delete(db_obj); db.commit()
        return {"ok": True}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Não é possível excluir: Turno vinculado a uma turma.")

# ==========================================
# 8. MODALIDADES
# ==========================================
@app.get("/modalidades/", response_model=list[schemas.ModalidadeResponse])
def listar_modalidades(db: Session = Depends(get_db)):
    return db.query(models.Modalidade).all()

@app.post("/modalidades/", response_model=schemas.ModalidadeResponse)
def criar_modalidade(obj: schemas.ModalidadeCreate, db: Session = Depends(get_db)):
    db_obj = models.Modalidade(**obj.model_dump())
    db.add(db_obj); db.commit(); db.refresh(db_obj)
    return db_obj

@app.put("/modalidades/{id}", response_model=schemas.ModalidadeResponse)
def atualizar_modalidade(id: int, obj: schemas.ModalidadeCreate, db: Session = Depends(get_db)):
    db_obj = db.query(models.Modalidade).filter(models.Modalidade.id == id).first()
    if not db_obj: raise HTTPException(status_code=404, detail="Não encontrado")
    for k, v in obj.model_dump().items(): setattr(db_obj, k, v)
    db.commit(); db.refresh(db_obj); return db_obj

@app.delete("/modalidades/{id}")
def deletar_modalidade(id: int, db: Session = Depends(get_db)):
    db_obj = db.query(models.Modalidade).filter(models.Modalidade.id == id).first()
    if not db_obj: raise HTTPException(status_code=404, detail="Não encontrado")
    try:
        db.delete(db_obj); db.commit()
        return {"ok": True}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Não é possível excluir: Modalidade vinculada a uma turma.")

# ==========================================
# 9. ALOCAÇÕES (TURMAS)
# ==========================================

# --- INTELIGÊNCIA DE CRUZAMENTO DE TURNOS ---
def obter_turnos_conflitantes(turno_id: int, db: Session):
    turno_atual = db.query(models.Turno).filter(models.Turno.id == turno_id).first()
    if not turno_atual: return [turno_id]
    
    nome = turno_atual.nome.strip().lower()
    todos_turnos = db.query(models.Turno).all()
    
    # Define o que cada turno ocupa no relógio
    mapa = {
        "manhã": {"manhã"},
        "tarde": {"tarde"},
        "noite": {"noite"},
        "diurno": {"manhã", "tarde"},
        "integral": {"manhã", "tarde", "noite"}
    }
    
    # Descobre os blocos de tempo do turno que estamos tentando cadastrar
    conjunto_alvo = mapa.get(nome, {nome})
    ids_conflito = []
    
    # Verifica todos os turnos do banco. Se cruzarem no tempo, é conflito!
    for t in todos_turnos:
        nome_t = t.nome.strip().lower()
        conjunto_t = mapa.get(nome_t, {nome_t})
        if conjunto_alvo.intersection(conjunto_t):
            ids_conflito.append(t.id)
            
    return ids_conflito

@app.get("/alocacoes/", response_model=list[schemas.AlocacaoResponse])
def listar_alocacoes(db: Session = Depends(get_db)):
    return db.query(models.Alocacao).all()

@app.post("/alocacoes/", response_model=schemas.AlocacaoResponse)
def criar_alocacao(alocacao: schemas.AlocacaoCreate, db: Session = Depends(get_db)):
    
    # 1. Busca quais turnos brigam com o turno escolhido
    turnos_proibidos = obter_turnos_conflitantes(alocacao.turno_id, db)

    # 2. Varre o banco buscando choques
    conflito = db.query(models.Alocacao).filter(
        models.Alocacao.data_ini_dic <= alocacao.data_fim_dic, # As datas se cruzam
        models.Alocacao.data_fim_dic >= alocacao.data_ini_dic,
        models.Alocacao.turno_id.in_(turnos_proibidos), # Os turnos se cruzam (Ex: Manhã e Diurno)
        or_(
            models.Alocacao.sala_id == alocacao.sala_id, # Mesma Sala OU
            models.Alocacao.professor_id == alocacao.professor_id # Mesmo Professor
        )
    ).first()

    # 3. Informa EXATAMENTE onde está o erro para o usuário
    if conflito:
        if conflito.professor_id == alocacao.professor_id:
            raise HTTPException(status_code=400, detail="Choque! Este professor já está dando aula em outra turma nas mesmas datas e horários.")
        else:
            raise HTTPException(status_code=400, detail="Choque! Esta sala já está ocupada por outra turma nas mesmas datas e horários.")

    db_alocacao = models.Alocacao(**alocacao.model_dump())
    db.add(db_alocacao); db.commit(); db.refresh(db_alocacao)
    return db_alocacao

@app.put("/alocacoes/{id}", response_model=schemas.AlocacaoResponse)
def atualizar_alocacao(id: int, obj: schemas.AlocacaoCreate, db: Session = Depends(get_db)):
    db_obj = db.query(models.Alocacao).filter(models.Alocacao.id == id).first()
    if not db_obj: raise HTTPException(status_code=404, detail="Não encontrado")
    
    turnos_proibidos = obter_turnos_conflitantes(obj.turno_id, db)

    # Varre buscando choques (IGNORANDO A SI MESMO na edição)
    conflito = db.query(models.Alocacao).filter(
        models.Alocacao.id != id, 
        models.Alocacao.data_ini_dic <= obj.data_fim_dic,
        models.Alocacao.data_fim_dic >= obj.data_ini_dic,
        models.Alocacao.turno_id.in_(turnos_proibidos),
        or_(
            models.Alocacao.sala_id == obj.sala_id,
            models.Alocacao.professor_id == obj.professor_id
        )
    ).first()

    if conflito:
        if conflito.professor_id == obj.professor_id:
            raise HTTPException(status_code=400, detail="Choque! Este professor já está dando aula em outra turma nas mesmas datas e horários.")
        else:
            raise HTTPException(status_code=400, detail="Choque! Esta sala já está ocupada por outra turma nas mesmas datas e horários.")

    for k, v in obj.model_dump().items(): setattr(db_obj, k, v)
    db.commit(); db.refresh(db_obj); return db_obj

@app.delete("/alocacoes/{id}")
def deletar_alocacao(id: int, db: Session = Depends(get_db)):
    db_obj = db.query(models.Alocacao).filter(models.Alocacao.id == id).first()
    if not db_obj: raise HTTPException(status_code=404, detail="Não encontrado")
    try:
        db.delete(db_obj); db.commit()
        return {"ok": True}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))