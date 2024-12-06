# Run with `pytest tests.py`
from utils import TileGroup, Tile, TileType
from player import Player
from game import RummikubGame
from collections import defaultdict
import random
random.seed(42)

class TestTileGroup:
    def test_too_short_group(self):
        group = TileGroup([
            Tile(TileType.RED, 1, 1),
            Tile(TileType.RED, 1, 2),
        ])
        assert not group.is_valid()

    def test_same_number_different_colors(self):
        group = TileGroup([
            Tile(TileType.RED, 1, 5),
            Tile(TileType.BLUE, 1, 5), 
            Tile(TileType.BLACK, 1, 5),
        ])
        assert group.is_valid()

    def test_same_number_duplicate_color(self):
        group = TileGroup([
            Tile(TileType.RED, 1, 5),
            Tile(TileType.RED, 1, 5),
            Tile(TileType.BLACK, 1, 5),
        ])
        assert not group.is_valid()

    def test_consecutive_numbers_same_color(self):
        group = TileGroup([
            Tile(TileType.RED, 1, 3),
            Tile(TileType.RED, 1, 4),
            Tile(TileType.RED, 1, 5),
        ])
        assert group.is_valid()

    def test_non_consecutive_numbers(self):
        group = TileGroup([
            Tile(TileType.RED, 1, 3),
            Tile(TileType.RED, 1, 5),
            Tile(TileType.RED, 1, 6),
        ])
        assert not group.is_valid()

    def test_joker_fills_number_gap(self):
        group = TileGroup([
            Tile(TileType.RED, 1, 3),
            Tile(TileType.JOKER, 1),
            Tile(TileType.RED, 1, 5),
        ])
        assert group.is_valid()

    def test_joker_completes_color_set(self):
        group = TileGroup([
            Tile(TileType.RED, 1, 7),
            Tile(TileType.BLUE, 1, 7),
            Tile(TileType.JOKER, 1),
        ])
        assert group.is_valid()

    def test_two_jokers(self):
        group = TileGroup([
            Tile(TileType.RED, 1, 3),
            Tile(TileType.JOKER, 1),
            Tile(TileType.JOKER, 1),
        ])
        assert group.is_valid()
    
    def test_long_sequence(self):
        group = TileGroup([
            Tile(TileType.BLUE, 1, 1),
            Tile(TileType.BLUE, 1, 2),
            Tile(TileType.BLUE, 1, 3),
            Tile(TileType.BLUE, 1, 4),
            Tile(TileType.BLUE, 1, 5),
            Tile(TileType.BLUE, 1, 6),
            Tile(TileType.BLUE, 1, 7),
            Tile(TileType.BLUE, 1, 8),
            Tile(TileType.BLUE, 1, 9),
            Tile(TileType.BLUE, 1, 10),
            Tile(TileType.BLUE, 1, 11),
            Tile(TileType.BLUE, 1, 12),
            Tile(TileType.BLUE, 1, 13),
        ])
        assert group.is_valid()

    def test_too_long_sequence_jokers(self):
        group = TileGroup([
            Tile(TileType.JOKER, 1, -1),
            Tile(TileType.BLUE, 1, 1),
            Tile(TileType.BLUE, 1, 2),
            Tile(TileType.BLUE, 1, 3),
            Tile(TileType.BLUE, 1, 4),
            Tile(TileType.BLUE, 1, 5),
            Tile(TileType.BLUE, 1, 6),
            Tile(TileType.BLUE, 1, 7),
            Tile(TileType.BLUE, 1, 8),
            Tile(TileType.BLUE, 1, 9),
            Tile(TileType.BLUE, 1, 10),
            Tile(TileType.BLUE, 1, 11),
            Tile(TileType.BLUE, 1, 12),
            Tile(TileType.BLUE, 1, 13),
        ])
        assert not group.is_valid()
    
    def test_too_long_sequence_jokers_2(self):
        group = TileGroup([
            Tile(TileType.JOKER, 1, -1),
            Tile(TileType.JOKER, 1, -1),
            Tile(TileType.BLUE, 1, 2),
            Tile(TileType.BLUE, 1, 3),
            Tile(TileType.BLUE, 1, 4),
            Tile(TileType.BLUE, 1, 5),
            Tile(TileType.BLUE, 1, 6),
            Tile(TileType.BLUE, 1, 7),
            Tile(TileType.BLUE, 1, 8),
            Tile(TileType.BLUE, 1, 9),
            Tile(TileType.BLUE, 1, 10),
            Tile(TileType.BLUE, 1, 11),
            Tile(TileType.BLUE, 1, 12),
            Tile(TileType.BLUE, 1, 13),
        ])
        assert not group.is_valid()

