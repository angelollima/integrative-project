from fastapi import ( APIRouter, Depends, Form, HTTPException, Path, Request, status,)

from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models.Usuario import Usuario
from util.mensagem import redirecionar_com_mensagem
from repositories.UsuarioRepo import UsuarioRepo
from util.seguranca import (conferir_senha, obter_hash_senha, obter_usuario_logado,)

router = APIRouter(prefix="/usuario")
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def get_index(request: Request, usuario: Usuario = Depends(obter_usuario_logado),):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    usuarios = UsuarioRepo.obter_todos()
    return templates.TemplateResponse("usuario/index.html", {"request": request, "usuario": usuario, "usuarios": usuarios},)

@router.get("/excluir/{id_usuario:int}", response_class=HTMLResponse)
async def get_excluir(request: Request, id_usuario: int = Path(), usuario: Usuario = Depends(obter_usuario_logado),):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    usuario_excluir = UsuarioRepo.obter_por_id(id_usuario)
    return templates.TemplateResponse("usuario/excluir.html", {"request": request, "usuario": usuario, "usuario_excluir": usuario_excluir},)

@router.post("/excluir/{id_usuario:int}", response_class=HTMLResponse)
async def post_excluir(usuario: Usuario = Depends(obter_usuario_logado), id_usuario: int = Path(),):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    if id_usuario == 1:
        response = redirecionar_com_mensagem("/usuario","Não é possível excluir o administrador padrão do sistema.",)
        return response
    if id_usuario == usuario.id:
        response = redirecionar_com_mensagem("/usuario", "Não é possível excluir o próprio usuário que está logado.",)
        return response

    UsuarioRepo.excluir(id_usuario)
    response = redirecionar_com_mensagem("/usuario", "Usuário excluído com sucesso.",)
    return response

@router.get("/alterar/{id_usuario:int}", response_class=HTMLResponse)
async def get_alterar(
    request: Request, 
    id_usuario: int = Path(), 
    usuario: Usuario = Depends(obter_usuario_logado),):

    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    usuario_alterar = UsuarioRepo.obter_por_id(id_usuario)
    return templates.TemplateResponse("usuario/alterar.html", {"request": request, 
    "usuario": usuario, 
    "usuario_alterar": usuario_alterar},)

@router.post("/alterar/{id_usuario:int}", response_class=HTMLResponse)
async def post_alterar(
    id_usuario: int = Path(), 
    nome: str = Form(...), 
    email: str = Form(...), 
    administrador: bool = Form(False), 
    usuario: Usuario = Depends(obter_usuario_logado)):

    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    if id_usuario == 1:
        response = redirecionar_com_mensagem("/usuario", "Não é possível alterar dados do administrador padrão.",)
        return response

    UsuarioRepo.alterar(
        Usuario(id=id_usuario, nome=nome, email=email, admin=administrador))
    response = redirecionar_com_mensagem("/usuario", "Usuário alterado com sucesso.")
    return response

@router.get("/cadastrar")
def getInserir(request: Request):
    return templates.TemplateResponse("cadastrar_usuario.html", {"request": request})

@router.post("/cadastrar")
def postInserir(request: Request, nome: str = Form(), email: str = Form(), senha: str = Form()):  
    usuario = Usuario(nome=nome, email=email, senha=senha)
    print(usuario)
    UsuarioRepo.inserir(usuario)
    return RedirectResponse("/", status.HTTP_302_FOUND)

@router.get("/novo")
async def get_usuario_novo(request: Request,):
    return templates.TemplateResponse("/usuario/inserir.html", {"request": request},)

@router.post("/novo", response_class=HTMLResponse)
async def post_usuario_novo(senha: str = Form(...), confsenha: str = Form(...),
    nome: str = Form(...), 
    email: str = Form(...), 
    administrador: bool = Form(False), 
    usuario: Usuario = Depends(obter_usuario_logado)):

    hash_senha = obter_hash_senha(senha)

    usuario = Usuario(nome=nome, email=email, senha=hash_senha, admin=administrador)
    print(usuario)
    print(UsuarioRepo.inserir(usuario))

    response = redirecionar_com_mensagem("/login", "Usuario criado com sucesso! Entre com seu email e senha para acessar!")
    return response

@router.get("/arearestrita", response_class=HTMLResponse)
async def get_area_restrita(request: Request, usuario: Usuario = Depends(obter_usuario_logado),):

    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    return templates.TemplateResponse("usuario/arearestrita.html", {"request": request, "usuario": usuario},)

@router.post("/alterardados", response_class=HTMLResponse)
async def alterar_dados(
    nome: str = Form(...),
    email: str = Form(...),
    usuario: Usuario = Depends(obter_usuario_logado),
    ):

    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    if usuario.id == 1:
        response = redirecionar_com_mensagem("/usuario", "Não é possível alterar dados do administrador padrão.",)
        return response
    
    UsuarioRepo.alterar(Usuario(id=usuario.id, nome=nome, email=email, admin=usuario.admin))

    response = redirecionar_com_mensagem("/usuario/arearestrita", "Dados alterados com sucesso.",)

    return response

@router.post("/alterarsenha", response_class=HTMLResponse)
async def alterar_senha(senha_atual: str = Form(...), nova_senha: str = Form(...), conf_nova_senha: str = Form(...), usuario: Usuario = Depends(obter_usuario_logado)):

    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    hash_senha_bd = UsuarioRepo.obter_senha_por_email(usuario.email)

    if conferir_senha(senha_atual, hash_senha_bd):
        if nova_senha == conf_nova_senha:
            hash_nova_senha = obter_hash_senha(nova_senha)
            UsuarioRepo.alterar_senha(Usuario(senha=hash_nova_senha,email=usuario.email))
            response = redirecionar_com_mensagem("/usuario/arearestrita", "Senha alterada com sucesso")
        else:
            response = redirecionar_com_mensagem("/usuario/arearestrita", "As senhas não coincidem!")
    else:
        response = redirecionar_com_mensagem("/usuario/arearestrita", "Informe a senha atual corretamente!")

    return response