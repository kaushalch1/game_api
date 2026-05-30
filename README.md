**API Text Adventure — Routes**

This document describes the HTTP routes implemented in the FastAPI application in [main.py](main.py).

**Overview**: The app exposes a small text-adventure game API. New players are created via `/new_player` which sets a `player_id` cookie; most routes require that cookie to identify the player session.
 WELCOME, ADVENTURER
HOW TO START
- Begin your journey: POST /new_player
- This creates your character automatically
- You will NOT need to enter player_id again (cookies handle it)

CORE GAME ROUTES
1. Explore your current location:
   GET /explore_room
   → Shows where you are and what you can do

2. Move between locations:
   POST /teleport
   → Travel to places like cave, library, merchant, etc.

3. Perform actions in a room:
   POST /choice
   → Example actions depend on location:
     - mine (in cave)
     - brew (in brewery)
     - meditate (in forest)
     - riddle (in library)
     - buy/sell (merchant)
     - upgrade (blacksmith)
     - quest1/quest2/quest3 (quests)

ITEMS AND POTIONS
- Use potions: POST /usepotion
  * health_potion → restores health
  * mining_potion → boosts mining for 2 minutes

PLAYER INFO
- Check status: GET /playerinfo
  → View health, coins, inventory, and armor

MAIN LOCATIONS
- lobby → starting area
- cave → mine stone, iron, diamonds
- brewery → craft potions
- library → solve riddles
- deep_forest → restore health
- merchant → buy and sell items
- quests → complete missions
- blacksmith → upgrade weapons
- boss_fight → final battle

QUEST GOAL
Complete all quests to unlock the final boss.
Defeat the Shadow Dragon to win the game.

IMPORTANT TIPS
- Always start with /new_player
- Your progress is stored in memory and resets if the server restarts
- Use /help anytime to see this guide

**Example usage (curl)**
Create a player and store cookies in `cookies.txt`:
```bash
curl -i -c cookies.txt -X POST http://localhost:8000/new_player
```
Call a protected route using the saved cookie:
```bash
curl -b cookies.txt http://localhost:8000/playerinfo
```
Teleport to the brewery:
```bash
curl -b cookies.txt -H "Content-Type: application/json" -d '{"teleport":"brewery"}' http://localhost:8000/teleport
```
Make a choice (e.g., harvest in brewery):
```bash
curl -b cookies.txt -H "Content-Type: application/json" -d '{"choice":"harvest"}' http://localhost:8000/choice
```

- All sessions are stored in-memory (`players` dict). On restart the state is lost. For production persist sessions externally.