class TestPlayerFindGroups:
    def test_basic_same_number_group(self):
        player = Player(0, [])
        
        tiles = [
            Tile(TileType.ORANGE, 1, 1),
            Tile(TileType.RED, 1, 1),
            Tile(TileType.BLUE, 1, 1),
        ]
        
        tile_group_map = player.find_groups(tiles)
        assert tile_group_map == {
            Tile(TileType.ORANGE, 1, 1) : {0},
            Tile(TileType.RED, 1, 1) : {0},
            Tile(TileType.BLUE, 1, 1) : {0},
        }

    def test_basic_sequence_group(self):
        player = Player(0, [])
        
        tiles = [
            Tile(TileType.BLUE, 1, 1),
            Tile(TileType.BLUE, 1, 2), 
            Tile(TileType.BLUE, 1, 3),
        ]
        
        tile_group_map = player.find_groups(tiles)
        assert tile_group_map == {
            Tile(TileType.BLUE, 1, 1) : {0},
            Tile(TileType.BLUE, 1, 2) : {0},
            Tile(TileType.BLUE, 1, 3) : {0},
        }

    def test_with_joker_same_number(self):
        player = Player(0, [])
        
        tiles = [
            Tile(TileType.ORANGE, 1, 1),
            Tile(TileType.RED, 1, 1),
            Tile(TileType.JOKER, 1, -1),
        ]
        
        tile_group_map = player.find_groups(tiles)
        assert tile_group_map == {
            Tile(TileType.ORANGE, 1, 1) : {0},
            Tile(TileType.RED, 1, 1) : {0},
            Tile(TileType.JOKER, 1, -1) : {0},
        }

    def test_with_joker_sequence(self):
        player = Player(0, [])
        
        tiles = [
            Tile(TileType.BLUE, 1, 1),
            Tile(TileType.BLUE, 1, 3),
            Tile(TileType.JOKER, 1, -1),
        ]
        
        tile_group_map = player.find_groups(tiles)
        assert tile_group_map == {
            Tile(TileType.BLUE, 1, 1) : {0},
            Tile(TileType.BLUE, 1, 3) : {0}, 
            Tile(TileType.JOKER, 1, -1) : {0},
        }

    def test_multiple_possible_groups(self):
        player = Player(0, [])
        
        tiles = [
            Tile(TileType.BLUE, 1, 1),
            Tile(TileType.BLUE, 1, 2),
            Tile(TileType.BLUE, 1, 3),
            Tile(TileType.RED, 1, 1),
            Tile(TileType.BLACK, 1, 1),
        ]
        
        tile_group_map = player.find_groups(tiles)
        # Should find both the sequence 1-2-3 and the same number group with 1s
        assert len(tile_group_map[Tile(TileType.BLUE, 1, 1)]) == 2
        assert len(tile_group_map[Tile(TileType.BLUE, 1, 2)]) == 1
        assert len(tile_group_map[Tile(TileType.BLUE, 1, 3)]) == 1
        assert len(tile_group_map[Tile(TileType.RED, 1, 1)]) == 1
        assert len(tile_group_map[Tile(TileType.BLACK, 1, 1)]) == 1      

    def test_valid_tilegroups(self):
        """ Find all possible combinations of tiles (213,536) and check them."""
        game = RummikubGame(num_players=1)
        tiles = game.all_tiles

        player = Player(0, [])
        tile_group_map = player.find_groups(tiles)

        tile_groups = defaultdict(list)
        for tile, groups in tile_group_map.items():
            for group in groups:
                tile_groups[group].append(tile)
        
        print(len(tile_groups))
        for tile_list in tile_groups.values():
            assert TileGroup(tile_list).is_valid(), " ".join([str(tile) for tile in tile_list])

class TestPlayerFindOptimalGroupList:
    def test_simple(self):
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
        assert chosen_tile_groups == [TileGroup([
            Tile(TileType.ORANGE, 1, 1),
            Tile(TileType.ORANGE, 1, 2),
            Tile(TileType.ORANGE, 1, 3),
            Tile(TileType.ORANGE, 1, 4),
        ])]

    def test_same_number_group(self):
        player = Player(0, [])
        
        tiles = [
            Tile(TileType.BLUE, 1, 3),
            Tile(TileType.RED, 1, 3),
            Tile(TileType.BLACK, 1, 3),
        ]
        required_tiles = []

        chosen_tile_groups = player.search_groups(tiles, required_tiles)
        assert chosen_tile_groups == [TileGroup([
            Tile(TileType.BLUE, 1, 3),
            Tile(TileType.RED, 1, 3),
            Tile(TileType.BLACK, 1, 3),
        ])]

    def test_with_joker(self):
        player = Player(0, [])
        
        tiles = [
            Tile(TileType.BLUE, 1, 1),
            Tile(TileType.BLUE, 1, 2),
            Tile(TileType.JOKER, 1, -1),
        ]
        required_tiles = []

        chosen_tile_groups = player.search_groups(tiles, required_tiles)
        assert chosen_tile_groups == [TileGroup([
            Tile(TileType.BLUE, 1, 1),
            Tile(TileType.BLUE, 1, 2),
            Tile(TileType.JOKER, 1, -1),
        ])]

    def test_required_tiles(self):
        player = Player(0, [])
        
        tiles = [
            Tile(TileType.BLUE, 1, 1),
            Tile(TileType.BLUE, 1, 2),
            Tile(TileType.BLUE, 1, 3),
            Tile(TileType.RED, 1, 1),
            Tile(TileType.BLACK, 1, 1),
        ]
        required_tiles = [Tile(TileType.RED, 1, 1)]

        chosen_tile_groups = player.search_groups(tiles, required_tiles)
        assert chosen_tile_groups == [TileGroup([
            Tile(TileType.BLUE, 1, 1),
            Tile(TileType.RED, 1, 1),
            Tile(TileType.BLACK, 1, 1),
        ])]

    def test_joker_hard(self):
        player = Player(0, [])
        
        tiles = [
            Tile(TileType.BLUE, 1, 1),
            Tile(TileType.BLUE, 1, 2),
            Tile(TileType.BLUE, 1, 4),
            Tile(TileType.JOKER, 1, -1),
            Tile(TileType.RED, 1, 3),
            Tile(TileType.BLACK, 1, 3),
        ]
        required_tiles = []

        chosen_tile_groups = player.search_groups(tiles, required_tiles)
        assert len(chosen_tile_groups) == 1
        assert TileGroup([
            Tile(TileType.BLUE, 1, 1),
            Tile(TileType.BLUE, 1, 2),
            Tile(TileType.BLUE, 1, 4),
            Tile(TileType.JOKER, 1, -1),
        ]) in chosen_tile_groups
