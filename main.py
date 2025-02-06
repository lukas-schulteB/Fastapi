from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Annotated
from starlette.responses import RedirectResponse
from data.dao.dao_reservas import DaoReservas
from data.database import database

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
dao_reservas = DaoReservas() 

opiniones_list = []


@app.get("/", response_class=HTMLResponse, name="home")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "nombre": "Chapatax"})

@app.get("/menu", response_class=HTMLResponse, name="menu")
async def menu(request: Request):
    menu_items = [
        {"plato": "Pizza Margherita", "precio": "7€"},
        {"plato": "Pizza Marinara", "precio": "6€"},
        {"plato": "Pizza Diavola", "precio": "9€"},
        {"plato": "Pizza Pesto", "precio": "9€"},
        {"plato": "Pizza Prociutto e Funghi", "precio": "9€"},
        {"plato": "Pizza Cuatro Quesos", "precio": "8€"},
        {"plato": "Tiramisú", "precio": "5€"},
        {"plato": "Panna Cotta", "precio": "4.5€"},
        {"plato": "Cannoli", "precio": "4.5€"},
    ]
    return templates.TemplateResponse("menu.html", {"request": request, "menu_items": menu_items})

@app.get("/opiniones", response_class=HTMLResponse, name="opiniones")
async def opiniones(request: Request):
    return templates.TemplateResponse("opiniones.html", {"request": request, "reviews": opiniones_list})

@app.post("/opiniones")
async def add_opinion(request: Request, nombre: str = Form(...), puntuacion: int = Form(...), comentario: str = Form(...)):
    opiniones_list.append({"nombre": nombre, "puntuacion": puntuacion, "comentario": comentario})
    return RedirectResponse(url="/opiniones", status_code=303)

@app.get("/faq", response_class=HTMLResponse, name="faq")
async def faq(request: Request):
    preguntas = [
        {"pregunta": "¿Ofrecen opciones vegetarianas?", "respuesta": "Sí, tenemos varios platos vegetarianos."},
        {"pregunta": "¿Aceptan reservas?", "respuesta": "Sí, puedes hacer tu reserva a través de la sección de reservas."},
        {"pregunta": "¿Tienen servicio de entrega?", "respuesta": "Por el momento no ofrecemos entrega a domicilio."},
        {"pregunta": "¿Cuáles son los horarios de apertura?", "respuesta": "Abrimos todos los días de 12 PM a 10 PM."},
        {"pregunta": "¿Puedo llevármelo?", "respuesta": "En nuestra tienda puedes venir y llevártelo todo"},
        {"pregunta": "¿Teneis pizzas sin gluten?", "respuesta": "De momento no disponemos de pizzas sin gluten"},
    ]
    return templates.TemplateResponse("faq.html", {"request": request, "preguntas": preguntas})

@app.get("/contacto", response_class=HTMLResponse, name="contacto")
async def contacto(request: Request):
    return templates.TemplateResponse("contacto.html", {"request": request})

@app.get("/reservas", response_class=HTMLResponse, name="reservas")
def get_reservas(request: Request):
    db = database  
    reservas = dao_reservas.get_all(db) 
    return templates.TemplateResponse("reservas.html", {"request": request, "reservas": reservas})

@app.get("/deletereserva/{reserva_id}", response_class=HTMLResponse, name="deletereserva")
def delete_reserva(request: Request, reserva_id: str):
    db = database
    dao_reservas.delete(db, reserva_id)  
    reservas = dao_reservas.get_all(db)  
    return templates.TemplateResponse("reservas.html", {"request": request, "reservas": reservas})

@app.post("/delreserva", response_class=HTMLResponse)
def del_reserva(request: Request, reserva_id: Annotated[str, Form()]):
    db = database
    dao_reservas.delete(db, reserva_id)  
    reservas = dao_reservas.get_all(db) 
    return templates.TemplateResponse("reservas.html", {"request": request, "reservas": reservas})

@app.get("/formaddreserva", response_class=HTMLResponse, name="formaddreserva")
def form_add_reserva(request: Request):
    return templates.TemplateResponse("formaddreserva.html", {"request": request})

@app.post("/addreserva", response_class=HTMLResponse, name="addreserva")
def add_reserva(request: Request, nombre: Annotated[str, Form()], telefono: Annotated[str, Form()], email: Annotated[str, Form()], fecha: Annotated[str, Form()], hora: Annotated[str, Form()], personas: Annotated[int, Form()]):
    db = database
    dao_reservas.insert(db, nombre, telefono, email, fecha, hora, personas) 
    reservas = dao_reservas.get_all(db) 
    return templates.TemplateResponse("reservas.html", {"request": request, "reservas": reservas})


@app.get("/editreserva/{reserva_id}", response_class=HTMLResponse, name="editreserva")
def edit_reserva(request: Request, reserva_id: str):
    db = database
    reserva = dao_reservas.get_by_id(db, reserva_id)  
    return templates.TemplateResponse("formeditreserva.html", {"request": request, "reserva": reserva})

@app.post("/update_reserva/{reserva_id}", response_class=HTMLResponse)
def update_reserva(request: Request, reserva_id: str, nombre: Annotated[str, Form()], telefono: Annotated[str, Form()], email: Annotated[str, Form()], fecha: Annotated[str, Form()], hora: Annotated[str, Form()], personas: Annotated[int, Form()]):
    db = database
    dao_reservas.update(db, reserva_id, nombre, telefono, email, fecha, hora, personas) 
    reservas = dao_reservas.get_all(db) 
    return templates.TemplateResponse("reservas.html", {"request": request, "reservas": reservas})
