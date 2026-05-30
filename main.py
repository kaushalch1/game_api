from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
import uvicorn
import random
import time

app = FastAPI(
    title="API Text Adventure",
    description="A text-based RPG engine played entirely through API requests!",
    version="1.0.0"
)
riddles=[{"riddle": "What has hands but cannot clap?", "answer": "Clock"},
            {"riddle": "What has a head and a tail but no body?", "answer": "Coin"},
            {"riddle": "What has one eye but cannot see?", "answer": "Needle"},
            {"riddle": "What gets wetter the more it dries?", "answer": "Towel"},
            {"riddle": "What is full of holes but still holds water?", "answer": "Sponge"},
            {"riddle": "What has legs but does not walk?", "answer": "Table"},
            {"riddle": "What goes up but never comes down?", "answer": "Age"},
            {"riddle": "What has words but never speaks?", "answer": "Book"},
            {"riddle": "What belongs to you but is used more by others?", "answer": "Name"},
            {"riddle": "What can you catch but not throw?", "answer": "Cold"},
            {"riddle": "What has a neck but no head?", "answer": "Bottle"},
            {"riddle": "What goes through cities but never moves?", "answer": "Road"},
            {"riddle": "What has teeth but cannot bite?", "answer": "Comb"},
            {"riddle": "The more you take, the more you leave behind. What are they?", "answer": "Footsteps"},
            {"riddle": "What can honk without a horn?", "answer": "Goose"},
            {"riddle": "What has a thumb and four fingers but isn't alive?", "answer": "Glove"},
            {"riddle": "What is easy to get into but hard to get out of?", "answer": "Trouble"},
            {"riddle": "What loses its head in the morning and gets it back at night?", "answer": "Pillow"},
            {"riddle": "What is orange and sounds like a parrot?", "answer": "Carrot"},
            {"riddle": "What building has the most stories?", "answer": "Library"}]
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
        self.armor=[
            "wooden_pickaxe",
            "wooden_sword",
        ]
        self.location = "library"
        self.coins=0
        self.state=None
        self.brew=None
        self.meditate_timer=time.time()
        self.mine_potion=0
        self.mine_time=time.time()
        self.quests=None
        self.tasks=[]
player = Player()
player.tasks.append(riddles[random.randint(0,5)])
player.tasks.append(riddles[random.randint(6,10)])
player.tasks.append(riddles[random.randint(11,14)])
player.tasks.append(riddles[random.randint(15,19)])
class ActionRequest(BaseModel):
    teleport: str
class Action(BaseModel):
    choice: str
