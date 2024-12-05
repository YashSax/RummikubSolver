from game import RummikubGame
from player import Player

from utils import *

example_game = RummikubGame(num_players=2)
players = example_game.deal_players()

player_1 = players[0]
player_2 = players[1]

print("Player 1 Bank Before:")
for tile in player_1.bank:
    print(tile, end=" ")

board_info = example_game.get_board_info()
player_move = player_1.generate_move(board_info)
print("\n\nPlayer 1 Move:")
for tile_group in player_move:
    print(tile_group)

example_game.step(player_move, player_1)

print("\nBoard state after:")
for tile_group in example_game.get_board_info()[1]:
    print(tile_group)


print("Player 2 Bank Before:")
for tile in player_2.bank:
    print(tile, end=" ")

board_info = example_game.get_board_info()
player_move = player_2.generate_move(board_info)
print("\n\nPlayer 2 Move:")
for tile_group in player_move:
    print(tile_group)

example_game.step(player_move, player_1)

print("\nBoard state after:")
for tile_group in example_game.get_board_info()[1]:
    print(tile_group)





# for tile_group in chosen_tile_groups:
#     print(tile_group)

# from collections import defaultdict
# game = RummikubGame(num_players=1)
# tiles = game.all_tiles

# player = Player(0, [])
# tile_group_map = player.find_groups(tiles)

# tile_groups = defaultdict(list)
# for tile, groups in tile_group_map.items():
#     for group in groups:
#         tile_groups[group].append(tile)

# print(len(tile_groups))
# for tile_list in tile_groups.values():
#     assert TileGroup(tile_list).is_valid(), " ".join([str(tile) for tile in tile_list])
