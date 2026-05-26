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
        self.location = "lobby"

player = Player()

class ActionRequest(BaseModel):
    teleport: str
class Action(BaseModel):
    choice:str
ROOMS = {
    "lobby": {
        "description": "You are at the edge of a dark forest. You see a path leading 'inside' and a shiny 'coin' on the ground.",
        "choices":[]
    },
    "brewery": {
        "description": "It is pitch black. A goblin appears! You can 'fight' or 'run'.",
        "choices": ["harvest_crops"]
    },
    "deep_forest": {
        "description": "You defeated the goblin and won the game! Restart the server to play again.",
        "choices": ["Meditate"]
    },
    "cave":{
        "description":"",
        "choices":["Mine"]
    },
    "quests":{
        "description":"",
        "choices":["Craft a gold pickaxe"]
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
@app.get("/status")
def status():
    return{
        "location":player.location,
        "description":ROOMS.get(player.location,{}).get("description"),
        "choices":ROOMS.get(player.location,{}).get("choices",[])
    }

LOCATIONS=["lobby","cave","brewery","library","deep_forest","merchant","quests","boss_fight","upgrade"]
@app.post("/teleport")
def teleport(action: ActionRequest):
    if not action.teleport:
        options = ", ".join(LOCATIONS)
        return PlainTextResponse(f"Please choose a location. Available locations: {options}") 
    location = action.teleport.lower()
    if location not in LOCATIONS:
        raise HTTPException(status_code=400, detail=f"Invalid location. Choose from: {', '.join(LOCATIONS)}")
    x = player.location
    player.location = location
    return PlainTextResponse(f"Player has teleported from {x} to {player.location}")
@app.post("/choice")
def choice(action:Action):
    if not action.choice:
        options=ROOMS.get(player.location, {}).get("choices", [])
        return PlainTextResponse(f"Please select a choice.Available choices:{options}")
    if action.choice not in ROOMS.get(player.location, {}).get("choices", []):
        options=ROOMS.get(player.location,{}).get("choices",[])
        return PlainTextResponse(f"Please select a choice.Available choices:{options}")
    # if(player.location=="brewery"):
    #     if(action.choice=="")
@app.get("/playerinfo")
def info():
    return{
        "player_health":player.health,
        "player_inventory":player.inventory,
        "player_location":player.location
    }    
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)