class a(BaseModel):
    potion: str
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
    "library":{
        "description":"Dusty books fill the ancient shelves.Candelight flickers and strange symbols.You can solve riddle",
        "choices":["riddle"]
    },
    "merchant":{
        "description":"A merchant stands with a wagon of supplies and rare items.You can buy and sell items here",
        "choices": ["buy","sell"]
    },
    "quests":{
        "description":"A large wodden board is ccovered with quests and bounties.You can accept them and complete all  to unlock and fight with boss",
        "choices":["quest1","quest2","quest3"]
    },
    "blacksmith":{
        "description":"You can forge your tools like sword and pickaxe and also repair them if their health is less",
        "choices":["upgrade"]
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
quest={
            "quest1":"Craft a health_potion and a mining_potion from the brewery",
            "quest2":"Solve 2 riddles from the librarian",
            "quest3":"Buy a full emerald armor from the merchant includes the helmet,vest,pant,boots",
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
def game_over():
    return PlainTextResponse(
            "=================================\n"
            "           GAME OVER\n"
            "=================================\n"
            f"final health={player.health}\n"
            f"coins collected={player.coins}\n"
            "The adventure has ended.\n"
            "Restart the server to play again.\n"
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
    player.state=None
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
                           "You don't have enough blue herbs ,harvest them in brewery\n"
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
    elif(player.location=="deep_forest"):
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
    elif(player.location=="cave"):
        if(action.choice=="mine"):
            if player.mine_potion == 1:
                if (time.time() - player.mine_time) >= 120:
                    player.mine_potion = 0
                    player.health -= 3
                    if player.health<=0:
                        return game_over()
            else:
                player.health -= 3
                if player.health<=0:
                    return game_over()
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
                f"Your health is decreased by -3Hp.Watch out( ■_■)"
            )
    elif(player.location=="blacksmith"):
        if player.state==None:
            if(action.choice=="upgrade"):
                player.state=action.choice
                items=player.armor
                return PlainTextResponse(
                    "Which item you wan to upgrade:\n"
                    f"{items[0]}\n"
                    f"{items[1]}\n"
                )
            else:
                return PlainTextResponse(
                    "Choose a valid choice:\n"
                    "upgrade"
                )
        else:
            player.state=None
            if(action.choice=="wooden_pickaxe"):
                if(player.inventory["iron"]>=3):
                    player.inventory["iron"]-=3
                    player.armor[0]="iron_pickaxe"
                    return(
                        f"You succesfully upgraded your pickaxe to {player.armor[0]}."
                    )
                else:
                    return PlainTextResponse(
                        "To upgrade your pickaxe you need more iron required\n"
                        "Go to the cave and mine some iron"
                    )
            elif(action.choice=="iron_pickaxe"):
                if(player.inventory["diamond"]>=3):
                    player.inventory["diamond"]-=3
                    player.armor[0]="diamond_pickaxe"
                    return(
                        f"You succesfully upgraded your pickaxe to {player.armor[0]}."
                    )
                else:
                    return PlainTextResponse(
                        "To upgrade your pickaxe you need more diamond required\n"
                        "Go to the cave and mine some diamonds\n"
                    )
            elif(action.choice=="wooden_sword"):
                if(player.inventory["iron"]>=3):
                    player.inventory["iron"]-=3
                    player.armor[1]="iron_sword"
                    return(
                        f"You succesfully upgraded your sword to {player.armor[1]}"
                    )
                else:
                    return PlainTextResponse(
                        "To upgrade your sword you need more iron required\n"
                        "Go to the cave and mine some iron"
                    )
            elif(action.choice=="iron_sword"):
                if(player.inventory["diamond"]>=3):
                    player.inventory["diamond"]-=3
                    player.armor[1]="diamond_sword"
                    return(
                        f"You succesfully upgraded your sword to {player.armor[1]}"
                    )
                else:
                    return PlainTextResponse(
                        "To upgrade your sword you need more diamond required\n"
                        "Go to the cave and mine some diamonds\n"
                    )
            else:
                return PlainTextResponse(
                    "Enter a valid choice:\n"
                    f"{player.armor[0]}\n"
                    f"{player.armor[1]}\n"
                )
    elif(player.location=="merchant"):
        if(player.state==None):
            if(action.choice=="buy" or action.choice=="sell"):
                player.state=action.choice
                if(action.choice=="buy"):
                    return PlainTextResponse(
                        "emerald_helmet=15coins\n"
                        "emerald_vest=18coins\n"
                        "emerald_pant=20coins\n"
                        "emerald_boots=22coins\n"
                    )
                else:
                    return PlainTextResponse(
                        "stone=1coin\n"
                        "iron=2coin\n"
                        "diamond=4coin\n"
                        "health_potion=5coins\n"
                        "mining_potion=5coins\n"
                    )
            else:
                return PlainTextResponse(
                    "Enter a valid choice:\n"
                    "buy\n"
                    "sell\n"
                )
        else:
            if(player.state=="buy"):
                buy_items={
                    "emerald_helmet":15,
                    "emerald_vest":18,
                    "emerald_pant":20,
                    "emerald_boots":22
                }
                if action.choice in buy_items:
                    if(buy_items[action.choice]<=player.coins):
                        player.state=None
                        player.coins-=buy_items[action.choice]
                        player.armor.append(action.choice)
                        return(
                            f"You have purchased {action.choice}!!!"
                        )
                    else:
                        player.state=None
                        return PlainTextResponse(
                            f"You don't have to coins to buy {action.choice},Go earn them."
                        )
                else:
                    player.state=None
                    return PlainTextResponse(
                        "Enter a valid choice:\n"
                        "emerald_helmet\n"
                        "emerald_vest\n"
                        "emerald_pant\n"
                        "emerald_boots\n"
                    )
            elif (player.state=="sell"):
                sell_items={
                    "stone":1,
                    "iron":2,
                    "diamond":4,
                    "health_potion":5,
                    "mining_potion":5
                }
                if(action.choice in sell_items):
                    player.state=None
                    if(player.inventory[action.choice]>=1):
                        player.inventory[action.choice]-=1
                        player.coins+=sell_items[action.choice]
                        return PlainTextResponse(
                            f"Succesfully sold the {action.choice} for {sell_items[action.choice]}"
                        )
                    else:
                        return PlainTextResponse(
                            "You don't have enough resources to sell go make them"
                        )
                else:
                    player.state=None
                    return PlainTextResponse(
                        "Enter a valid choice:\n"
                        "stone\n"
                        "iron\n"
                        "diamond\n"
                        "health_potion\n"
                        "mining_potion\n"
                    )
    elif(player.location=="quests"):
        if(player.quests==None):
            if(action.choice not in ROOMS["quests"]["choices"]):
                return PlainTextResponse(
                    "Complete all the quests to be able to fight with the boss.\n"
                    f"Remaining quests:\n{quest}\n"
                    "If completed the quest enter the name of the quest"
                )
            else:
                player.quests=action.choice
                if(action.choice=="quest1"):
                    player.quests=None
                    if(player.inventory["health_potion"] and player.inventory["mining_potion"]):
                        quest.pop("quest1",None)
                        return PlainTextResponse(
                            "Succesfully completed the quest1 complete remaining quests"
                            f"Remaining quests:\n{quest}"
                        )
                    else:
                        return PlainTextResponse(
                            "You don't have the required potions go and craft them:\n"
                            "check if your inventory has the both health_potion and a mining_potion"
                        )
                elif(action.choice=="quest2"):
                    player.quests=None
                    if len(player.tasks)<=2:
                        quest.pop("quest2",None)
                        return PlainTextResponse(
                                "Succesfully completed the quest2 complete remaining quests"
                                f"Remaining quests:\n{quest}"
                            )
                    else:
                        return PlainTextResponse(
                            "Complete the library riddles more than 2 times totally\n"
                            f"You have completed only {4-len(player.tasks)}tasks."
                        )
                elif(action.choice=="quest3"):
                    player.quests=None
                    emerald_set = [
                        "emerald_helmet",
                        "emerald_vest",
                        "emerald_pant",
                        "emerald_boots"
                        ]
                    if all(item in player.armor for item in emerald_set):
                            quest.pop("quest3",None)
                            return PlainTextResponse(
                                "Succesfully completed the quest3 complete remaining quests"
                                f"Remaining quests:\n{quest}"
                            )
                    else:
                        return PlainTextResponse(
                            "You don't have the complete armor go and earn coins and buy it from merchant\n"
                            "check if your armor has the the whole set of emerrald_armor which contains 4 parts"
                        )
    elif(player.location=="library"):
        if len(player.tasks) == 0:
            return PlainTextResponse(
                "You completed all riddles!"
            )
        if(action.choice=="riddle"):
            player.state="riddle"
            return PlainTextResponse(
                f"{player.tasks[0]['riddle']}"
            )
        elif(player.state=="riddle"):
            if(action.choice==player.tasks[0]["answer"].lower()):
                player.state=None
                player.tasks.pop(0)
                return PlainTextResponse(
                    "Correct answer,solve the next riddle"
                )
            else:
                return PlainTextResponse(
                    "Wrong answer,please retry\n"
                    f"{player.tasks[0]['riddle']}"
                )
        else:
            return PlainTextResponse(
                "Enter a valid choice:\n"
                "riddle"
            )
    elif(player.location=="boss_fight"):
        if len(quest)!=0:
            return PlainTextResponse(
                "You must complete all quests to fight with boss"
            )
        
        boss_health = getattr(player, "boss_health", 150)
        if player.state is None:
            if action.choice=="enter":
                player.state="boss"
                player.boss_health=150
                return PlainTextResponse(
                    "A massive Shadow Dragon appears!\n"
                    "Boss Health: 150HP\n\n"
                    "Choose your action:\n"
                    "attack\n"
                    "heavy_attack\n"
                    "heal\n"
                )
            return PlainTextResponse(
                "Enter a valid choice:\n"
                "enter"
            )
        elif player.state=="boss":
            if (action.choice=="attack"):
                damage=random.randint(10,20)
                if "diamond_sword" in player.armor:
                    damage+=15
                elif "iron_sword" in player.armor:
                    damage+=8
                player.boss_health-=damage
                if player.boss_health <= 0:
                    player.state = None
                    return PlainTextResponse(
                        f"You dealt {damage} damage!\n"
                        "The Shadow Dragon has been defeated!\n"
                        "YOU WIN THE GAME!"
                    )
                boss_damage=random.randint(8,18)
                player.health-=boss_damage
                if player.health<=0:
                    player.state=None
                    player.location="game_over"
                return PlainTextResponse(
                    f"You dealt {damage} damage.\n"
                    f"The boss dealt {boss_damage} damage.\n"
                    "You were defeated...\n"
                    "GAME OVER"
                )
            return PlainTextResponse(
                f"You dealt {damage} damage!\n"
                f"Boss HP: {player.boss_health}\n\n"
                f"The boss attacked back for {boss_damage} damage!\n"
                f"Your HP: {player.health}\n\n"
                "Choose:\n"
                "attack\n"
                "heavy_attack\n"
                "heal"
            )
        elif action.choice=="heavy_attack":

            hit=random.randint(0,1)
            if hit==1:
                damage=random.randint(25,40)
                if "diamod_sword" in player.armor:
                    damage+=20
                elif "iron_sword" in player.armor:
                    damage+=10
                player.boss_health-=damage
                if boss_health<=0:
                    player.state=None
                    return PlainTextResponse(
                        f"CRITICAL HIT! You dealt {damage} damage!\n"
                        "The Shadow Dragon has been defeated!\n"
                        "YOU WIN THE GAME!"
                    )
                boss_damage=random.randint(10,20)
                player.health-=boss_damage
                if player.health<=0:
                    player.state=None
                    player.location="game_over"
                    return PlainTextResponse(
                            "You were defeated...\n"
                            "GAME OVER"
                    )
                return PlainTextResponse(
                        f"Critical hit! You dealt {damage} damage!\n"
                        f"Boss HP: {player.boss_health}\n\n"
                        f"The boss attacked back for {boss_damage} damage!\n"
                        f"Your HP: {player.health}"
                )
            else:
                boss_damage=random.randint(15,25)
                player.health-=boss_damage
                if (player.health<=0):
                    player.state=None
                    player.location="game_over"
                    return PlainTextResponse(
                        "Your heavy attack missed!\n"
                        "The boss defeated you...\n"
                        "GAME OVER"
                    )
                return PlainTextResponse(
                    f"Your heavy attack missed!\n"
                    f"The boss attacked for {boss_damage} damage!\n"
                    f"Your HP: {player.health}"
                )
        elif action.choice=="heal":
            if player.inventory["health_potion"]<=0:
                return PlainTextResponse(
                    "You do not have any health potions!"
                )
            player.inventory["health_potion"] -= 1
            player.health += 30
            if player.health>=200:
                player.health=200
            boss_damage = random.randint(5, 15)
            player.health -= boss_damage

            if player.health <= 0:
                player.state = None
                player.location = "game_over"
                return PlainTextResponse(
                    "You healed, but the boss defeated you...\n"
                    "GAME OVER"
                )
            return PlainTextResponse(
                f"You healed 35 HP!\n"
                f"The boss attacked for {boss_damage} damage!\n"
                f"Your HP: {player.health}\n"
                f"Boss HP: {player.boss_health}"
            )
        else:
            return PlainTextResponse(
                "Choose a valid move:\n"
                "attack\n"
                "heavy_attack\n"
                "heal"
            )
    elif(player.location=="game_over"):
        return game_over()                
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
        "player_coins":player.coins,
        "player_inventory":player.inventory,
        "player_armor":player.armor
    }


# @app.get("/rules"):

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)