from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from typing import List
import uvicorn

app = FastAPI(
    title="API Text Adventure",
    description="A text-based RPG engine played entirely through API requests!",
    version="1.0.0"
)

class Player:
    def __init__(self):
        self.health = 100
        self.inventory: List[str] = []
        self.location = "Lobby"

player = Player()

class ActionRequest(BaseModel):
    choice: int

ROOMS = {
    "Lobby": {
        "description": "You are at the edge of a dark forest. You see a path leading 'inside' and a shiny 'coin' on the ground.",
        "choices": ["Brewery","Deep Forest","Merchant","Boss Fight"]
    },
    "Brewery": {
        "description": "It is pitch black. A goblin appears! You can 'fight' or 'run'.",
        "choices": ["Harvest crops", "Make a potion"]
    },
    "Deep forest": {
        "description": "You defeated the goblin and won the game! Restart the server to play again.",
        "choices": ["Meditate","Cave","Quests"]
    },
    "game_over": {
        "description": "You died. Restart the server to try again.",
        "choices": []
    }
}

@app.get("/map", response_class=PlainTextResponse)
def map():
    return (
        "+-------------------+-------------------+-------------------+\n"
        "|                   |                   |                   |\n"
        "|       Cave        |      Brewery      |      Library      |\n"
        "|                   |                   |                   |\n"
        "+--------[ ]--------+--------[ ]--------+--------[ ]--------+\n"
        "|                   |                   |                   |\n"
        "|    Deep Forest    |      LOBBY        |      Merchant     |\n"
        "|                   |                   |                   |\n"
        "+--------[ ]--------+--------[ ]--------+--------[ ]--------+\n"
        "|                   |                   |                   |\n"
        "|       Quests      |    Boss Fight     |      Upgrade      |\n"
        "|                   |                   |                   |\n"
        "+-------------------+--------[ ]--------+-------------------+\n"
        "                          |       |\n"
        "                          |       |\n"
        "                          |       |\n"
        "                          [  EXIT ] \n"
    )
@app.get("/playerinfo")
def info():
    return{
        "player_health":player.health,
        "player_inventory":player.inventory,
        "player_location":player.location
    }
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)