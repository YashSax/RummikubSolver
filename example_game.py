from game import RummikubGame
from player import Player

from utils import *

# example_game = RummikubGame(num_players=4)
# players = example_game.deal_players()

# print("Player 0 bank")
# for tile in players[0].bank:
#     print(tile)

# print("\nPlayer 3 bank")
# for tile in players[3].bank:
#     print(tile)

# assert False

# while True:
#     for player in players:
#         print("Player:", player.player_id, "Turn:", example_game.get_board_info()[0])
#         print("Board:")
#         for tile_group in example_game.get_board_info()[1]:
#             print(tile_group)
        
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
        
#         print("-" * 80)

required_tiles = [
    Tile(TileType.RED, 1, 11),
    Tile(TileType.BLUE, 1, 11),
    Tile(TileType.ORANGE, 1, 11),

    Tile(TileType.BLACK, 1, 5),
    Tile(TileType.BLUE, 1, 5),
    Tile(TileType.RED, 1, 5),
    Tile(TileType.ORANGE, 1, 5),
    
    Tile(TileType.ORANGE, 1, 10),
    Tile(TileType.ORANGE, 2, 11),
    Tile(TileType.ORANGE, 1, 12),
    
    Tile(TileType.BLACK, 1, 8),
    Tile(TileType.BLACK, 1, 9),
    Tile(TileType.BLACK, 1, 10),
    Tile(TileType.BLACK, 1, 11),
    Tile(TileType.BLACK, 1, 12),
    Tile(TileType.BLACK, 1, 13),
    
    Tile(TileType.BLUE, 1, 10),
    Tile(TileType.ORANGE, 2, 10),
    Tile(TileType.BLACK, 2, 10),
    Tile(TileType.RED, 1, 10),
    
    Tile(TileType.BLACK, 1, 7),
    Tile(TileType.ORANGE, 1, 7),
    Tile(TileType.RED, 1, 7),

    
    Tile(TileType.RED, 1, 13),
    Tile(TileType.BLACK, 2, 13),
    Tile(TileType.BLUE, 1, 13),
    
    Tile(TileType.BLUE, 1, 3),
    Tile(TileType.JOKER, 1),
    Tile(TileType.BLUE, 2, 5),
]

player_bank = [
    Tile(TileType.BLACK, 1, 3),
    Tile(TileType.BLACK, 1, 4),
    Tile(TileType.BLUE, 1, 8),
    Tile(TileType.BLUE, 2, 8),
    Tile(TileType.RED, 1, 2),
]

def find_duplicates(l):
    d = {}
    for i in l:
        d[i] = d.get(i, 0) + 1
    
    for k, v in d.items():
        if v > 1:
            print("Duplicate:", k)

combined = required_tiles + player_bank
find_duplicates(combined)
assert len(combined) == len(set(combined))
player_bank = set(player_bank)
required_tiles = set(required_tiles)
combined = set(combined)

print("Total number of tiles:", len(combined))
player = Player(0, [])

import time
start_time = time.time()
optimal_groups = player.search_groups(combined, required_tiles)
print(f"Search took {time.time() - start_time:.3f} seconds")

print(optimal_groups)
for tile_group in optimal_groups:
    print(tile_group)

print(player.info)


# player = Player(0, [])

# required_tiles = [
#     Tile(TileType.RED, 1, 11),
#     Tile(TileType.BLUE, 1, 11),
#     Tile(TileType.ORANGE, 1, 11),

#     Tile(TileType.BLACK, 1, 5),
#     Tile(TileType.BLUE, 1, 5),
#     Tile(TileType.RED, 1, 5),
#     Tile(TileType.ORANGE, 1, 5),
    
#     Tile(TileType.ORANGE, 1, 10),
#     Tile(TileType.ORANGE, 2, 11),
#     Tile(TileType.ORANGE, 1, 12),
    
#     Tile(TileType.BLACK, 1, 8),
#     Tile(TileType.BLACK, 1, 9),
#     Tile(TileType.BLACK, 1, 10),
#     Tile(TileType.BLACK, 1, 11),
#     Tile(TileType.BLACK, 1, 12),
#     Tile(TileType.BLACK, 1, 13),
    
#     Tile(TileType.BLUE, 1, 10),
#     Tile(TileType.ORANGE, 2, 10),
#     Tile(TileType.BLACK, 2, 10),
#     Tile(TileType.RED, 1, 10),
    
#     Tile(TileType.BLACK, 1, 7),
#     Tile(TileType.ORANGE, 1, 7),
#     Tile(TileType.RED, 1, 7),
    
#     Tile(TileType.RED, 1, 13),
#     Tile(TileType.BLACK, 2, 13),
#     Tile(TileType.BLUE, 1, 13),
    
#     Tile(TileType.BLUE, 1, 3),
#     Tile(TileType.JOKER, 1),
#     Tile(TileType.BLUE, 2, 5),
# ]

# assert len(set(required_tiles)) == len(required_tiles)

# chosen_tile_groups = player.search_groups(set(required_tiles), set())
# assert sum(len(tile_group.tiles) for tile_group in chosen_tile_groups) == len(required_tiles)



# board = [
#     Tile(TileType.BLUE, 1, 1), Tile(TileType.RED, 1, 1), Tile(TileType.ORANGE, 1, 1), Tile(TileType.BLACK, 1, 1),
#     Tile(TileType.RED, 1, 8), Tile(TileType.ORANGE, 1, 8), Tile(TileType.BLACK, 1, 8),
#     Tile(TileType.BLACK, 1, 5), Tile(TileType.BLACK, 1, 6), Tile(TileType.BLACK, 1, 7),
#     Tile(TileType.JOKER, 1), Tile(TileType.ORANGE, 1, 9), Tile(TileType.ORANGE, 1, 10), Tile(TileType.ORANGE, 1, 12),
#     Tile(TileType.RED, 1, 5), Tile(TileType.ORANGE, 1, 5), Tile(TileType.BLACK, 2, 5),
#     Tile(TileType.RED, 1, 10), Tile(TileType.BLUE, 2, 10), Tile(TileType.ORANGE, 2, 10)
# ]

# assert len(board) == len(set(board))
# board = set(board)

# player_bank = set([
#     Tile(TileType.BLUE, 1, 2),
#     Tile(TileType.RED, 1, 4),
#     Tile(TileType.ORANGE, 1, 11),
#     Tile(TileType.RED, 1, 6),
#     Tile(TileType.BLUE, 1, 4)
# ])

# player = Player(0, [])
# optimal_groups = player.search_groups(board | player_bank, board)

# for tile_group in optimal_groups:
#     print(tile_group)

# print("Num tiles used:", sum(len(tile_group.tiles) for tile_group in optimal_groups))
# print("Total number of tiles:", len(board))

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
