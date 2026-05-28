from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from typing import List
import uvicorn
import random
import time

app = FastAPI(
    title="API Text Adventure",
    description="A text-based RPG engine played entirely through API requests!",
    version="1.0.0"
)

class Player:
    def __init__(self):
        self.health = 100
        self.inventory= {
            "green_herbs":0,
            "blue_herbs":0,
            "health_potion":0,
            "mining_potion":0,
            "stone":0,
            "iron":0,
            "diamond":0
        }
        self.armor={
            "wooden_pickaxe",
            "wooden_sword",
        }
        self.location = "cave"
        self.state=None
        self.brew=None
        self.meditate_timer=time.time()
        self.mine_potion=0
        self.mine_time=time.time()
player = Player()

class ActionRequest(BaseModel):
    teleport: str
class Action(BaseModel):
    choice:str
class a(BaseModel):
    potion:str

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
        "description":"You entered a cold dark cave ,Water drips from the ceiling .You can mine here and use them for upgrading tools-make sure to have enough health or use potions for stamina",
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
        "|    Deep Forest    |       LOBBY       |      Merchant     |\n"
        "|                   |                   |                   |\n"
        "+--------[ ]--------+--------[ ]--------+--------[ ]--------+\n"
        "|                   |                   |                   |\n"
        "|       Quests      |    Boss Fight     |     Blacksmith    |\n"
        "|                   |                   |                   |\n"
        "+-------------------+--------[ ]--------+-------------------+\n"
        "                          |       |\n"
        "                          |       |\n"
        "                          |       |\n"
        "                          [  EXIT ]\n"
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
    # if action.choice not in ROOMS.get(player.location, {}).get("choices", []):
    #     options=ROOMS.get(player.location,{}).get("choices",[])
    #     return PlainTextResponse(f"Please select a choice.Available choices:{options}")
    if(player.location=="brewery"):
        if(action.choice=="harvest"):
            g = random.randint(1,3)
            b = random.randint(1,2)
            player.inventory["green_herbs"] += g-1
            player.inventory["blue_herbs"] += b-1
            content = (
                f"You have harvested:\n"
                f"Green herbs: {g-1}\n"
                f"Blue herbs: {b-1}\n"
            )
            return PlainTextResponse(content)
        if player.state==None:
            if action.choice=="brew":
                player.state=action.choice
                return PlainTextResponse(
                    "Which potion you want to brew?\n"
                    "health_potion\n"
                    "The potion increases the health to 50hp\n"
                    "mining_potion\n"
                    "The potion when taken and mined you may get more resources\n"
                    "Enter your choice with the exact name mentioned above"
                )
        else:
            if player.state=="brew" :
                if action.choice=="health_potion" :
                    if player.inventory["green_herbs"]>=2:
                       player.inventory["health_potion"]+=1
                       player.inventory["green_herbs"]-=2
                       player.state=None
                       return PlainTextResponse(
                           "Succesfully crafted a health_potion\n"
                        )
                    else:
                        player.state=None
                        return PlainTextResponse(
                           "You don't have enough green herbs ,harvest them in brewery\n"
                        )
                elif action.choice=="mining_potion" :
                    if player.inventory["blue_herbs"]>=2:
                       player.inventory["mining_potion"]+=1
                       player.inventory["blue_herbs"]-=2
                       player.state=None
                       return PlainTextResponse(
                           "Succesfully crafted a mining_potion\n"
                        )
                    else:
                        player.state=None
                        return PlainTextResponse(
                           "You don't have enough green herbs ,harvest them in brewery\n"
                        )
                else:
                    return PlainTextResponse(
                    "Which potion you want to brew?\n"
                    "health_potion\n"
                    "mining_potion\n"
                    "Enter your choice with the exact name mentioned above"
                )
        return PlainTextResponse(
            "Enter valid choices\n"
            "harvest\n"
            "brew"
        )
    if(player.location=="deep_forest"):
        if(action.choice=="meditate"):
            if(time.time() - player.meditate_timer) >= 20:
                player.health+=10
                player.meditate_timer=time.time()
                return PlainTextResponse(
                    "Your health has been increased by 10HP\n"
                )
            else:
                return PlainTextResponse(
                    f"Your on a cooldown come after {20-abs(int(time.time() - player.meditate_timer))}sec\n"
                )
        else:
            return PlainTextResponse(
                "Return a valid choice\n"
                "meditate"
            )
    if(player.location=="cave"):
        if(action.choice=="mine"):
            if (time.time() - player.mine_time) >= 120:
                player.mine_potion = 0
                player.health -= 3
            else:
                player.health -= 3
            s=0
            i=0
            d=0
            if "wooden_pickaxe" in player.armor:
               s=random.randint(0,2)
               i=random.randint(0,1)
            elif "iron_pickaxe" in player.armor:
                s=random.randint(0,2)
                i=random.randint(0,2)
                d=random.randint(0,1)
            elif "diamond_pickaxe" in player.armor:
                s=random.randint(0,2)
                i=random.randint(0,2)
                d=random.randint(0,2)
            player.inventory["stone"]+=s
            player.inventory["iron"]+=i
            player.inventory["diamond"]+=d
            return PlainTextResponse(
                f"You have mined:\n"
                f"Stone: {s}\n"
                f"Iron: {i}\n"
                f"Diamond: {d}\n"
            )
            
                       
@app.post("/usepotion")
def potion(action:a):
    if(action.potion=="health_potion"):
        if player.inventory["health_potion"] <= 0:
            return PlainTextResponse(
                "You do not have a health potion."
            )
        player.health+=30
        player.inventory["health_potion"] -=1
        if player.health > 200:
            player.health = 200
        return PlainTextResponse(
            "Health potion activated!! 30HP increased"
        )
    elif(action.potion=="mining_potion"):
        if player.inventory["mining_potion"] <= 0:
            return PlainTextResponse(
                "You do not have a mining potion."
            )
        player.mine_potion=1
        player.mine_time=time.time()
        player.inventory["mining_potion"] -= 1
        return PlainTextResponse(
            "Mining potion activated!! You can mine for 2 minutes with no loss of health"
        )
    else:
        return PlainTextResponse(
            "Enter a valid choice:\n"
            "health_potion\n"
            "mining_potion"
        )




@app.get("/playerinfo")
def info():
    return{
        "player_health":player.health,
        "player_location":player.location,
        "player_inventory":player.inventory,
        "player_armor":player.armor
    }    
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)