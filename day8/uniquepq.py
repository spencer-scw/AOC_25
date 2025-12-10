import heapq

class TopKPruningQueue:
    def __init__(self, k=10):
        self.k = k + 1
        self._heap = []  # Max-Heap (stores negative priorities)
        
        # Caching the threshold
        # Starts at infinity (accepts everything until we have k items)
        self.threshold = float('inf') 

        # Uniqueness tracking
        self._seen_priorities = set()
        self._seen_connections = set()

    def push(self, priority, connection):
        """
        Returns True if the item was added (improving the list), False otherwise.
        """
        # 1. FAST FAIL: Pruning Check
        # If the queue is full and this new priority is worse than 
        # our current 10th best, ignore it immediately.
        if len(self._heap) == self.k and priority >= self.threshold:
            return False

        # 2. Uniqueness Check
        # Normalize connection (A, B) == (B, A)
        normalized_conn = tuple(sorted(connection))
        
        if normalized_conn in self._seen_connections:
            return False
        if priority in self._seen_priorities:
            return False

        # 3. Insert / Update Heap
        # We use negative priority to simulate a Max-Heap with Python's heapq
        entry = (-priority, normalized_conn)

        if len(self._heap) < self.k:
            heapq.heappush(self._heap, entry)
            # Track uniqueness
            self._seen_connections.add(normalized_conn)
            self._seen_priorities.add(priority)
        else:
            # Queue is full: Replace the worst (root) with the new better item
            
            # Remove the old "worst" from tracking sets
            old_prio, old_conn = self._heap[0]
            self._seen_priorities.remove(-old_prio) # Remember to flip sign back
            self._seen_connections.remove(old_conn)

            # Add new item to heap
            heapq.heapreplace(self._heap, entry)
            
            # Add new item to tracking sets
            self._seen_connections.add(normalized_conn)
            self._seen_priorities.add(priority)

        # 4. Update Cache
        # If full, the threshold is the priority of the worst item (root)
        # If not full, threshold remains infinity
        if len(self._heap) == self.k:
            self.threshold = -self._heap[0][0]
        
        return True

    def get_items(self):
        """Returns the sorted list of the top k items (smallest to largest)"""
        # We must re-sort because the heap is only partially ordered
        return sorted([(-p, c) for p, c in self._heap])[1:]

