from game import RummikubGame
from player import Player

from utils import *

# example_game = RummikubGame(num_players=4)
# players = example_game.deal_players()

# while True:
#     for player in players:
#         new_board = player.generate_move(example_game.get_board_info())
#         example_game.step(new_board, player)

#         if player.is_game_over():
#             print(f"Player {player.player_id} has won!")

player = Player(0, [])
        
tiles = [
    Tile(TileType.ORANGE, 1, 2),
    Tile(TileType.BLUE, 1, 4),
    Tile(TileType.ORANGE, 1, 5),
    Tile(TileType.JOKER,  1, -1)
]

tile_group_map = player.find_groups(tiles)

for tile, groups in tile_group_map.items():
    print(tile, end=" ")
    print(groups)