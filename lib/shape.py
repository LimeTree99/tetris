from lib import color


class Shape:
    def __init__(self):
        self.grid = None
        self.direction = 0
    
    def add_to_grid(self, grid):
        self.grid = grid
        self.grid.set_points(self.shapes[self.direction], self.color)
        
    def add_to_display(self, grid):
        self.grid = grid
        self.grid.set_points(self.display, self.color)
        
    def rotate_right(self):
        self.grid.set_points(self.shapes[self.direction], None)
        self.rotate_direction_right()
        self.grid.set_points(self.shapes[self.direction], self.color)
        
    def rotate_left(self):
        self.grid.set_points(self.shapes[self.direction], None)
        self.rotate_direction_left()
        self.grid.set_points(self.shapes[self.direction], self.color)

    def rotate_direction_left(self):
        if self.direction == 0:
            self.direction = len(self.shapes) - 1
        else:
            self.direction -= 1

    def rotate_direction_right(self):
        if self.direction >= len(self.shapes) - 1:
            self.direction = 0
        else:
            self.direction += 1
        
    def can_rotate_right(self):
        blocks = self.shapes[self.direction]
        self.rotate_direction_right()
        new_blocks = self.shapes[self.direction]
        can_rotate = self.grid.range_is_free(range=new_blocks, ignore=blocks)
        self.rotate_direction_left()
        
        return can_rotate
    
    def can_rotate_left(self):
        blocks = self.shapes[self.direction]
        self.rotate_direction_left()
        new_blocks = self.shapes[self.direction]
        can_rotate = self.grid.range_is_free(range=new_blocks, ignore=blocks)
        self.rotate_direction_right()
        
        return can_rotate
            
    def can_advance(self, x:int, y:int) -> bool:
        '''
        check if shape can move in a desired direction
        
        Parameters:
        x (int):    
        y (int):
        
        Returns:
        bool: True if no obsticle in desired location
        '''
        advancable = True
        n=0
        
        while advancable and n < len(self.shapes[self.direction]):
            block = self.shapes[self.direction][n]
            new_block = [block[0]+x, block[1]+y]
            
            if new_block not in self.shapes[self.direction]:
                if not self.grid.is_free(new_block):
                    advancable = False
            
            n += 1
            
        return advancable
             
    
    def advance(self, x:int, y:int):
        # remove current from grid
        self.grid.set_points(self.shapes[self.direction], None)
        # then move
        for direction in self.shapes:
            for block in direction:
                block[0] += x
                block[1] += y
        # re-add to grid in new pos
        self.grid.set_points(self.shapes[self.direction], self.color)
    
    def hard_drop(self):
        """
        drop shape
        
        Returns:
        distace droped
        """
        distance = 0
        while self.can_advance(0, 1):
            self.advance(0, 1)
            distance += 1
        return distance
            

           
class Shape_I(Shape):
    def __init__(self):
        self.shapes = [[[3,0],[4,0],[5,0],[6,0]],
                       [[5,0],[5,1],[5,2],[5,3]],
                       [[3,1],[4,1],[5,1],[6,1]],
                       [[4,0],[4,1],[4,2],[4,3]]
                      ]
        self.display = [[0,0],[1,0],[2,0],[3,0]]
        self.color = color.teal
        super().__init__()
        
class Shape_J(Shape):
    def __init__(self):
        self.shapes = [[[3,0],[3,1],[4,1],[5,1]],
                       [[5,0],[4,0],[4,1],[4,2]],
                       [[3,1],[4,1],[5,1],[5,2]],
                       [[4,0],[4,1],[4,2],[3,2]]
                      ]
        self.display = [[0,0],[0,1],[1,1],[2,1]]
        self.color = color.blue
        super().__init__()
        
class Shape_L(Shape):
    def __init__(self):
        self.shapes = [[[3,1],[4,1],[5,1],[5,0]],
                       [[4,0],[4,1],[4,2],[5,2]],
                       [[3,2],[3,1],[4,1],[5,1]],
                       [[3,0],[4,0],[4,1],[4,2]]
                      ]
        self.display = [[0,1],[1,1],[2,1],[2,0]]
        self.color = color.orange
        super().__init__()
        
class Shape_O(Shape):
    def __init__(self):
        self.shapes = [[[4,0],[4,1],[5,0],[5,1]]
                      ]
        self.display = [[0,0],[0,1],[1,0],[1,1]]
        self.color = color.yellow
        super().__init__()

class Shape_S(Shape):
    def __init__(self):
        self.shapes = [[[4,1],[5,0],[5,1],[6,0]],
                       [[5,0],[5,1],[6,1],[6,2]],
                       [[4,2],[5,1],[5,2],[6,1]],
                       [[4,0],[4,1],[5,1],[5,2]],
                      ]
        self.display = [[0,1],[1,0],[1,1],[2,0]]
        self.color = color.green
        super().__init__()

class Shape_T(Shape):
    def __init__(self):
        self.shapes = [[[4,1],[5,0],[5,1],[6,1]],
                       [[5,0],[5,1],[5,2],[6,1]],
                       [[4,1],[5,1],[5,2],[6,1]],
                       [[4,1],[5,0],[5,1],[5,2]]
                      ]
        self.display = [[0,1],[1,0],[1,1],[2,1]]
        self.color = color.purple
        super().__init__()
 
class Shape_Z(Shape):
    def __init__(self):
        self.shapes = [[[4,0],[5,0],[5,1],[6,1]],
                       [[5,1],[5,2],[6,0],[6,1]],
                       [[4,1],[5,1],[5,2],[6,2]],
                       [[4,1],[4,2],[5,0],[5,1]],
                      ]
        self.display = [[0,0],[1,0],[1,1],[2,1]]
        self.color = color.red
        super().__init__()