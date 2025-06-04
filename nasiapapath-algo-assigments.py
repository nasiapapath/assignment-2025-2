import sys
import json
import math


class SparseTable:
    
    def __init__(self, nn, mm, k, initial_key):
       
        self.nn = nn
        self.mm = mm
        self.k = k
        self.nn_authentic = 1  

        if k == 1:
             self.mm = int(self.nn[0] * self.mm[0])
        else:
            self.mm = int(self.nn[k-2] * self.mm[k-1])  
        
        self.table = [initial_key] * self.mm
        self.head = 0  
        
        print(f"CREATE with k={k}, n_k={nn}, m_k={mm}, key={initial_key}")
        self._print_table()
    
    def _print_table(self):
        result = []
        for i in range(self.mm):
            if i == self.head:
                result.append(f">{self.table[i]}<")
            else:
                result.append(str(self.table[i]))
        print(f"[{', '.join(result)}]")
    
    def _sorting_table(self):
        sorted_table = []
        for i in range(self.mm):
            position= (self.head + i) % self.mm
            sorted_table.append(self.table[position])
        return sorted_table
    
    def _binary_search_position(self, key):
        
        sorted_table = self._sorting_table()
        left, right = 0, self.mm - 1
        
        while left <= right:
            mid = (left + right) // 2
            if sorted_table[mid] < key:
                left = mid + 1
            else:
                right = mid - 1
        
        return left
        def _search_key_position(self, key):
       
        sorted_table = self._sorting_table()
        for i in range(self.mm):
            if sorted_table[i] == key:
                return True, i
            elif sorted_table[i] > key:
                return False, i
        return False, self.mm
    
    def _count_authentic_keys(self, start_position):
        
        sorted_table = self._sorting_table()
        if start_position >= len(sorted_table):
            return 0
            
        count = 0
        current_value = sorted_table[start_position]
        
        for i in range(start_position, self.mm):
            if sorted_table[i] != current_value:
                break
            count += 1
        
        return count
    
    def _move_to_right(self, relative_position, elements):
        
        if elements == 0:
            return

        elements_to_move = []
        for i in range(elements):
            position= (self.head + relative_position + i) % self.mm
            elements_to_move.append(self.table[position])
        
        for i in range(elements - 1, -1, -1):
            from_position= (self.head + relative_position + i) % self.mm
            to_position= (self.head + relative_position + i + 1) % self.mm
            self.table[to_position] = elements_to_move[i]
        
        if relative_position == 0:
            self.head = (self.head - 1) % self.mm
    
  def _new_table(self, new_nn):
        
        sorted_table = self._sorting_table()
        authentic_keys = list(set(sorted_table))
        authentic_keys.sort()
        authentic_keys = authentic_keys[:new_nn]  
        
        new_k = len(self.nn) - 1
        for i, n_val in enumerate(self.nn):
            if new_nn <= n_val:
                new_k = i + 1
                break
        
        if new_k == 1:
            new_mm = int(self.nn[0] * self.mm[0])
        else:
            new_mm = int(self.nn[new_k - 1] * self.mm[new_k - 1])
        
        self.k = new_k
        self.mm = new_mm
        self.nn_authentic = new_nn
        
        self.table = [0] * self.mm
        self.head = 0
        
        if not authentic_keys:
            return
  
        positions = []
        for i in range(len(authentic_keys)):
            position= int((i * self.mm) // len(authentic_keys))
            positions.append(position)
        
        for i, key in enumerate(authentic_keys):
            self.table[positions[i]] = key
        
        for i in range(len(authentic_keys)):
            start_position = positions[i]
            end_position= positions[(i + 1) % len(authentic_keys)] if i < len(authentic_keys) - 1 else self.mm
            
            for j in range(start_position + 1, end_position):
                if j < self.mm:
                    next_key_idx = (i + 1) % len(authentic_keys)
                    self.table[j] = authentic_keys[next_key_idx] if next_key_idx < len(authentic_keys) else authentic_keys[i]
        
        last_key = authentic_keys[-1]
        for i in range(len(self.table)):
            if self.table[i] == 0:
                self.table[i] = last_key
    
    def insert(self, key):
       
        found, _ = self._search_key_position(key)
        if found:
            self._print_table()
            return
        
 
        if self.nn_authentic >= self.nn[self.k - 1]:
            self._new_table(self.nn_authentic + 1)
            self.insert(key)
            return
        
        insert_position= self._binary_search_position(key)
        
       
        sorted_table = self._sorting_table()
        if insert_position< len(sorted_table):
            value_position= sorted_table[insert_position]
            
            if key < value_position:
               
                prev_value = sorted_table[insert_position- 1] if insert_position> 0 else float('-inf')
                if prev_value < key < value_position:
                    
                    actual_position= (self.head + insert_position) % self.mm
                    self.table[actual_position] = key
                    self.nn_authentic += 1
                    self._print_table()
                    return
        
        con_count = self._count_authentic_keys(insert_position)
        self._move_to_right(insert_position, con_count)
        
        actual_position= (self.head + insert_position) % self.mm
        self.table[actual_position] = key
        self.nn_authentic += 1
        
        self._print_table()
    
    def lookup(self, key):
       
        print(f"LOOKUP {key}")
        
        found, position= self._search_key_position(key)
        
        if found:
            print(f"Key {key} found at position {position}.")
        else:
            print(f"Key {key} not found. It should be at position {position}.")
        
        self._print_table()
    
    def delete(self, key):
       
        print(f"DELETE {key}")
        
        found, position= self._search_key_position(key)
        
        if not found:
            self._print_table()
            return
        
        sorted_table = self._sorting_table()
        next_authentic_value = None
        
        for i in range(position+ 1, self.mm):
            if sorted_table[i] != key:
                next_authentic_value = sorted_table[i]
                break
        
        if next_authentic_value is None:
            next_authentic_value = sorted_table[0] if sorted_table else key
        
        for i in range(self.mm):
            relative_position= (self.head + i) % self.mm
            if self.table[relative_position] == key:
                self.table[relative_position] = next_authentic_value
        
        self.nn_authentic -= 1
        
        if self.k > 1 and self.nn_authentic <= self.nn[self.k - 2]:
            self._new_table(self.nn_authentic)
        
        self._print_table()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python library_sorting.py <test_file.json>")
        sys.exit(1)
    
    test_file = sys.argv[1]
    
    try:
        with open(test_file, 'r') as f:
            data = json.load(f)
        
        nn = data['n']
        mm = data['m']
        k = data['k']
        initial_key = data['x']
        actions = data['actions']
        
        sparse_table = SparseTable(nn,mm, k, initial_key)
        
        for action in actions:
            action_type = action['action']
            key = action['key']
            
            if action_type == 'insert':
                sparse_table.insert(key)
            elif action_type == 'lookup':
                sparse_table.lookup(key)
            elif action_type == 'delete':
                sparse_table.delete(key)
    
    except FileNotFoundError:
        print(f"Error: File {test_file} not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in file {test_file}.")
        sys.exit(1)
    except KeyError as e:
        print(f"Error: Missing key {e} in JSON file.")
        sys.exit(1)
