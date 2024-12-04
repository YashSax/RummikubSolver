from typing import List, Tuple
from player import Player
from utils import Tile, TileType, TileGroup
from copy import deepcopy
import random
random.seed(42)

class RummikubGame:
    def __init__(self, num_players: int):
        self.num_players = num_players

        self.all_tiles = []
        self.initialize_game()
        assert len(self.all_tiles) == 106

        self.board = []
        self.players = []
        self.num_turns = 0
    
    def initialize_game(self):
        self.all_tiles.append(Tile(1, TileType.JOKER))
        self.all_tiles.append(Tile(2, TileType.JOKER))

        for color in [TileType.BLACK, TileType.BLUE, TileType.ORANGE, TileType.RED]:
            for number in range(1, 14):
                self.all_tiles.append(Tile(color, 1, number))
                self.all_tiles.append(Tile(color, 2, number))

    def deal_players(self) -> List[Player]:
        for player_id in range(self.num_players):
            player_tiles = random.sample(self.all_tiles, 14)
            for tile in player_tiles:
                self.all_tiles.remove(tile)
            self.players.append(Player(player_id, player_tiles))
        return self.players

    def step(self, new_board: List[TileGroup], player: Player) -> None:
        self.num_turns += 1

        # Assume that the player has updated their own bank to remove the tiles they used.
        for tile_group in new_board:
            assert tile_group.is_valid(), f"Tile group {tile_group} is invalid!"
        
        new_tiles = []
        for tile_group in new_tiles:
            for tile in tile_group.tiles:
                new_tiles.append(tile)
        
        old_tiles = []
        for tile_group in self.board:
            for tile in tile_group.tiles:
                old_tiles.append(tile)
                assert tile in new_tiles, f"{tile} from original board not in new board."
        
        # Player hasn't made a move, give them a new tile.
        if len(new_tiles) == len(old_tiles):
            assert len(self.all_tiles) > 0, "We've run out of tiles!"
            tile = random.choice(self.all_tiles)
            self.all_tiles.remove(tile)
            player.bank.append(tile)
    
    def get_board_info(self) -> Tuple[int, List[TileGroup]]:
        return self.num_turns // self.num_players, deepcopy(self.board)

if __name__ == "__main__":
    game = RummikubGame(num_players=1)
    print("Number of tiles @ beginning:", len(game.all_tiles))

    players = game.deal_players()

    for player in players:
        print("[ ", end="")
        for tile in player.bank:
            print(tile, end=" ")
        print("]")
    