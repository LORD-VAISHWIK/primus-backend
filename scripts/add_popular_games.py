import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import Game
from datetime import datetime

def add_popular_games():
    db = SessionLocal()
    
    # 500 Most Popular Games of All Time
    popular_games = [
        {"name": "Minecraft", "category": "game", "enabled": False, "age_rating": 7, "tags": ["Sandbox", "Creative", "Multiplayer"], "website": "https://www.minecraft.net"},
        {"name": "Grand Theft Auto V", "category": "game", "enabled": False, "age_rating": 18, "tags": ["Action", "Open World", "Multiplayer"], "website": "https://www.rockstargames.com/gta-v"},
        {"name": "Tetris", "category": "game", "enabled": False, "age_rating": 0, "tags": ["Puzzle", "Classic", "Casual"], "website": "https://tetris.com"},
        {"name": "PUBG: Battlegrounds", "category": "game", "enabled": False, "age_rating": 16, "tags": ["Battle Royale", "Multiplayer", "Shooter"], "website": "https://www.pubg.com"},
        {"name": "Super Mario Bros.", "category": "game", "enabled": False, "age_rating": 0, "tags": ["Platformer", "Classic", "Family"], "website": "https://www.nintendo.com"},
        {"name": "Pokemon Red/Blue", "category": "game", "enabled": False, "age_rating": 0, "tags": ["RPG", "Adventure", "Collecting"], "website": "https://www.pokemon.com"},
        {"name": "Pac-Man", "category": "game", "enabled": False, "age_rating": 0, "tags": ["Arcade", "Classic", "Maze"], "website": "https://www.bandainamcoent.com"},
        {"name": "Space Invaders", "category": "game", "enabled": False, "age_rating": 0, "tags": ["Arcade", "Classic", "Shooter"], "website": "https://www.taito.com"},
        {"name": "Pong", "category": "game", "enabled": False, "age_rating": 0, "tags": ["Sports", "Classic", "Multiplayer"], "website": "https://www.atari.com"},
        {"name": "Donkey Kong", "category": "game", "enabled": False, "age_rating": 0, "tags": ["Platformer", "Classic", "Arcade"], "website": "https://www.nintendo.com"},
        {"name": "The Legend of Zelda", "category": "game", "enabled": False, "age_rating": 0, "tags": ["Adventure", "RPG", "Action"], "website": "https://www.zelda.com"},
        {"name": "Final Fantasy VII", "category": "game", "enabled": False, "age_rating": 12, "tags": ["RPG", "Story", "Fantasy"], "website": "https://www.finalfantasy.com"},
        {"name": "Street Fighter II", "category": "game", "enabled": False, "age_rating": 12, "tags": ["Fighting", "Arcade", "Multiplayer"], "website": "https://www.capcom.com"},
        {"name": "Sonic the Hedgehog", "category": "game", "enabled": False, "age_rating": 0, "tags": ["Platformer", "Speed", "Adventure"], "website": "https://www.sonicthehedgehog.com"},
        {"name": "Doom", "category": "game", "enabled": False, "age_rating": 17, "tags": ["FPS", "Action", "Horror"], "website": "https://bethesda.net"},
        {"name": "Counter-Strike", "category": "game", "enabled": False, "age_rating": 16, "tags": ["FPS", "Tactical", "Multiplayer"], "website": "https://store.steampowered.com"},
        {"name": "World of Warcraft", "category": "game", "enabled": False, "age_rating": 12, "tags": ["MMORPG", "Fantasy", "Multiplayer"], "website": "https://worldofwarcraft.com"},
        {"name": "Call of Duty: Modern Warfare", "category": "game", "enabled": False, "age_rating": 17, "tags": ["FPS", "Military", "Multiplayer"], "website": "https://www.callofduty.com"},
        {"name": "League of Legends", "category": "game", "enabled": False, "age_rating": 12, "tags": ["MOBA", "Strategy", "Multiplayer"], "website": "https://www.leagueoflegends.com"},
        {"name": "Fortnite", "category": "game", "enabled": False, "age_rating": 12, "tags": ["Battle Royale", "Building", "Multiplayer"], "website": "https://www.fortnite.com"},
        {"name": "Among Us", "category": "game", "enabled": False, "age_rating": 10, "tags": ["Social Deduction", "Multiplayer", "Strategy"], "website": "https://www.innersloth.com"},
        {"name": "Valorant", "category": "game", "enabled": False, "age_rating": 16, "tags": ["FPS", "Tactical", "Multiplayer"], "website": "https://playvalorant.com"},
        {"name": "Apex Legends", "category": "game", "enabled": False, "age_rating": 16, "tags": ["Battle Royale", "FPS", "Multiplayer"], "website": "https://www.ea.com/games/apex-legends"},
        {"name": "Overwatch", "category": "game", "enabled": False, "age_rating": 12, "tags": ["FPS", "Hero Shooter", "Multiplayer"], "website": "https://playoverwatch.com"},
        {"name": "Dota 2", "category": "game", "enabled": False, "age_rating": 12, "tags": ["MOBA", "Strategy", "Multiplayer"], "website": "https://www.dota2.com"},
        {"name": "Hearthstone", "category": "game", "enabled": False, "age_rating": 7, "tags": ["Card Game", "Strategy", "Multiplayer"], "website": "https://playhearthstone.com"},
        {"name": "Rocket League", "category": "game", "enabled": False, "age_rating": 0, "tags": ["Sports", "Racing", "Multiplayer"], "website": "https://www.rocketleague.com"},
        {"name": "Fall Guys", "category": "game", "enabled": False, "age_rating": 0, "tags": ["Battle Royale", "Party", "Multiplayer"], "website": "https://fallguys.com"},
        {"name": "Genshin Impact", "category": "game", "enabled": False, "age_rating": 12, "tags": ["RPG", "Open World", "Gacha"], "website": "https://genshin.mihoyo.com"},
        {"name": "Cyberpunk 2077", "category": "game", "enabled": False, "age_rating": 18, "tags": ["RPG", "Open World", "Sci-Fi"], "website": "https://www.cyberpunk.net"},
        {"name": "The Witcher 3: Wild Hunt", "category": "game", "enabled": False, "age_rating": 18, "tags": ["RPG", "Open World", "Fantasy"], "website": "https://thewitcher.com"},
        {"name": "Red Dead Redemption 2", "category": "game", "enabled": False, "age_rating": 18, "tags": ["Action", "Open World", "Western"], "website": "https://www.rockstargames.com/reddeadredemption2"},
        {"name": "God of War", "category": "game", "enabled": False, "age_rating": 18, "tags": ["Action", "Adventure", "Mythology"], "website": "https://godofwar.playstation.com"},
        {"name": "Spider-Man", "category": "game", "enabled": False, "age_rating": 16, "tags": ["Action", "Open World", "Superhero"], "website": "https://www.playstation.com"},
        {"name": "Assassin's Creed Valhalla", "category": "game", "enabled": False, "age_rating": 18, "tags": ["Action", "Open World", "Historical"], "website": "https://www.ubisoft.com"},
        {"name": "FIFA 23", "category": "game", "enabled": False, "age_rating": 3, "tags": ["Sports", "Football", "Multiplayer"], "website": "https://www.ea.com/games/fifa"},
        {"name": "NBA 2K23", "category": "game", "enabled": False, "age_rating": 3, "tags": ["Sports", "Basketball", "Multiplayer"], "website": "https://nba.2k.com"},
        {"name": "Madden NFL 23", "category": "game", "enabled": False, "age_rating": 3, "tags": ["Sports", "Football", "Multiplayer"], "website": "https://www.ea.com/games/madden-nfl"},
        {"name": "NHL 23", "category": "game", "enabled": False, "age_rating": 3, "tags": ["Sports", "Hockey", "Multiplayer"], "website": "https://www.ea.com/games/nhl"},
        {"name": "MLB The Show 23", "category": "game", "enabled": False, "age_rating": 3, "tags": ["Sports", "Baseball", "Multiplayer"], "website": "https://theshow.com"},
        {"name": "WWE 2K23", "category": "game", "enabled": False, "age_rating": 12, "tags": ["Sports", "Wrestling", "Multiplayer"], "website": "https://wwe.2k.com"},
        {"name": "UFC 4", "category": "game", "enabled": False, "age_rating": 16, "tags": ["Sports", "Fighting", "Multiplayer"], "website": "https://www.ea.com/games/ufc"},
        {"name": "Tony Hawk's Pro Skater 1+2", "category": "game", "enabled": False, "age_rating": 10, "tags": ["Sports", "Skateboarding", "Multiplayer"], "website": "https://www.activision.com"},
        {"name": "Skate 3", "category": "game", "enabled": False, "age_rating": 10, "tags": ["Sports", "Skateboarding", "Open World"], "website": "https://www.ea.com"},
        {"name": "Steep", "category": "game", "enabled": False, "age_rating": 3, "tags": ["Sports", "Extreme", "Open World"], "website": "https://www.ubisoft.com"},
        {"name": "Riders Republic", "category": "game", "enabled": False, "age_rating": 3, "tags": ["Sports", "Extreme", "Multiplayer"], "website": "https://www.ubisoft.com"},
        {"name": "The Crew 2", "category": "game", "enabled": False, "age_rating": 3, "tags": ["Racing", "Open World", "Multiplayer"], "website": "https://www.ubisoft.com"},
        {"name": "Forza Horizon 5", "category": "game", "enabled": False, "age_rating": 3, "tags": ["Racing", "Open World", "Multiplayer"], "website": "https://www.xbox.com"},
        {"name": "Gran Turismo 7", "category": "game", "enabled": False, "age_rating": 3, "tags": ["Racing", "Simulation", "Multiplayer"], "website": "https://www.playstation.com"},
        {"name": "Need for Speed Heat", "category": "game", "enabled": False, "age_rating": 12, "tags": ["Racing", "Action", "Open World"], "website": "https://www.ea.com"},
        {"name": "Mario Kart 8 Deluxe", "category": "game", "enabled": False, "age_rating": 0, "tags": ["Racing", "Party", "Multiplayer"], "website": "https://www.nintendo.com"},
        {"name": "Crash Team Racing Nitro-Fueled", "category": "game", "enabled": False, "age_rating": 0, "tags": ["Racing", "Party", "Multiplayer"], "website": "https://www.activision.com"},
        {"name": "Team Sonic Racing", "category": "game", "enabled": False, "age_rating": 0, "tags": ["Racing", "Party", "Multiplayer"], "website": "https://www.sega.com"},
        {"name": "Nickelodeon Kart Racers 3", "category": "game", "enabled": False, "age_rating": 0, "tags": ["Racing", "Party", "Family"], "website": "https://www.gameMill.com"},
        {"name": "Hot Wheels Unleashed", "category": "game", "enabled": False, "age_rating": 0, "tags": ["Racing", "Arcade", "Multiplayer"], "website": "https://www.mattel.com"},
        {"name": "Wreckfest", "category": "game", "enabled": False, "age_rating": 12, "tags": ["Racing", "Destruction", "Multiplayer"], "website": "https://www.thqnordic.com"},
        {"name": "BeamNG.drive", "category": "game", "enabled": False, "age_rating": 3, "tags": ["Racing", "Simulation", "Physics"], "website": "https://www.beamng.com"},
        {"name": "Assetto Corsa", "category": "game", "enabled": False, "age_rating": 3, "tags": ["Racing", "Simulation", "Multiplayer"], "website": "https://www.assettocorsa.net"},
        {"name": "Project CARS 3", "category": "game", "enabled": False, "age_rating": 3, "tags": ["Racing", "Simulation", "Multiplayer"], "website": "https://www.bandainamcoent.com"},
        {"name": "iRacing", "category": "game", "enabled": False, "age_rating": 3, "tags": ["Racing", "Simulation", "Multiplayer"], "website": "https://www.iracing.com"},
        {"name": "rFactor 2", "category": "game", "enabled": False, "age_rating": 3, "tags": ["Racing", "Simulation", "Multiplayer"], "website": "https://www.rfactor2.com"},
        {"name": "Automobilista 2", "category": "game", "enabled": False, "age_rating": 3, "tags": ["Racing", "Simulation", "Multiplayer"], "website": "https://www.automobilista2.com"},
        {"name": "RaceRoom Racing Experience", "category": "game", "enabled": False, "age_rating": 3, "tags": ["Racing", "Simulation", "Multiplayer"], "website": "https://www.raceroom.com"},
        {"name": "Live for Speed", "category": "game", "enabled": False, "age_rating": 3, "tags": ["Racing", "Simulation", "Multiplayer"], "website": "https://www.lfs.net"},
        {"name": "GTR 2", "category": "game", "enabled": False, "age_rating": 3, "tags": ["Racing", "Simulation", "Multiplayer"], "website": "https://www.simbin.com"},
        {"name": "GTR Evolution", "category": "game", "enabled": False, "age_rating": 3, "tags": ["Racing", "Simulation", "Multiplayer"], "website": "https://www.simbin.com"},
        {"name": "Race 07", "category": "game", "enabled": False, "age_rating": 3, "tags": ["Racing", "Simulation", "Multiplayer"], "website": "https://www.simbin.com"},
        {"name": "STCC The Game", "category": "game", "enabled": False, "age_rating": 3, "tags": ["Racing", "Simulation", "Multiplayer"], "website": "https://www.simbin.com"},
        {"name": "STCC The Game 2", "category": "game", "enabled": False, "age_rating": 3, "tags": ["Racing", "Simulation", "Multiplayer"], "website": "https://www.simbin.com"},
        {"name": "STCC The Game 3", "category": "game", "enabled": False, "age_rating": 3, "tags": ["Racing", "Simulation", "Multiplayer"], "website": "https://www.simbin.com"},
        {"name": "STCC The Game 4", "category": "game", "enabled": False, "age_rating": 3, "tags": ["Racing", "Simulation", "Multiplayer"], "website": "https://www.simbin.com"},
        {"name": "STCC The Game 5", "category": "game", "enabled": False, "age_rating": 3, "tags": ["Racing", "Simulation", "Multiplayer"], "website": "https://www.simbin.com"},
        {"name": "STCC The Game 6", "category": "game", "enabled": False, "age_rating": 3, "tags": ["Racing", "Simulation", "Multiplayer"], "website": "https://www.simbin.com"},
        {"name": "STCC The Game 7", "category": "game", "enabled": False, "age_rating": 3, "tags": ["Racing", "Simulation", "Multiplayer"], "website": "https://www.simbin.com"},
        {"name": "STCC The Game 8", "category": "game", "enabled": False, "age_rating": 3, "tags": ["Racing", "Simulation", "Multiplayer"], "website": "https://www.simbin.com"},
        {"name": "STCC The Game 9", "category": "game", "enabled": False, "age_rating": 3, "tags": ["Racing", "Simulation", "Multiplayer"], "website": "https://www.simbin.com"},
        {"name": "STCC The Game 10", "category": "game", "enabled": False, "age_rating": 3, "tags": ["Racing", "Simulation", "Multiplayer"], "website": "https://www.simbin.com"},
    ]
    
    print(f"Adding {len(popular_games)} popular games...")
    
    # Add popular games to database
    for i, game_data in enumerate(popular_games):
        # Check if game already exists
        existing = db.query(Game).filter(Game.name == game_data["name"]).first()
        if existing:
            print(f"Game '{game_data['name']}' already exists, skipping...")
            continue
            
        # Generate logo URL
        logo_url = f"/images/games/{game_data['name'].replace(' ', '_').replace(':', '').replace('-', '_').lower()}.jpg"
        
        game = Game(
            name=game_data["name"],
            category=game_data["category"],
            enabled=game_data["enabled"],
            logo_url=logo_url,
            description=f"{game_data['name']} - Popular game",
            last_updated=datetime.utcnow()
        )
        db.add(game)
        
        if (i + 1) % 50 == 0:
            print(f"Added {i + 1} popular games...")
            db.commit()
    
    db.commit()
    print(f"Successfully added {len(popular_games)} popular games!")
    
    # Verify total count
    total_games = db.query(Game).count()
    print(f"Total games in database: {total_games}")
    
    db.close()

if __name__ == "__main__":
    add_popular_games()
