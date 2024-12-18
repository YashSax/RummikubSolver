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

        self.turn_time_limit = 1e99 # seconds

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
        self.group_tile_map = defaultdict(set)
        for tile, potential_groups in self.tile_group_map.items():
            for group in potential_groups:
                self.group_tile_map[group].add(tile)

        self.group_overlap = defaultdict(set)
        for potential_groups in self.tile_group_map.values():
            for group in potential_groups:
                self.group_overlap[group] |= potential_groups

        self.required_tiles = required_tiles
        print("Number of required tiles:", len(self.required_tiles))

        all_existing_groups = set()
        for groups in self.tile_group_map.values():
            all_existing_groups = all_existing_groups | groups
        
        self.best_value = len(self.required_tiles)
        self.best_groups = []
        self.cache = set()
        self.remaining_tiles_cache = dict()
        self.start_time = time.time()
        self.info = defaultdict(int)
        self.search_groups_no_recursion(
        # self.search_groups_helper(
            used_tiles=set(),
            used_groups=set(),
            existing_groups=all_existing_groups,
            remaining_required=required_tiles,
            remaining_tiles=tiles,
            optimize_for=optimize_for,
            # show_progress=True
        )
        
        best_tile_groups = []
        for group_num in self.best_groups:
            tiles_in_group = []
            for tile, potential_groups in self.tile_group_map.items():
                if group_num in potential_groups:
                    tiles_in_group.append(tile)
            best_tile_groups.append(TileGroup(tiles_in_group))

        return best_tile_groups
    
    def search_groups_no_recursion(self, used_tiles: Set[Tile], used_groups: Set[int], existing_groups: Set[int], remaining_required: Set[int], remaining_tiles: Set[int], optimize_for: str="tiles"):
        state_stack = [
            (used_tiles, used_groups, existing_groups, remaining_required, remaining_tiles, optimize_for)
        ]

        while len(state_stack) > 0:
            used_tiles, used_groups, existing_groups, remaining_required, remaining_tiles, optimize_for = state_stack.pop()
            if time.time() - self.start_time > self.turn_time_limit:
                return
            
            if self.used_tiles_in_cache(used_tiles):
                continue

            if self.required_tile_has_no_group(remaining_required, existing_groups):
                continue

            if optimize_for == "tiles" and self.remaining_tiles_not_enough(used_tiles, existing_groups):
                continue

            if len(existing_groups) == 0:
                num_tiles_used = len(used_tiles)
                if True: # Original: "all(tile in used_tiles for tile in self.required_tiles)" -> we don't need this since we have optimization #2
                    if optimize_for == "tiles":
                        if num_tiles_used > self.best_value:
                            self.best_value = num_tiles_used
                            print("Updated best value to", self.best_value)
                            self.best_groups = deepcopy(used_groups)

                            # for group in self.best_groups:
                            #     print("[" + ", ".join([str(i) for i in self.group_tile_map[group]]), "]")

                    else:
                        assert optimize_for == "sum"
                        # TODO: This is a bug: Jokers take the numerical value of the tile they replace.
                        # For now, I'm going to ignore it.
                        # TODO: Probably want to add a heuristic here about what tiles you prefer adding
                        # if you've already hit 30. Currently just want to optimize for the highest sum.
                        tile_sum = sum(tile.number for tile in used_tiles)
                        if tile_sum >= self.best_value:
                            self.best_value = tile_sum
                            self.best_groups = deepcopy(used_groups)
                continue

            for group in existing_groups:
                remaining_groups = existing_groups - self.group_overlap[group]
                tiles_added = self.group_tile_map[group]
                
                state_stack.append((
                    used_tiles | tiles_added,
                    used_groups.union({group}),
                    remaining_groups,
                    remaining_required - tiles_added,
                    remaining_tiles - tiles_added,
                    optimize_for
                ))


    def used_tiles_in_cache(self, used_tiles):
        cache_key = tuple(sorted(used_tiles, key=lambda tile: tile.hash_no_tile_id()))
        if cache_key in self.cache:
            self.info["vanilla cache"] += 1
            return True
        self.cache.add(cache_key)
        return False
    
    def remaining_tiles_in_cache(self, used_tiles, used_groups, remaining_tiles):
        remaining_tiles_cache_key = tuple(sorted(remaining_tiles, key=lambda tile: tile.hash_no_tile_id()))
        if remaining_tiles_cache_key in self.remaining_tiles_cache:
            self.info["remaining tiles cache"] += 1

            num_new_tiles, new_groups = self.remaining_tiles_cache[remaining_tiles_cache_key]
            if len(used_tiles) + num_new_tiles > self.best_value:
                print("Updating best value to", len(used_tiles) + num_new_tiles)
                self.best_value = len(used_tiles) + num_new_tiles
                self.best_groups = used_groups | new_groups

                # for group in self.best_groups:
                #     print("[" + ", ".join([str(i) for i in self.group_tile_map[group]]), "]")
            return True
        return False

    def required_tile_has_no_group(self, remaining_required, existing_groups):
        for tile in remaining_required:
            potential_groups = self.tile_group_map[tile]
            if len(potential_groups.intersection(existing_groups)) == 0:
                self.info["required tile no group"] += 1
                return True
        return False
    
    def remaining_tiles_not_enough(self, used_tiles, existing_groups):
        max_number_of_tiles = len(used_tiles)
        for tile, potential_groups in self.tile_group_map.items():
            max_number_of_tiles += len(potential_groups.intersection(existing_groups)) > 0
        if max_number_of_tiles <= self.best_value:
            self.info["best case is still bad"] += 1
            return True
        return False


    def search_groups_helper(self, used_tiles: Set[Tile], used_groups: Set[int], existing_groups: Set[int], remaining_required: Set[int], remaining_tiles: Set[int], optimize_for: str="tiles", show_progress=False):
        if time.time() - self.start_time > self.turn_time_limit:
            return -1e99, set()
        
        # Optimization # 1: cache used_groups to know if you've already been here.
        cache_key = tuple(sorted(used_tiles, key=lambda tile: tile.hash_no_tile_id()))
        if cache_key in self.cache:
            self.info["vanilla cache"] += 1
            return -1e99, set()
        self.cache.add(cache_key)

        # Optimization #2: Cache over the remaining tiles.
        remaining_tiles_cache_key = tuple(sorted(remaining_tiles, key=lambda tile: tile.hash_no_tile_id()))
        if optimize_for == "tiles":
            if remaining_tiles_cache_key in self.remaining_tiles_cache:
                self.info["remaining tiles cache"] += 1

                num_new_tiles, new_groups = self.remaining_tiles_cache[remaining_tiles_cache_key]
                if len(used_tiles) + num_new_tiles > self.best_value:
                    print("Updating best value to", len(used_tiles) + num_new_tiles)
                    self.best_value = len(used_tiles) + num_new_tiles
                    self.best_groups = used_groups | new_groups

                    for group in self.best_groups:
                        print("[" + ", ".join([str(i) for i in self.group_tile_map[group]]), "]")
                return -1e99, set()

        # Optimization #3: For each required tile, there must be one group it can be in that's either already been chosen or can potentially be chosen.
        for tile in remaining_required:
            potential_groups = self.tile_group_map[tile]
            if len(potential_groups.intersection(existing_groups)) == 0:
                self.info["required tile no group"] += 1
                return -1e99, set()

        # Optimization (only when optimizing for tile count) #4: If getting all the tiles in the remaining groups is not enough to beat the current best, leave early.
        if optimize_for == "tiles":
            max_number_of_tiles = len(used_tiles)
            for tile, potential_groups in self.tile_group_map.items():
                max_number_of_tiles += len(potential_groups.intersection(existing_groups)) > 0
            if max_number_of_tiles <= self.best_value:
                self.info["best case is still bad"] += 1
                return -1e99, set()

        # Base case: no tile can be placed in any group
        if len(existing_groups) == 0:
            num_tiles_used = len(used_tiles)
            if True: # Original: "all(tile in used_tiles for tile in self.required_tiles)" -> we don't need this since we have optimization #2
                if optimize_for == "tiles":
                    if num_tiles_used > self.best_value:
                        self.best_value = num_tiles_used
                        print("Updated best value to", self.best_value)
                        self.best_groups = deepcopy(used_groups)

                        for group in self.best_groups:
                            print("[" + ", ".join([str(i) for i in self.group_tile_map[group]]), "]")

                else:
                    assert optimize_for == "sum"
                    # TODO: This is a bug: Jokers take the numerical value of the tile they replace.
                    # For now, I'm going to ignore it.
                    # TODO: Probably want to add a heuristic here about what tiles you prefer adding
                    # if you've already hit 30. Currently just want to optimize for the highest sum.
                    tile_sum = sum(tile.number for tile in used_tiles)
                    if tile_sum >= self.best_value:
                        self.best_value = tile_sum
                        self.best_groups = deepcopy(used_groups)
            return num_tiles_used, deepcopy(used_groups)
        
        # Recursive case: Tiles have groups
        best_num_new_tiles = -1
        best_resulting_groups = set()

        group_iterable = tqdm(existing_groups) if show_progress else existing_groups
        for group in group_iterable:
            remaining_groups = existing_groups - self.group_overlap[group]
            tiles_added = self.group_tile_map[group]
            
            used_tiles |= tiles_added
            used_groups.add(group)
            num_tiles_used, resulting_groups = self.search_groups_helper(
                used_tiles=used_tiles,
                used_groups=used_groups,
                existing_groups=remaining_groups,
                remaining_required=remaining_required - tiles_added,
                remaining_tiles=remaining_tiles - tiles_added,
                optimize_for=optimize_for
            )
            used_tiles -= tiles_added
            used_groups.remove(group)

            num_new_tiles = num_tiles_used - len(used_tiles)
            new_groups = resulting_groups - used_groups
            if num_new_tiles > best_num_new_tiles:
                best_num_new_tiles = num_new_tiles
                best_resulting_groups = new_groups
        
        self.remaining_tiles_cache[remaining_tiles_cache_key] = (best_num_new_tiles, best_resulting_groups)
        return best_num_new_tiles, best_resulting_groups
    

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
                for start_num in range(1, 15 - seq_len):
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


if __name__ == "__main__":
    pass