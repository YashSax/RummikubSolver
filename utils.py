from enum import Enum
from typing import List

class TileType(Enum):
    BLUE = 1
    RED = 2
    ORANGE = 3
    BLACK = 4
    JOKER = 5

enum_to_color = {
    TileType.BLUE: "Blue",
    TileType.RED: "Red", 
    TileType.ORANGE: "Orange",
    TileType.BLACK: "Black",
    TileType.JOKER: "Joker",
}

class Tile:
    def __init__(self, tile_type: TileType, tile_id: int, number: int = -1):
        # Jokers have number=-1, tile_type=JOKER
        # There are two instances of each color-number pair. The tile_id distinguishes between them.
        self.number = number
        self.tile_id = tile_id
        self.tile_type = tile_type
    
    def __str__(self):
        if self.tile_type == TileType.JOKER:
            return "JOKER"
        return f"{enum_to_color[self.tile_type]}_{self.number}"
    
    def __eq__(self, other):
        if not isinstance(other, Tile):
            return False
        return self.number == other.number and self.tile_type == other.tile_type
    
    def __hash__(self):
        return hash((self.tile_type, self.tile_id, self.number))


class TileGroup:
    def __init__(self, tiles: List[Tile]=[]):
        self.tiles = tiles

    def is_valid(self) -> bool:
        if len(self.tiles) < 3:
            return False

        jokers = sum(1 for tile in self.tiles if tile.tile_type == TileType.JOKER)
        non_joker_tiles = [tile for tile in self.tiles if tile.tile_type != TileType.JOKER]
        
        # Check same number, different colors.
        if len(set(tile.number for tile in non_joker_tiles)) == 1:
            colors = set(tile.tile_type for tile in non_joker_tiles)
            return (
                len(colors) + jokers == len(self.tiles) and
                len(colors) + jokers <= 4
            )
        
        # Check same color, consecutive numbers.
        if len(set(tile.tile_type for tile in non_joker_tiles)) == 1:
            numbers = sorted(tile.number for tile in non_joker_tiles)
            gaps = 0
            for i in range(len(numbers)-1):
                if numbers[i + 1] == numbers[i]:
                    return False
                gaps += numbers[i+1] - numbers[i] - 1

            if gaps <= jokers and numbers[-1] - numbers[0] == len(self.tiles) - 1:
                return True
            
            # Cover the case if you have a huge consecutive group.
            if jokers - gaps == 1:
                return len(numbers) <= 12
            if jokers - gaps == 2:
                return len(numbers) <= 11
            
        return False

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TileGroup):
            return False
        for tile in self.tiles:
            if tile not in other.tiles:
                return False
        return True
    
    def __str__(self):
        return "[" + ", ".join(str(tile) for tile in self.tiles) + "]"
