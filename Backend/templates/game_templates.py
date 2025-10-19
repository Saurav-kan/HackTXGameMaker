"""
Game Templates and Generation Patterns
Predefined templates and patterns for common game types
"""

import json
import random
from typing import Dict, List, Any

class GameTemplate:
    """Base class for game templates"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    def generate_concept(self, theme: str = None) -> Dict[str, Any]:
        """Generate game concept based on template"""
        raise NotImplementedError
    
    def generate_level_pattern(self, level_number: int) -> Dict[str, Any]:
        """Generate level pattern based on template"""
        raise NotImplementedError

class AdventureTemplate(GameTemplate):
    """Adventure game template"""
    
    def __init__(self):
        super().__init__(
            "Adventure",
            "Exploration-based games with collection mechanics"
        )
    
    def generate_concept(self, theme: str = None) -> Dict[str, Any]:
        return {
            "title": f"{theme or 'Mystic'} Adventure",
            "description": "Explore mysterious lands, collect treasures, and avoid dangerous creatures",
            "genre": "adventure",
            "theme": theme or "fantasy",
            "objective": "Collect all treasures while exploring the world",
            "mechanics": [
                "exploration",
                "collection",
                "avoidance",
                "discovery"
            ],
            "player_abilities": [
                "move",
                "collect",
                "explore"
            ],
            "enemies": [
                {"name": "Guardian", "behavior": "patrols treasure areas", "difficulty": "easy"},
                {"name": "Shadow Beast", "behavior": "chases when player is near", "difficulty": "medium"},
                {"name": "Ancient Spirit", "behavior": "teleports and attacks", "difficulty": "hard"}
            ],
            "powerups": [
                {"name": "Health Potion", "effect": "restores health"},
                {"name": "Speed Boots", "effect": "increases movement speed"},
                {"name": "Treasure Map", "effect": "reveals hidden treasures"}
            ],
            "level_progression": "Open world exploration with increasing danger",
            "scoring_system": "Points for treasures collected and areas discovered",
            "visual_style": "Mystical and atmospheric with glowing elements",
            "sound_theme": "Ambient fantasy with magical chimes"
        }
    
    def generate_level_pattern(self, level_number: int) -> Dict[str, Any]:
        # Generate more complex layouts for adventure games
        width, height = 1000, 800
        obstacles = []
        powerups = []
        enemies = []
        
        # Create maze-like structure
        for i in range(0, width, 100):
            for j in range(0, height, 100):
                if random.random() < 0.3:  # 30% chance of obstacle
                    obstacles.append({
                        "x": i + random.randint(0, 50),
                        "y": j + random.randint(0, 50),
                        "width": random.randint(30, 80),
                        "height": random.randint(30, 80),
                        "type": random.choice(["wall", "rock", "tree"])
                    })
        
        # Add powerups in hidden areas
        for _ in range(3 + level_number):
            powerups.append({
                "x": random.randint(50, width - 50),
                "y": random.randint(50, height - 50),
                "type": random.choice(["health", "speed", "treasure_map"])
            })
        
        # Add enemies with patrol paths
        for _ in range(2 + level_number):
            x, y = random.randint(100, width - 100), random.randint(100, height - 100)
            patrol_path = [
                [x, y],
                [x + random.randint(-100, 100), y + random.randint(-100, 100)],
                [x + random.randint(-100, 100), y + random.randint(-100, 100)]
            ]
            enemies.append({
                "x": x, "y": y,
                "type": random.choice(["basic", "aggressive", "fast"]),
                "patrol_path": patrol_path
            })
        
        return {
            "level_number": level_number,
            "name": f"Mystic Realm {level_number}",
            "description": f"Explore the {level_number}th realm of mystery",
            "size": {"width": width, "height": height},
            "spawn_points": [{"x": 50, "y": 50, "type": "player"}],
            "obstacles": obstacles,
            "powerups": powerups,
            "enemies": enemies,
            "objectives": [
                {"type": "collect", "target": "treasures", "count": 5 + level_number},
                {"type": "explore", "target": "areas", "count": 3}
            ],
            "difficulty": "medium" if level_number <= 3 else "hard",
            "time_limit": 180 + (level_number * 30)
        }

class ActionTemplate(GameTemplate):
    """Action game template"""
    
    def __init__(self):
        super().__init__(
            "Action",
            "Fast-paced games with combat and quick reflexes"
        )
    
    def generate_concept(self, theme: str = None) -> Dict[str, Any]:
        return {
            "title": f"{theme or 'Epic'} Action",
            "description": "Fast-paced action game with intense combat and quick reflexes",
            "genre": "action",
            "theme": theme or "sci-fi",
            "objective": "Survive waves of enemies and achieve high scores",
            "mechanics": [
                "combat",
                "evasion",
                "power-ups",
                "scoring"
            ],
            "player_abilities": [
                "move",
                "dash",
                "collect"
            ],
            "enemies": [
                {"name": "Drone", "behavior": "flies in patterns", "difficulty": "easy"},
                {"name": "Hunter", "behavior": "aggressively chases player", "difficulty": "medium"},
                {"name": "Boss", "behavior": "complex attack patterns", "difficulty": "hard"}
            ],
            "powerups": [
                {"name": "Shield", "effect": "temporary invincibility"},
                {"name": "Multi-shot", "effect": "increased firepower"},
                {"name": "Speed Boost", "effect": "increased movement speed"}
            ],
            "level_progression": "Wave-based progression with increasing enemy density",
            "scoring_system": "Points for enemies defeated and survival time",
            "visual_style": "Bright, energetic with particle effects",
            "sound_theme": "Electronic music with intense beats"
        }
    
    def generate_level_pattern(self, level_number: int) -> Dict[str, Any]:
        width, height = 800, 600
        obstacles = []
        powerups = []
        enemies = []
        
        # Minimal obstacles for fast action
        for _ in range(2 + level_number):
            obstacles.append({
                "x": random.randint(100, width - 100),
                "y": random.randint(100, height - 100),
                "width": random.randint(40, 80),
                "height": random.randint(40, 80),
                "type": "barrier"
            })
        
        # Powerups scattered around
        for _ in range(2 + level_number):
            powerups.append({
                "x": random.randint(50, width - 50),
                "y": random.randint(50, height - 50),
                "type": random.choice(["shield", "multi_shot", "speed_boost"])
            })
        
        # Many enemies for action
        for _ in range(5 + level_number * 2):
            enemies.append({
                "x": random.randint(50, width - 50),
                "y": random.randint(50, height - 50),
                "type": random.choice(["drone", "hunter", "boss"]),
                "patrol_path": []
            })
        
        return {
            "level_number": level_number,
            "name": f"Action Zone {level_number}",
            "description": f"Survive wave {level_number} of enemies",
            "size": {"width": width, "height": height},
            "spawn_points": [{"x": width // 2, "y": height // 2, "type": "player"}],
            "obstacles": obstacles,
            "powerups": powerups,
            "enemies": enemies,
            "objectives": [
                {"type": "survive", "target": "time", "count": 60 + (level_number * 20)},
                {"type": "defeat", "target": "enemies", "count": 10 + (level_number * 5)}
            ],
            "difficulty": "hard",
            "time_limit": 60 + (level_number * 20)
        }

class PuzzleTemplate(GameTemplate):
    """Puzzle game template"""
    
    def __init__(self):
        super().__init__(
            "Puzzle",
            "Logic-based games requiring problem-solving"
        )
    
    def generate_concept(self, theme: str = None) -> Dict[str, Any]:
        return {
            "title": f"{theme or 'Mind'} Puzzle",
            "description": "Solve challenging puzzles using logic and strategy",
            "genre": "puzzle",
            "theme": theme or "abstract",
            "objective": "Solve puzzles by moving blocks and activating switches",
            "mechanics": [
                "block_pushing",
                "switch_activation",
                "pathfinding",
                "logic"
            ],
            "player_abilities": [
                "move",
                "push",
                "activate"
            ],
            "enemies": [
                {"name": "Guardian", "behavior": "blocks certain paths", "difficulty": "easy"},
                {"name": "Timer", "behavior": "creates time pressure", "difficulty": "medium"}
            ],
            "powerups": [
                {"name": "Extra Move", "effect": "grants additional moves"},
                {"name": "Hint", "effect": "shows solution path"},
                {"name": "Reset", "effect": "resets puzzle state"}
            ],
            "level_progression": "Increasingly complex puzzle layouts",
            "scoring_system": "Points for efficiency and speed of solution",
            "visual_style": "Clean, geometric with clear visual hierarchy",
            "sound_theme": "Calm, ambient music with puzzle-solving sounds"
        }
    
    def generate_level_pattern(self, level_number: int) -> Dict[str, Any]:
        width, height = 600, 600
        obstacles = []
        powerups = []
        enemies = []
        
        # Create puzzle layout
        grid_size = 40
        for i in range(0, width, grid_size):
            for j in range(0, height, grid_size):
                if random.random() < 0.4:  # 40% chance of obstacle
                    obstacles.append({
                        "x": i, "y": j,
                        "width": grid_size,
                        "height": grid_size,
                        "type": "puzzle_block"
                    })
        
        # Add switches and powerups
        for _ in range(2 + level_number):
            powerups.append({
                "x": random.randint(50, width - 50),
                "y": random.randint(50, height - 50),
                "type": random.choice(["extra_move", "hint", "reset"])
            })
        
        # Minimal enemies for puzzle games
        if level_number > 2:
            enemies.append({
                "x": random.randint(100, width - 100),
                "y": random.randint(100, height - 100),
                "type": "guardian",
                "patrol_path": []
            })
        
        return {
            "level_number": level_number,
            "name": f"Puzzle Chamber {level_number}",
            "description": f"Solve the {level_number}th puzzle",
            "size": {"width": width, "height": height},
            "spawn_points": [{"x": 50, "y": 50, "type": "player"}],
            "obstacles": obstacles,
            "powerups": powerups,
            "enemies": enemies,
            "objectives": [
                {"type": "solve", "target": "puzzle", "count": 1},
                {"type": "efficiency", "target": "moves", "count": 20 - level_number}
            ],
            "difficulty": "medium",
            "time_limit": 300 - (level_number * 30)
        }

class TemplateManager:
    """Manages game templates and pattern generation"""
    
    def __init__(self):
        self.templates = {
            "adventure": AdventureTemplate(),
            "action": ActionTemplate(),
            "puzzle": PuzzleTemplate()
        }
    
    def get_template(self, template_name: str) -> GameTemplate:
        """Get a specific template"""
        return self.templates.get(template_name.lower())
    
    def list_templates(self) -> List[str]:
        """List available templates"""
        return list(self.templates.keys())
    
    def generate_game_from_template(self, template_name: str, theme: str = None, num_levels: int = 3) -> Dict[str, Any]:
        """Generate complete game from template"""
        template = self.get_template(template_name)
        if not template:
            raise ValueError(f"Template '{template_name}' not found")
        
        concept = template.generate_concept(theme)
        levels = []
        
        for i in range(1, num_levels + 1):
            level = template.generate_level_pattern(i)
            levels.append(level)
        
        return {
            "concept": concept,
            "levels": levels,
            "template": template_name,
            "num_levels": num_levels
        }
    
    def get_random_template(self) -> str:
        """Get a random template name"""
        return random.choice(list(self.templates.keys()))
    
    def get_template_suggestions(self, theme: str) -> List[str]:
        """Get template suggestions based on theme"""
        theme_lower = theme.lower()
        
        suggestions = []
        if any(word in theme_lower for word in ["adventure", "explore", "quest", "journey"]):
            suggestions.append("adventure")
        if any(word in theme_lower for word in ["action", "fight", "battle", "combat", "war"]):
            suggestions.append("action")
        if any(word in theme_lower for word in ["puzzle", "solve", "logic", "brain", "mind"]):
            suggestions.append("puzzle")
        
        # If no specific matches, return all templates
        if not suggestions:
            suggestions = list(self.templates.keys())
        
        return suggestions

# Predefined themes for quick generation
THEME_COLLECTIONS = {
    "fantasy": [
        "Medieval Castle", "Magic Forest", "Dragon's Lair", "Elven Kingdom",
        "Wizard's Tower", "Mystic Caverns", "Fairy Realm", "Ancient Ruins"
    ],
    "sci-fi": [
        "Space Station", "Alien Planet", "Cyber City", "Robot Factory",
        "Quantum Realm", "Neon District", "Mars Colony", "Time Machine"
    ],
    "horror": [
        "Haunted Mansion", "Dark Forest", "Abandoned Hospital", "Creepy Basement",
        "Ghost Town", "Vampire Castle", "Zombie Apocalypse", "Nightmare Realm"
    ],
    "nature": [
        "Tropical Island", "Mountain Peak", "Desert Oasis", "Arctic Tundra",
        "Ocean Depths", "Jungle Temple", "Volcano Crater", "Crystal Caves"
    ],
    "urban": [
        "City Streets", "Underground Metro", "Skyscraper", "Shopping Mall",
        "Amusement Park", "Construction Site", "Airport Terminal", "Subway Station"
    ]
}

def get_random_theme(category: str = None) -> str:
    """Get a random theme from a category"""
    if category and category in THEME_COLLECTIONS:
        return random.choice(THEME_COLLECTIONS[category])
    else:
        all_themes = []
        for themes in THEME_COLLECTIONS.values():
            all_themes.extend(themes)
        return random.choice(all_themes)

def get_theme_categories() -> List[str]:
    """Get all available theme categories"""
    return list(THEME_COLLECTIONS.keys())
