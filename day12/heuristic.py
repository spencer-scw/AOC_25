class HeuristicPacker:
    def __init__(self, width, height, counts):
        self.width = width
        self.height = height
        # Copy counts so we don't mutate the original
        self.counts = list(counts)
        self.grid = [[False] * width for _ in range(height)]

    def can_fit(self):
        """
        Returns True if the simplified rectangles fit.
        Returns False if they don't (which implies nothing; we must still solve it).
        """
        rects_to_pack = self._generate_rect_list()
        
        # Sort rectangles by height (descending). 
        # This is a standard heuristic for bin packing.
        rects_to_pack.sort(key=lambda r: r[1], reverse=True)
        
        for w, h in rects_to_pack:
            if not self._place_rect(w, h):
                return False
        return True

    def _generate_rect_list(self):
        rects = []
        
        # 1. Identify "Macro Blocks" (Sets of 2 of each of the 6 types)
        # We are limited by whichever piece we have the fewest of.
        min_count = min(self.counts)
        num_macro_blocks = min_count // 2
        
        if num_macro_blocks > 0:
            # Add the 6x14 rectangles
            # We try to keep them as 6x14, but the packer will try rotating to 14x6 automatically
            for _ in range(num_macro_blocks):
                rects.append((6, 14))
                
            # Deduct the pieces we just "used"
            consumed = num_macro_blocks * 2
            for i in range(len(self.counts)):
                self.counts[i] -= consumed

        # 2. Convert remaining pieces to 3x3 squares
        # (The user states all pieces fit in 3x3)
        remaining_pieces = sum(self.counts)
        for _ in range(remaining_pieces):
            rects.append((3, 3))
            
        return rects

    def _place_rect(self, w, h):
        """
        Tries to place a rect of size w*h (or h*w) anywhere in the grid.
        Scanning Top-Left to Bottom-Right.
        """
        # Try preferred orientation first, then rotated
        orientations = [(w, h), (h, w)] if w != h else [(w, h)]
        
        for curr_w, curr_h in orientations:
            # Scan grid
            for y in range(self.height - curr_h + 1):
                for x in range(self.width - curr_w + 1):
                    if self._check_region(x, y, curr_w, curr_h):
                        self._mark_region(x, y, curr_w, curr_h)
                        return True
        return False

    def _check_region(self, x, y, w, h):
        for cy in range(y, y + h):
            for cx in range(x, x + w):
                if self.grid[cy][cx]: # Occupied
                    return False
        return True

    def _mark_region(self, x, y, w, h):
        for cy in range(y, y + h):
            for cx in range(x, x + w):
                self.grid[cy][cx] = True
