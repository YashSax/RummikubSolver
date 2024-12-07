from typing import List, Tuple, Dict, Set
from utils import Tile, TileGroup, TileType, enum_to_color
from collections import defaultdict
from itertools import combinations
from copy import deepcopy
from tqdm import tqdm
from functools import lru_cache 
import time

class Player:
    def __init__(self, player_id: int, bank: Set[Tile]):
        self.player_id = player_id
        self.bank = bank

        self.turn_time_limit = 180 # seconds

        # The tiles in the first move a player makes must be self-contained
        # and must have a sum greater than or equal to 30.
        self.escaped_init = False
    
    def generate_move(self, board_info: Tuple[int, List[TileGroup]]) -> List[TileGroup]:
        round_num, curr_board = board_info
        board_tiles = set()
        for tile_group in curr_board:
            for tile in tile_group.tiles:
                board_tiles.add(tile)

        if not self.escaped_init:
            bank_tile_groups = self.search_groups(self.bank, [], optimize_for="sum")
            if self.best_value < 30:
                return curr_board
            
            tiles_used = []
            for tile_group in bank_tile_groups:
                tiles_used.extend(tile_group.tiles)
            self.remove_tiles_from_bank(tiles_used)
            self.escaped_init = True
            return curr_board + bank_tile_groups

        new_board = self.search_groups(
            tiles=self.bank | board_tiles,
            required_tiles=board_tiles,
            optimize_for="tiles"
        )

        if new_board is None:
            return curr_board

        for tile_group in new_board:
            for tile in tile_group.tiles:
                if tile in self.bank:
                    print("Used tile:", tile)
                    self.bank.remove(tile)

        return new_board
    
    def remove_tiles_from_bank(self, tiles: List[Tile]):
        for tile in tiles:
            self.bank.remove(tile)

    def search_groups(self, tiles: Set[Tile], required_tiles: Set[Tile], optimize_for="tiles") -> List[TileGroup]:
        """ Given a list of tiles, return a list of possibilities of groups """
        self.tile_group_map = self.find_groups(tiles)
        self.required_tiles = required_tiles
        print("Number of required tiles:", len(self.required_tiles))

        all_existing_groups = set()
        for groups in self.tile_group_map.values():
            all_existing_groups = all_existing_groups | groups
        
        self.best_value = len(self.required_tiles)
        self.best_groups = []
        self.cache = set()
        self.start_time = time.time()
        self.search_groups_helper(set(), all_existing_groups, optimize_for, True)

        if self.best_value == len(self.required_tiles):
            return None
        
        best_tile_groups = []
        for group_num in self.best_groups:
            tiles_in_group = []
            for tile, potential_groups in self.tile_group_map.items():
                if group_num in potential_groups:
                    tiles_in_group.append(tile)
            best_tile_groups.append(TileGroup(tiles_in_group))

        return best_tile_groups
    
    def search_groups_helper(self, used_groups: Set[int], existing_groups: Set[int], optimize_for: str="tiles", show_progress=False):
        if time.time() - self.start_time > self.turn_time_limit:
            return
        
        # Optimization: cache used_groups to know if you've already been here.
        used_tiles = []
        for group in used_groups:
            for tile, potential_groups in self.tile_group_map.items():
                if group in potential_groups:
                    used_tiles.append(tile)
        used_tiles.sort(key=lambda tile: 2**tile.tile_type.value * 3**tile.tile_id * 5**(tile.number + 2))

        cache_key = tuple(used_tiles)
        if cache_key in self.cache:
            return
        self.cache.add(cache_key)

        # Optimization: For each required tile, there must be one group it can be in that's either already been chosen or can potentially be chosen.
        for tile in self.required_tiles:
            tile_has_group = False
            for potential_group in self.tile_group_map[tile]:
                if potential_group in existing_groups or potential_group in used_groups:
                    tile_has_group = True
                    break
            if not tile_has_group:
                return

        # Optimization: If getting all the tiles in the remaining groups is not enough to beat the current best, leave early.
        all_groups = used_groups | existing_groups
        max_number_of_tiles = 0
        for tile, potential_groups in self.tile_group_map.items():
            for group in potential_groups:
                if group in all_groups:
                    max_number_of_tiles += 1
                    break
        if max_number_of_tiles <= self.best_value:
            return

        # Base case: no tile can be placed in any group
        if len(existing_groups) == 0:
            num_tiles_used = len(used_tiles)
            if all(tile in used_tiles for tile in self.required_tiles):
                if optimize_for == "tiles":
                    if num_tiles_used > self.best_value:
                        self.best_value = num_tiles_used
                        print("Updated best value to", self.best_value)
                        self.best_groups = deepcopy(used_groups)
                else:
                    assert optimize_for == "sum"
                    # TODO: This is a bug: Jokers take the numerical value of the tile they replace.
                    # For now, I'm going to ignore it.
                    # TODO: Probably want to add a heuristic here about what tiles you prefer adding
                    # if you've already hit 30. Currently just want to optimize for the highest sum.
                    tile_sum = sum(tile.number for tile in used_tiles)
                    if self.best_value < tile_sum:
                        self.best_value = tile_sum
                        self.best_groups = deepcopy(used_groups)
            return []
        
        # Recursive case: Tiles have groups
        group_iterable = tqdm(existing_groups) if show_progress else existing_groups
        for group in group_iterable:
            remaining_groups = existing_groups - {group}

            for tile, potential_groups in self.tile_group_map.items():
                if group not in potential_groups:
                    continue
                remaining_groups -= potential_groups
            
            used_groups.add(group)
            self.search_groups_helper(used_groups, remaining_groups, optimize_for)
            used_groups.remove(group)


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
