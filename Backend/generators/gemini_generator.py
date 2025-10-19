"""
Gemini API Integration for Game Generation
Handles all interactions with Google's Gemini AI for autonomous game creation
"""

import os
import json
import google.generativeai as genai
from typing import Dict, List, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiGameGenerator:
    """Main class for interfacing with Gemini AI for game generation"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Gemini client"""
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("Gemini API key not found. Set GEMINI_API_KEY environment variable.")
        
        genai.configure(api_key=self.api_key)
        # Try different model names for compatibility
        try:
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        except:
            try:
                self.model = genai.GenerativeModel('gemini-2.5-pro')
            except:
                self.model = genai.GenerativeModel('gemini-pro')
        
    def generate_game_concept(self, theme: str = None) -> Dict[str, Any]:
        """Generate a complete game concept using Gemini"""
        prompt = f"""
        You are an expert game designer. Create a complete game concept for a topdown 2D game.
        
        Theme: {theme or "Choose an engaging theme"}
        
        Please provide a JSON response with the following structure:
        {{
            "title": "Game Title",
            "description": "Brief game description",
            "genre": "Game genre (e.g., action, adventure, puzzle, RPG)",
            "theme": "Visual/atmospheric theme",
            "objective": "Main objective/goal",
            "mechanics": [
                "Core gameplay mechanic 1",
                "Core gameplay mechanic 2",
                "Core gameplay mechanic 3"
            ],
            "player_abilities": [
                "Ability 1",
                "Ability 2",
                "Ability 3"
            ],
            "enemies": [
                {{"name": "Enemy 1", "behavior": "How it acts", "difficulty": "easy/medium/hard"}},
                {{"name": "Enemy 2", "behavior": "How it acts", "difficulty": "easy/medium/hard"}}
            ],
            "powerups": [
                {{"name": "Powerup 1", "effect": "What it does"}},
                {{"name": "Powerup 2", "effect": "What it does"}}
            ],
            "level_progression": "How levels progress",
            "scoring_system": "How points are earned",
            "visual_style": "Art style description",
            "sound_theme": "Audio theme description"
        }}
        
        Make it creative, engaging, and suitable for a topdown 2D game. Focus on clear, implementable mechanics.
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Extract JSON from response
            content = response.text.strip()
            
            # Try to find JSON in the response
            if content.startswith('```json'):
                content = content[7:-3]
            elif content.startswith('```'):
                content = content[3:-3]
            
            game_concept = json.loads(content)
            logger.info(f"Generated game concept: {game_concept.get('title', 'Unknown')}")
            return game_concept
            
        except Exception as e:
            logger.error(f"Error generating game concept: {e}")
            # Return a fallback concept
            return self._get_fallback_concept(theme)
    
    def generate_level_design(self, game_concept: Dict[str, Any], level_number: int = 1) -> Dict[str, Any]:
        """Generate specific level design based on game concept"""
        prompt = f"""
        Based on this game concept, design level {level_number}:
        
        Game: {game_concept.get('title', 'Unknown')}
        Genre: {game_concept.get('genre', 'Unknown')}
        Mechanics: {', '.join(game_concept.get('mechanics', []))}
        
        Provide a JSON response with:
        {{
            "level_number": {level_number},
            "name": "Level name",
            "description": "Level description",
            "size": {{"width": 800, "height": 600}},
            "spawn_points": [
                {{"x": 100, "y": 100, "type": "player"}},
                {{"x": 400, "y": 300, "type": "enemy"}}
            ],
            "obstacles": [
                {{"x": 200, "y": 200, "width": 50, "height": 50, "type": "wall"}},
                {{"x": 500, "y": 400, "width": 30, "height": 30, "type": "rock"}}
            ],
            "powerups": [
                {{"x": 300, "y": 150, "type": "health"}},
                {{"x": 600, "y": 500, "type": "speed"}}
            ],
            "enemies": [
                {{"x": 350, "y": 250, "type": "basic", "patrol_path": [[350, 250], [400, 250], [400, 300], [350, 300]]}},
                {{"x": 150, "y": 450, "type": "aggressive", "patrol_path": [[150, 450], [200, 450]]}}
            ],
            "objectives": [
                {{"type": "collect", "target": "coins", "count": 5}},
                {{"type": "defeat", "target": "enemies", "count": 3}}
            ],
            "difficulty": "easy/medium/hard",
            "time_limit": 120
        }}
        
        Make it challenging but fair for level {level_number}.
        """
        
        try:
            response = self.model.generate_content(prompt)
            content = response.text.strip()
            
            if content.startswith('```json'):
                content = content[7:-3]
            elif content.startswith('```'):
                content = content[3:-3]
            
            level_design = json.loads(content)
            logger.info(f"Generated level design for level {level_number}")
            return level_design
            
        except Exception as e:
            logger.error(f"Error generating level design: {e}")
            return self._get_fallback_level(level_number)
    
    def generate_game_code(self, game_concept: Dict[str, Any], level_design: Dict[str, Any]) -> str:
        """Generate pygame code for the game"""
        prompt = f"""
        Generate complete pygame code for this game:
        
        Game Concept:
        {json.dumps(game_concept, indent=2)}
        
        Level Design:
        {json.dumps(level_design, indent=2)}
        
        Requirements:
        1. Use pygame for the game engine
        2. Implement topdown 2D view
        3. Include player movement (WASD or arrow keys)
        4. Implement all game mechanics from the concept
        5. Add collision detection
        6. Include basic enemy AI
        7. Add powerup collection
        8. Implement scoring system
        9. Add basic graphics (colored rectangles/circles are fine)
        10. Include game states (menu, playing, game over)
        
        Generate a complete, runnable Python file. Include all necessary imports and a main() function.
        Use simple colored shapes for graphics - no external images needed.
        """
        
        try:
            response = self.model.generate_content(prompt)
            code = response.text.strip()
            
            # Clean up the code if it's wrapped in markdown
            if code.startswith('```python'):
                code = code[9:-3]
            elif code.startswith('```'):
                code = code[3:-3]
            
            logger.info("Generated game code")
            return code
            
        except Exception as e:
            logger.error(f"Error generating game code: {e}")
            return self._get_fallback_code()
    
    def generate_asset_descriptions(self, game_concept: Dict[str, Any]) -> Dict[str, str]:
        """Generate descriptions for game assets"""
        prompt = f"""
        For this game concept, provide simple descriptions for creating basic visual assets:
        
        Game: {game_concept.get('title', 'Unknown')}
        Visual Style: {game_concept.get('visual_style', 'Unknown')}
        
        Provide JSON with asset descriptions:
        {{
            "player": "Description of player character appearance",
            "enemies": {{
                "basic": "Description of basic enemy",
                "aggressive": "Description of aggressive enemy"
            }},
            "powerups": {{
                "health": "Description of health powerup",
                "speed": "Description of speed powerup"
            }},
            "obstacles": {{
                "wall": "Description of wall obstacle",
                "rock": "Description of rock obstacle"
            }},
            "background": "Description of background/environment",
            "ui_elements": {{
                "score": "Description of score display",
                "health_bar": "Description of health bar"
            }}
        }}
        
        Keep descriptions simple and suitable for basic colored shapes or simple graphics.
        """
        
        try:
            response = self.model.generate_content(prompt)
            content = response.text.strip()
            
            if content.startswith('```json'):
                content = content[7:-3]
            elif content.startswith('```'):
                content = content[3:-3]
            
            assets = json.loads(content)
            logger.info("Generated asset descriptions")
            return assets
            
        except Exception as e:
            logger.error(f"Error generating asset descriptions: {e}")
            return self._get_fallback_assets()
    
    def _get_fallback_concept(self, theme: str = None) -> Dict[str, Any]:
        """Fallback game concept if Gemini fails"""
        return {
            "title": f"Adventure Quest {theme or 'Mystery'}",
            "description": "A topdown adventure game where you explore and collect items",
            "genre": "adventure",
            "theme": theme or "fantasy",
            "objective": "Collect all coins while avoiding enemies",
            "mechanics": ["movement", "collection", "avoidance"],
            "player_abilities": ["move", "collect"],
            "enemies": [
                {"name": "Guard", "behavior": "patrols", "difficulty": "easy"},
                {"name": "Hunter", "behavior": "chases player", "difficulty": "medium"}
            ],
            "powerups": [
                {"name": "Health", "effect": "restores health"},
                {"name": "Speed", "effect": "increases movement speed"}
            ],
            "level_progression": "Linear progression with increasing difficulty",
            "scoring_system": "Points for collecting items and surviving",
            "visual_style": "Simple colored shapes",
            "sound_theme": "Retro arcade style"
        }
    
    def _get_fallback_level(self, level_number: int) -> Dict[str, Any]:
        """Fallback level design"""
        return {
            "level_number": level_number,
            "name": f"Level {level_number}",
            "description": f"Basic level {level_number}",
            "size": {"width": 800, "height": 600},
            "spawn_points": [
                {"x": 50, "y": 50, "type": "player"}
            ],
            "obstacles": [
                {"x": 200, "y": 200, "width": 50, "height": 50, "type": "wall"},
                {"x": 500, "y": 300, "width": 30, "height": 30, "type": "rock"}
            ],
            "powerups": [
                {"x": 300, "y": 150, "type": "health"},
                {"x": 600, "y": 400, "type": "speed"}
            ],
            "enemies": [
                {"x": 400, "y": 300, "type": "basic", "patrol_path": [[400, 300], [450, 300]]}
            ],
            "objectives": [
                {"type": "collect", "target": "coins", "count": 3}
            ],
            "difficulty": "easy",
            "time_limit": 120
        }
    
    def _get_fallback_code(self) -> str:
        """Fallback game code"""
        return '''
import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Generated Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.score = 0
        
        # Player
        self.player = pygame.Rect(50, 50, 30, 30)
        self.player_speed = 5
        
        # Collectibles
        self.coins = []
        for _ in range(5):
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 50)
            self.coins.append(pygame.Rect(x, y, 20, 20))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    
    def update(self):
        keys = pygame.key.get_pressed()
        
        # Player movement
        if keys[pygame.K_LEFT] and self.player.x > 0:
            self.player.x -= self.player_speed
        if keys[pygame.K_RIGHT] and self.player.x < SCREEN_WIDTH - self.player.width:
            self.player.x += self.player_speed
        if keys[pygame.K_UP] and self.player.y > 0:
            self.player.y -= self.player_speed
        if keys[pygame.K_DOWN] and self.player.y < SCREEN_HEIGHT - self.player.height:
            self.player.y += self.player_speed
        
        # Check coin collection
        for coin in self.coins[:]:
            if self.player.colliderect(coin):
                self.coins.remove(coin)
                self.score += 10
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw player
        pygame.draw.rect(self.screen, BLUE, self.player)
        
        # Draw coins
        for coin in self.coins:
            pygame.draw.rect(self.screen, YELLOW, coin)
        
        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
'''
    
    def _get_fallback_assets(self) -> Dict[str, str]:
        """Fallback asset descriptions"""
        return {
            "player": "Blue rectangle representing the player character",
            "enemies": {
                "basic": "Red rectangle for basic enemy",
                "aggressive": "Dark red rectangle for aggressive enemy"
            },
            "powerups": {
                "health": "Green circle for health powerup",
                "speed": "Yellow circle for speed powerup"
            },
            "obstacles": {
                "wall": "Gray rectangle for wall obstacle",
                "rock": "Brown circle for rock obstacle"
            },
            "background": "Black background",
            "ui_elements": {
                "score": "White text for score display",
                "health_bar": "Red rectangle for health bar"
            }
        }
