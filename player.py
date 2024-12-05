from typing import List, Tuple, Dict, Set
from utils import Tile, TileGroup, TileType, enum_to_color
from collections import defaultdict
from itertools import combinations
from copy import deepcopy

class Player:
    def __init__(self, player_id: int, bank: Set[Tile]):
        self.player_id = player_id
        self.bank = bank

        # The tiles in the first move a player makes must be self-contained
        # and must have a sum greater than or equal to 30.
        self.escaped_init = False
    
    def generate_move(self, board_info: Tuple[int, List[TileGroup]]) -> List[TileGroup]:
        round_num, curr_board = board_info
        board_tiles = []
        for tile_group in curr_board:
            board_tiles.extend(tile_group.tiles)

        if not self.escaped_init:
            bank_tile_groups = self.search_groups(self.bank, [], optimize_for="sum")
            print()
            for tile_group in bank_tile_groups:
                print("Found group:", tile_group)
            print(self.best_value)
            if self.best_value < 30:
                return curr_board
            
            print("Found something more than 30")
            tiles_used = []
            for tile_group in bank_tile_groups:
                tiles_used.extend(tile_group.tiles)
            self.remove_tiles_from_bank(tiles_used)
            self.escaped_init = True
            return curr_board + bank_tile_groups

        return self.search_groups(
            tiles=self.bank + board_tiles,
            required_tiles=board_tiles,
            optimize_for="tiles"
        )
    
    def remove_tiles_from_bank(self, tiles: List[Tile]):
        for tile in tiles:
            self.bank.remove(tile)

    def search_groups(self, tiles: List[Tile], required_tiles: List[Tile], optimize_for="tiles") -> List[List[TileGroup]]:
        """ Given a list of tiles, return a list of possibilities of groups """
        tile_group_map = self.find_groups(tiles)

        all_exiting_groups = set()
        for groups in tile_group_map.values():
            all_exiting_groups = all_exiting_groups | groups
        
        self.best_value = 0
        self.best_tile_groups = []
        self.search_groups_helper(tile_group_map, [], all_exiting_groups, required_tiles, optimize_for)
        return self.best_tile_groups
        
    def search_groups_helper(self, tile_group_map: Dict[Tile, Set[int]], curr_group_list: List[TileGroup], existing_groups: Set[int], required_tiles: List[Tile]=[], optimize_for: str="tiles"):
        # Base case: no tile can be placed in any group
        if len(existing_groups) == 0:
            num_tiles_used = sum(len(group.tiles) for group in curr_group_list)
            all_tiles = set()
            for tile_group in curr_group_list:
                for tile in tile_group.tiles:
                    all_tiles.add(tile)
            
            if all(tile in all_tiles for tile in required_tiles):
                if optimize_for == "tiles":
                    if num_tiles_used > self.best_value:
                        self.best_value = num_tiles_used
                        self.best_tile_groups = deepcopy(curr_group_list)
                else:
                    assert optimize_for == "sum"
                    # TODO: This is a bug: Jokers take the numerical value of the tile they replace.
                    # For now, I'm going to ignore it.
                    # TODO: Probably want to add a heuristic here about what tiles you prefer adding
                    # if you've already hit 30. Currently just want to optimize for the highest sum.
                    tile_sum = sum(tile.number for tile in all_tiles)
                    if self.best_value < tile_sum:
                        self.best_value = tile_sum
                        self.best_tile_groups = deepcopy(curr_group_list)
            return []
        
        # Recursive case: Tiles have groups
        for group in existing_groups:
            remaining_groups = existing_groups - {group}
            
            # For each tile that is in the chosen group, remove all groups that tile is in
            tiles_in_new_group = []
            for tile, group_list in tile_group_map.items():
                if group in group_list:
                    remaining_groups -= group_list
                    tiles_in_new_group.append(tile)
            new_group = TileGroup(tiles_in_new_group)
            assert new_group.is_valid()

            curr_group_list.append(new_group)
            self.search_groups_helper(tile_group_map, curr_group_list, remaining_groups, required_tiles, optimize_for)
            curr_group_list.pop()


    def find_groups(self, tiles: List[Tile]) -> Dict[Tile, Set[int]]:
        """
        Takes a group of tiles and returns a dictionary mapping each tile to a list of groups they could belong to.
        """

        potential_groups = []
        jokers = [tile for tile in tiles if tile.tile_type == TileType.JOKER]
        
        # Search for same number, different color
        numbers = defaultdict(list)
        for tile in tiles:
            if tile.tile_type == TileType.JOKER:
                continue
            numbers[tile.number].append(tile)
        
        for _, number_tiles in numbers.items():
            potential_groups.extend([group for group in combinations(number_tiles + jokers, 3) if len(set(tile.tile_type for tile in group)) == 3])
            potential_groups.extend([group for group in combinations(number_tiles + jokers, 4) if len(set(tile.tile_type for tile in group)) == 4])

        # Search for consecutive numbers, same color.
        colors = defaultdict(list)
        for tile in tiles:
            if tile.tile_type == TileType.JOKER:
                continue
            colors[enum_to_color[tile.tile_type]].append(tile)
        
        for _, color_tiles in colors.items():
            number_occs = defaultdict(list)
            for color_tile in color_tiles:
                number_occs[color_tile.number].append(color_tile)
            
            # Can iterate over all possible sequence lengths
            for seq_len in range(3, 14):
                for start_num in range(1, 14 - seq_len):
                    # Determine if the sequence is possible
                    num_missing = sum(
                        number not in number_occs for number in
                        range(start_num, start_num + seq_len)
                    )

                    if num_missing > len(jokers):
                        continue
                    
                    # Get what we need
                    all_tiles = []
                    for number in range(start_num, start_num + seq_len):
                        if number in number_occs:
                            all_tiles.append(number_occs[number])
                    
                    if num_missing == 1:
                        # If there is only one missing, you can choose between jokers if you have multiple.
                        all_tiles.append(jokers)
                    elif num_missing == 2:
                        # If there are two missing, you need to use both jokers.
                        all_tiles.append([jokers[0]])
                        all_tiles.append([jokers[1]])

                    potential_groups.extend(self.calculate_tile_combinations(all_tiles))

                    # Calculate with extra jokers
                    if len(jokers) - num_missing == 1 and seq_len < 13:
                        all_tiles.append([jokers[-1]])
                        potential_groups.extend(self.calculate_tile_combinations(all_tiles))
                    elif len(jokers) - num_missing == 2 and seq_len < 12:
                        potential_groups.extend(self.calculate_tile_combinations(all_tiles + [jokers]))
                        potential_groups.extend(self.calculate_tile_combinations(all_tiles + [[jokers[0]]] + [[jokers[1]]]))
        
        tile_group_map = defaultdict(set)
        for group_id, group in enumerate(potential_groups):
            for tile in group:
                tile_group_map[tile].add(group_id)
        
        return tile_group_map
    
    def calculate_tile_combinations(self, tile_choices: List[List[Tile]]) -> List[List[Tile]]:
        ''' Given a list of groups of tiles, get all the possbible combinations choosing one tile from each group'''
        if not tile_choices:
            return [[]]
        
        first_group = tile_choices[0]
        remaining_groups = tile_choices[1:]
        
        combinations = []
        sub_combinations = self.calculate_tile_combinations(remaining_groups)
        
        for tile in first_group:
            for sub_combo in sub_combinations:
                combinations.append([tile] + sub_combo)
                
        return combinations

    
    def is_game_over(self):
        return len(self.bank) == 0
