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
        "description": "The central area conecting every room together.Players can rest here and choose where they can explore next.",
        "choices":[]
    },
    "brewery": {
        "description": "The room smells of herbs and and old barrels.You can brew potions here and harvest herbs required for it",
        "choices": ["brew","harvest"]
    },
    "deep_forest": {
        "description": "The room is full of trees where you can meditate and grow your health",
        "choices": ["meditate"]
    },
    "cave":{
        "description":"You entered a cold dark cave .Water drips from the ceiling and stranger noises  echo the tunnels.You can mine here and use them for upgrading tools",
        "choices":["mine"]
    },
    "quests":{
        "description":"",
        "choices":["Craft a gold pickaxe"]
    },
    "library":{
        "description":"Dusty books fill the ancient shelves.Candelight flickers and strange symbols.You can read ,solve riddle",
        "choices":["read","riddle"]
    },
    "merchant":{
        "description":"A merchant stands with a wagon of supplies and rare items.You can buy and sell items here",
        "choices": ["buy","sell"]
    },
    "quests":{
        "description":"A large wodden board is ccovered with quests and bounties.You can accept them",
        "choices":["accept"]
    },
    "blacksmith":{
        "description":"You can forge your tools like sword and pickaxe and also repair them if their health is less",
        "choices":["upgrade","repair"]
    },
    "boss_fight":{
        "description":"You step into a massive area.The ground shakes as a powerful enemy is hiding in the dark",
        "choices":["enter"]
    },
    "game_over": {
        "description": "",
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
        "|       Quests      |    Boss Fight     |     Blacksmith    |\n"
        "|                   |                   |                   |\n"
        "+-------------------+--------[ ]--------+-------------------+\n"
        "                          |       |\n"
        "                          |       |\n"
        "                          |       |\n"
        "                          [  EXIT ] \n"
    )
@app.get("/explore_room")
def status():
    return{
        "location":player.location,
        "description":ROOMS.get(player.location,{}).get("description"),
        "choices":ROOMS.get(player.location,{}).get("choices",[])
    }

LOCATIONS=["lobby","cave","brewery","library","deep_forest","merchant","quests","boss_fight","blacksmith"]
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
    action.choice=action.choice.lower()
    if not action.choice:
        options=ROOMS.get(player.location, {}).get("choices", [])
        return PlainTextResponse(f"Please select a choice.Available choices:{options}")
    if action.choice not in ROOMS.get(player.location, {}).get("choices", []):
        options=ROOMS.get(player.location,{}).get("choices",[])
        return PlainTextResponse(f"Please select a choice.Available choices:{options}")
    #if(player.location=="brewery"):
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