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
        self.all_tiles.append(Tile(TileType.JOKER, 1))
        self.all_tiles.append(Tile(TileType.JOKER, 2))

        for color in [TileType.BLACK, TileType.BLUE, TileType.ORANGE, TileType.RED]:
            for number in range(1, 14):
                self.all_tiles.append(Tile(color, 1, number))
                self.all_tiles.append(Tile(color, 2, number))

    def deal_players(self) -> List[Player]:
        for player_id in range(self.num_players):
            player_tiles = set(random.sample(self.all_tiles, 14))
            for tile in player_tiles:
                self.all_tiles.remove(tile)
            
            self.players.append(Player(player_id, player_tiles))
        
        tiles = []
        tiles.extend(self.all_tiles)
        for player in self.players:
            for tile in player.bank:
                tiles.append(tile)
        
        assert len(tiles) == len(set(tiles))
        
        return self.players

    def step(self, new_board: List[TileGroup], player: Player) -> None:
        self.num_turns += 1

        tiles_in_new_board = []
        for tile_group in new_board:
            tiles_in_new_board.extend(tile_group.tiles)
        assert len(tiles_in_new_board) == len(set(tiles_in_new_board)), f"Player {player.player_id} adding a double!"

        # Assume that the player has updated their own bank to remove the tiles they used.
        for tile_group in new_board:
            assert tile_group.is_valid(), f"Tile group {tile_group} is invalid!"
        
        new_tiles = []
        for tile_group in new_board:
            new_tiles.extend(tile_group.tiles)
        
        old_tiles = []
        for tile_group in self.board:
            for tile in tile_group.tiles:
                old_tiles.append(tile)
                assert tile in new_tiles, f"{tile} from original board not in new board."
        
        # Player hasn't made a move, give them a new tile.
        if len(new_tiles) == len(old_tiles):
            assert len(self.all_tiles) > 0, "We've run out of tiles!"
            print("Player didn't make a change to board, giving them a tile")
            tile = random.choice(self.all_tiles)
            self.all_tiles.remove(tile)
            player.bank.add(tile)
        else:
            self.board = new_board
    
    def get_board_info(self) -> Tuple[int, List[TileGroup]]:
        return self.num_turns, deepcopy(self.board)

if __name__ == "__main__":
    game = RummikubGame(num_players=1)
    print("Number of tiles @ beginning:", len(game.all_tiles))

    players = game.deal_players()

    for player in players:
        print("[ ", end="")
        for tile in player.bank:
            print(tile, end=" ")
        print("]")
    