from xcover import covers

def solve_with_xcover(grid_w, grid_h, unique_pieces, counts, verbose = False):
    """
    unique_pieces: List of 6 Piece objects (the prototypes)
    counts: List of integers (how many of each piece are needed)
    """
    
    options = []
    primary_ids = []
    
    # Grid cells are secondary (optional/slack allowed)
    secondary_ids = [(x, y) for x in range(grid_w) for y in range(grid_h)]

    # Loop through each unique shape prototype
    for proto_piece, count in zip(unique_pieces, counts):
        
        # Optimization: Calculate the valid geometric spots ONLY ONCE for this shape
        # (This is much faster than recalculating it for every single copy)
        valid_geometries = list(proto_piece.get_valid_placements(grid_w, grid_h))
        
        # Now, create the specific rows for each required copy (A_0, A_1, etc.)
        for i in range(count):
            # Create a unique ID for this specific physical piece
            unique_uid = f"{proto_piece.uid}_{i}"
            primary_ids.append(unique_uid)
            
            # Add all valid positions for this specific ID to the matrix options
            for placement_coords in valid_geometries:
                # The row: [Piece_ID, (x,y), (x,y)...]
                row = [unique_uid] + placement_coords
                options.append(row)

    if verbose:
        print(f"Solver Setup: {len(primary_ids)} pieces to fit.")
        print(f"Matrix Size: {len(options)} rows (possible moves).")

    if not options:
        return None

    # Run Solver
    # We pass the generated unique IDs as 'primary' (must be used exactly once)
    solution_generator = covers(
        options, 
        primary=primary_ids, 
        secondary=secondary_ids
    )
    
    try:
        # Get the first valid result
        result = next(solution_generator)
        if verbose:
            parse_solution(result, options)
        return result
    except StopIteration:
        if verbose:
            print('\nNo solution found.')
        return None

def parse_solution(solution_indices, all_options):
    """
    solution_indices: list of integers (indices of selected rows)
    all_options: the original list of rows passed to xcover
    """
    print("\nSUCCESS! Solution Found:")
    
    final_placements = []
    
    for idx in solution_indices:
        # Retrieve the actual row data using the index
        row_data = all_options[idx] 
        
        piece_id = row_data[0]
        coords = row_data[1:]
        
        print(f"  {piece_id}: {coords}")
        final_placements.append(row_data)
       
