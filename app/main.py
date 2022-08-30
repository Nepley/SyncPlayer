from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi_socketio import SocketManager

app = FastAPI()
socket_manager = SocketManager(app=app)

app.mount("/static", StaticFiles(directory="static/"), name="static")
templates = Jinja2Templates(directory="templates/")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/syncplayer/{room}", response_class=HTMLResponse)
async def player(request: Request, room: str):
    return templates.TemplateResponse("playerRoller.html", {"request": request, "room": room})

@app.get("/playlisteditor", response_class=HTMLResponse)
async def playlistEditor(request: Request):
    return templates.TemplateResponse('playlistEditor.html', {"request": request})

@app.get("/roll/{room}", response_class=HTMLResponse)
async def rollDice(request: Request, room: str):
    return templates.TemplateResponse("rollPage.html", {"request": request, "room": room})

## Socket
@app.sio.on('player')
async def handle_player_event(sid, data, **kwargs):
    if("room" in data):
        await app.sio.emit('player', data, room=data["room"])

@app.sio.on('roll')
async def handle_roll_event(sid, data, **kwargs):
    if("room" in data):
        await app.sio.emit('roll', data, room=data["room"])

@app.sio.on('join_room')
async def handle_room_creation(sid, room, **kwargs):
    app.sio.enter_room(sid, room)

@app.sio.on('leave_room')
async def handle_room_creation(sid, room, **kwargs):
    app.sio.leave_room(sid, room)