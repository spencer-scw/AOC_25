import math

# Global cache
solution_cache = {}

def get_suffix_sums(pieces, counts):
    """
    Pre-calculates the maximum possible area available from index i to the end.
    """
    areas = [p.area for p in pieces]
    n = len(pieces)
    suffix_sums = [0] * (n + 1)
    
    current_total = 0
    for i in range(n - 1, -1, -1):
        current_total += areas[i] * counts[i]
        suffix_sums[i] = current_total
        
    return areas, suffix_sums

def generate_valid_partitions(pieces, counts, min_area, max_area, limit=500):
    """
    Yields mathematical partitions.
    Includes a 'limit' to prevent getting stuck in one cut forever.
    """
    n_types = len(pieces)
    areas, suffix_max_area = get_suffix_sums(pieces, counts)
    
    # Counter to stop us from trying 1 million math combinations for a single bad geometric cut
    yield_count = 0 

    def search(idx, current_counts_A, current_area):
        nonlocal yield_count
        if yield_count >= limit:
            return

        # 1. Lookahead Pruning (The "Can we make it?" check)
        if current_area + suffix_max_area[idx] < min_area:
            return
        
        # 2. Overshoot Pruning (The "Did we go too far?" check)
        if current_area > max_area:
            return

        # 3. Base Case
        if idx == n_types:
            # We already checked bounds, so this is valid
            counts_B = tuple(total - a for total, a in zip(counts, current_counts_A))
            yield (tuple(current_counts_A), counts_B)
            yield_count += 1
            return

        # 4. Recursive Step
        available = counts[idx]
        unit_area = areas[idx]
        
        # HEURISTIC: Proportional Split
        # If we need to fill X% of the area, try taking X% of this piece type first.
        # This finds the "most likely" fit first.
        
        # Estimate target ratio (0.0 to 1.0) of how full the bin is
        if max_area > 0:
            ratio = (min_area + max_area) / 2 / suffix_max_area[0] # approx target ratio
            start_guess = int(available * ratio)
        else:
            start_guess = available // 2

        # Create a search order that spirals out from the guess
        # e.g. if available=5, guess=3 -> [3, 4, 2, 5, 1, 0]
        search_order = [start_guess]
        radius = 1
        while True:
            added = False
            up = start_guess + radius
            down = start_guess - radius
            if up <= available:
                search_order.append(up)
                added = True
            if down >= 0:
                search_order.append(down)
                added = True
            if not added:
                break
            radius += 1
            
        for take in search_order:
            # Recurse
            current_counts_A.append(take)
            yield from search(idx + 1, current_counts_A, current_area + (take * unit_area))
            current_counts_A.pop()
            
            if yield_count >= limit:
                return

    yield from search(0, [], 0)

def solve_recursively(width, height, pieces, counts):
    # Sort pieces by Area (Largest first) to fail fast in the generator
    # Note: If you do this, ensure 'pieces' and 'counts' are sorted together BEFORE calling this function!
    # For now, we assume they are passed in correct order or consistent order.
    
    state_key = (width, height, tuple(counts))
    if state_key in solution_cache:
        return solution_cache[state_key]

    grid_area = width * height
    total_piece_area = sum(p.area * c for p, c in zip(pieces, counts))
    total_slack = grid_area - total_piece_area
    
    # 1. Geometry Prune: Check if the split is physically too wide/tall (every piece is 3x3)
    if sum(counts) >= 1 and min(width, height) < 3:
        solution_cache[state_key] = False
        return False

    # --- 2. Base Case (DLX) ---
    total_piece_count = sum(counts)
    if total_piece_count <= 1 or (grid_area <= 64 and total_piece_count <= 6):
        from dsx import solve_with_xcover_counts 
        result = solve_with_xcover_counts(width, height, pieces, counts)
        solution_cache[state_key] = result
        return result

    # --- 3. Recursive Cut Strategy ---
    if width >= height:
        split_dim = width
        axis = 'vertical'
    else:
        split_dim = height
        axis = 'horizontal'

    # Optimization: Only try Center Cut
    cut_pos = split_dim // 2
    
    if axis == 'vertical':
        w1, h1 = cut_pos, height
        w2, h2 = width - cut_pos, height
    else:
        w1, h1 = width, cut_pos
        w2, h2 = width, height - cut_pos
        
    area1 = w1 * h1
    
    # --- CRITICAL FIX: Proportional Slack ---
    # Don't let Subgrid 1 take all the slack.
    # Allow it to take its "Fair Share" + a small buffer (e.g. 20% extra).
    
    area_ratio = area1 / grid_area
    fair_share_slack = total_slack * area_ratio
    
    # Buffer: Allow slightly more or less slack than perfect average
    slack_buffer = max(2, total_slack * 0.15) 
    
    max_allowed_slack = int(fair_share_slack + slack_buffer)
    
    # Calculate Bounds
    # It must be at least this full:
    min_p_area = max(0, area1 - max_allowed_slack)
    # It cannot be more than completely full:
    max_p_area = area1 

    # Generate Partitions with Limit
    # We limit to 200 tries per cut. If we can't find a solution in the 
    # "best" 200 mathematical splits, this cut is probably bad geometrically.
    for counts_1, counts_2 in generate_valid_partitions(pieces, counts, min_p_area, max_p_area, limit=200):
        
        # Recurse Left
        if solve_recursively(w1, h1, pieces, counts_1):
            # Recurse Right
            if solve_recursively(w2, h2, pieces, counts_2):
                solution_cache[state_key] = True
                return True

    solution_cache[state_key] = False
    return False
