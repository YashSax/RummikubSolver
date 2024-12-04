# Run with `pytest tests.py`
from utils import TileGroup, Tile, TileType
from player import Player

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
        