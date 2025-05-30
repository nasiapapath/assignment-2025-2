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
    
