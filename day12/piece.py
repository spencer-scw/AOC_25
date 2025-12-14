class Piece:
    def __init__(self, uid, shape_grid):
        self.uid = uid
        self.shape_grid = shape_grid  # Stored for cloning reference
        
        # 1. Parse and Shift
        base_coords = self._parse_grid(shape_grid)

        self.area = len(base_coords)
        
        # 2. Generate Orientations (Rotations/Flips)
        self.orientations = self._generate_unique_orientations(base_coords)

    def _parse_grid(self, shape_grid):
        coords = set()
        for r, row in enumerate(shape_grid):
            for c, char in enumerate(row):
                if char == '#':
                    coords.add((c, r))
        return self._shift_to_zero(coords)

    def _shift_to_zero(self, coords):
        if not coords:
            return frozenset()
        min_x = min(c[0] for c in coords)
        min_y = min(c[1] for c in coords)
        return frozenset((x - min_x, y - min_y) for x, y in coords)

    def _generate_unique_orientations(self, base_coords):
        unique_shapes = set()
        current = base_coords
        for _ in range(4):
            unique_shapes.add(self._shift_to_zero(current))
            flipped = set((-x, y) for x, y in current)
            unique_shapes.add(self._shift_to_zero(flipped))
            current = set((-y, x) for x, y in current)
        return list(unique_shapes)

    def get_valid_placements(self, grid_w, grid_h):
        """Yields list of coordinates [(x1,y1), (x2,y2)...] for every valid position"""
        for orientation in self.orientations:
            max_x = max(c[0] for c in orientation)
            max_y = max(c[1] for c in orientation)
            
            for dy in range(grid_h - max_y):
                for dx in range(grid_w - max_x):
                    yield [(x + dx, y + dy) for x, y in orientation]
