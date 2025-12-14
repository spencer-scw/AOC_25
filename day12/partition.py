from dsx import solve_with_xcover

def generate_valid_partitions(pieces, counts, min_area, max_area):
    """
    Yields tuples of (counts_A, counts_B) where:
    - counts_A is the subset of pieces for SubGrid A
    - counts_B is the remaining pieces for SubGrid B
    - min_area <= Area(counts_A) <= max_area
    """
    n_types = len(pieces)
    piece_areas = [p.area for p in pieces] # Assuming p.shape_grid is the parsing source

    # Recursive Subset Sum Helper
    def search(idx, current_counts_A, current_area):
        # Optimization: Pruning
        # If we can't possibly reach min_area even taking all remaining pieces:
        potential_remaining = sum(piece_areas[k] * counts[k] for k in range(idx, n_types))
        if current_area + potential_remaining < min_area:
            return

        # Base Case: All piece types considered
        if idx == n_types:
            if min_area <= current_area <= max_area:
                # Construct the complimentary set (counts_B)
                counts_B = [total - a for total, a in zip(counts, current_counts_A)]
                yield (tuple(current_counts_A), tuple(counts_B))
            return

        # Recursive Step: Try taking 0 to N of piece type[idx]
        available = counts[idx]
        unit_area = piece_areas[idx]
        
        # Heuristic: Try taking more pieces first (greedy) to fill space faster?
        # Or fewer? Usually iterating normally 0..N is safest.
        for take in range(available + 1):
            added_area = take * unit_area
            new_area = current_area + added_area
            
            if new_area > max_area:
                break # Prune: Taking more will only exceed max_area
                
            # Recurse
            # Append 'take' to the growing list of counts for A
            current_counts_A.append(take)
            yield from search(idx + 1, current_counts_A, new_area)
            current_counts_A.pop() # Backtrack

    # Start Search
    yield from search(0, [], 0)

# Global memoization cache to avoid re-solving identical sub-rectangles
# Key: (width, height, tuple(counts)) -> Result
solution_cache = {}

def solve_recursively(width, height, pieces, counts):
    state_key = (width, height, tuple(counts))
    if state_key in solution_cache:
        return solution_cache[state_key]

    if sum(counts) >= 1 and min(width, height) <= 3:
        solution_cache[state_key] = False
        return False

    # --- 1. Calculate Areas and Slack ---
    # Be careful to calculate piece area correctly from your objects
    total_piece_area = sum(p.area * count for p, count in zip(pieces, counts))
    grid_area = width * height
    total_slack = grid_area - total_piece_area

    # Sanity Check
    if total_slack < 0:
        solution_cache[state_key] = False
        return False

    # --- 2. Base Case: Switch to DLX ---
    # Thresholds: Area < 60  OR  Pieces < 8 (tune these!)
    total_piece_count = sum(counts)
    if (total_piece_count <= 4 and grid_area <= 40) or total_piece_count <= 1:
        # Call your existing DLX function
        # Note: You need to return True/False or the Solution here.
        result = solve_with_xcover(width, height, pieces, counts, True)
        solution_cache[state_key] = result
        return result

    # --- 3. Recursive Step: Guillotine Cuts ---
    
    # Strategy: Cut along the Longest Axis to keep grids square-ish
    if width >= height:
        split_dim = width
        axis = 'vertical' # Cutting x-axis
    else:
        split_dim = height
        axis = 'horizontal' # Cutting y-axis

    # Try cuts from roughly 40% to 60% of the dimension 
    # (avoid slicing off tiny slivers, it's inefficient)
    start_cut = split_dim // 2 - (split_dim // 6)
    end_cut = split_dim // 2 + (split_dim // 6)
    
    # Ensure range is valid
    start_cut = max(1, start_cut)
    end_cut = min(split_dim - 1, end_cut)

    for cut_pos in range(start_cut, end_cut + 1):
        
        # Define the two new sub-rectangles
        if axis == 'vertical':
            w1, h1 = cut_pos, height
            w2, h2 = width - cut_pos, height
        else:
            w1, h1 = width, cut_pos
            w2, h2 = width, height - cut_pos
            
        area1 = w1 * h1
        
        # Bounds for the partition search
        # Subgrid 1 must hold pieces with Area between:
        # [Area1 - total_slack, Area1]
        min_p_area = area1 - total_slack
        max_p_area = area1
        
        # Avoid impossible ranges (e.g., if slack is huge)
        min_p_area = max(0, min_p_area)

        # Iterate through valid subsets of pieces
        for counts_1, counts_2 in generate_valid_partitions(pieces, counts, min_p_area, max_p_area):
            
            # RECURSE LEFT (or Top)
            sol_1 = solve_recursively(w1, h1, pieces, counts_1)
            
            if sol_1:
                # Optimization: Slack Update?
                # Technically, if sol_1 used LESS slack than budgeted, 
                # we pass that extra flexibility to sol_2. 
                # But our pure boolean check handles this implicitly.
                
                # RECURSE RIGHT (or Bottom)
                sol_2 = solve_recursively(w2, h2, pieces, counts_2)
                
                if sol_2:
                    # Found a valid split!
                    # For visualization, you might want to merge sol_1 and sol_2
                    # But for "Does it fit?", returning True is enough.
                    solution_cache[state_key] = True # You might store the actual merged solution here
                    return True

    # If no cut worked
    solution_cache[state_key] = False
    return False
