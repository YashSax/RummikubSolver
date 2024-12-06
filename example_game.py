from game import RummikubGame
from player import Player

from utils import *

# example_game = RummikubGame(num_players=1)
# players = example_game.deal_players()

# while True:
#     for player in players:
#         print("Board:")
#         for tile_group in example_game.get_board_info()[1]:
#             print(tile_group)
        
#         print(player.player_id, len(player.bank), len(example_game.board))
#         print("Player Bank")
#         for tile in player.bank:
#             print(tile, end = " ")
#         print()
#         new_board = player.generate_move(example_game.get_board_info())

#         print("New board:")
#         for tile_group in new_board:
#             print(tile_group)
#         example_game.step(new_board, player)

#         if player.is_game_over():
#             print(f"Player {player.player_id} has won!")
#             assert False

# player = Player(0, [])
        
# tiles = [
#     Tile(TileType.BLUE, 1, 1),
#     Tile(TileType.BLUE, 1, 2),
#     Tile(TileType.BLUE, 1, 4),
#     Tile(TileType.JOKER, 1, -1),
#     Tile(TileType.RED, 1, 3),
#     Tile(TileType.BLACK, 1, 3),
# ]
# required_tiles = []

# chosen_tile_groups = player.search_groups(tiles, required_tiles)
# assert len(chosen_tile_groups) == 1
# print(chosen_tile_groups[0])
# assert TileGroup([
#     Tile(TileType.BLUE, 1, 1),
#     Tile(TileType.BLUE, 1, 2),
#     Tile(TileType.BLUE, 1, 3),
#     Tile(TileType.JOKER, 1, -1),
# ]) in chosen_tile_groups


# board = [
#     Tile(TileType.BLACK, 1, 1), Tile(TileType.ORANGE, 1, 1), Tile(TileType.RED, 1, 1), Tile(TileType.BLUE, 1, 1),
#     Tile(TileType.RED, 1, 8), Tile(TileType.ORANGE, 1, 8), Tile(TileType.BLACK, 1, 8),
#     Tile(TileType.BLACK, 1, 5), Tile(TileType.BLACK, 1, 6), Tile(TileType.BLACK, 1, 7),
#     Tile(TileType.ORANGE, 1, 10), Tile(TileType.JOKER, 1), Tile(TileType.ORANGE, 1, 9), Tile(TileType.ORANGE, 1, 12),
#     Tile(TileType.ORANGE, 2, 10), Tile(TileType.RED, 1, 10), Tile(TileType.BLUE, 2, 10),
#     Tile(TileType.ORANGE, 1, 5), Tile(TileType.BLACK, 2, 5), Tile(TileType.RED, 1, 5)
# ]

# assert len(board) == len(set(board))
# board = set(board)

# player_bank = set([
#     Tile(TileType.BLUE, 1, 4),
#     Tile(TileType.RED, 1, 4), 
#     Tile(TileType.BLUE, 1, 2),
#     Tile(TileType.ORANGE, 1, 11),
#     Tile(TileType.RED, 1, 6)
# ])

# player = Player(0, [])
# optimal_groups = player.search_groups(board, board)

# for tile_group in optimal_groups:
#     print(tile_group)

# print("Num tiles used:", sum(len(tile_group.tiles) for tile_group in optimal_groups))
# print("Total number of tiles:", len(board))

player = Player(0, [])
        
tiles = [
    Tile(TileType.ORANGE, 1, 1),
    Tile(TileType.ORANGE, 1, 2),
    Tile(TileType.ORANGE, 1, 3),
    Tile(TileType.ORANGE, 1, 4),
    Tile(TileType.BLUE, 1, 3),
    Tile(TileType.RED, 1, 3),
    Tile(TileType.BLUE, 1, 1),
]
required_tiles = []

chosen_tile_groups = player.search_groups(tiles, required_tiles)
print(chosen_tile_groups[0])
assert chosen_tile_groups == [TileGroup([
    Tile(TileType.ORANGE, 1, 1),
    Tile(TileType.ORANGE, 1, 2),
    Tile(TileType.ORANGE, 1, 3),
    Tile(TileType.ORANGE, 1, 4),
])]

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
