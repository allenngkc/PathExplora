import pygame, os, sys
from pygame import Color
from overlay import Block
from settings import *
from pathfinding_algo import PathfindingAlgorithms
import time

# Obtain file system directories
current_dir = os.path.dirname(__file__)
assets_dir = os.path.join(current_dir, "..\\..\\assets")

class GridSystem:
    def __init__(self, rows, cols):
        self.grids = []
        self.img = pygame.image.load(os.path.join(assets_dir, 'ui\\grasstile.png')).convert_alpha()
        self.mouse_down = False

        # Selection of blocks for capturign user input
        self.blocks = [Block(143, 538), Block(190, 538)]

        self.grass_img = pygame.image.load(os.path.join(assets_dir, 'ui\\grasstile.png')).convert_alpha()
        self.wall_img = pygame.image.load(os.path.join(assets_dir, 'pathfinder\\Graphics\\bush.png')).convert_alpha()
        self.start_img = pygame.image.load(os.path.join(assets_dir, 'ui\\soiltile.png')).convert_alpha()
        self.end_img = pygame.image.load(os.path.join(assets_dir, 'ui\\stonetile.png')).convert_alpha()

        # Buttons for resetting the level or path only
        self.resetall_img = pygame.image.load(os.path.join(assets_dir, 'ui\\resetall.png')).convert_alpha()
        self.resetpath_img = pygame.image.load(os.path.join(assets_dir, 'ui\\resetpath.png')).convert_alpha()

        # Choosing the grid to start or end
        self.start_end = [Block(340, 538), Block(405, 538)]

        # Handles and modify path data 
        self.cur_selected = 0 # 0 = grass, 1 = wall, 2 = start, 3 = end

        # Saving previous block positions for start and end, could replace list tuple for better practice
        self.prev_start = []
        self.prev_end = []

        self.cur_start = []
        self.cur_end = []
        
        # Store path data for backend
        self.path_data = []
        for i in range(16):
            row = [0] * 16
            self.path_data.append(row)

        # Add surface grids
        for r in range(rows):
            inner_arr = []
            for c in range(cols):
                inner_arr.append(GridCell(GRID_INIT_X + c*GRID_SIZE,GRID_INIT_Y + r*GRID_SIZE, self.img))
            self.grids.append(inner_arr)    

        # Path finding mechanisms

        self.pathalgo_selection = [Block(610, 538), Block(735, 538)]

        self.algo_index = 0
        self.algo_list = ["DFS", "BFS", "Dijkstra", "A*"]

        self.cur_algo = "DFS"
        self.algo_font = pygame.font.Font(os.path.join(assets_dir, 'world\\m6x11.ttf'), 32)
        self.algo_text_surface = self.algo_font.render(self.cur_algo, True, (0,0,0))
        self.display_surface = pygame.display.get_surface()

        self.pathfinding_algo = PathfindingAlgorithms(self.path_data)

        self.last = pygame.time.get_ticks()
        self.cooldown = 50

        # Dynamic array, constantly being updated
        self.available_path = []

        # Second laying shortest path mechanism
        self.second_laying = False
        self.reflex_path = [] # Dynamic array

    # This needs a independent function due to rendering order issues
    def draw_algo_text(self):
        self.display_surface.blit(self.algo_text_surface, (666,542))

    # Bad naming convention, treatingw this as an update function
    def display_grids(self):
        for i in self.grids:
            for j in i:
                j.draw()

        # Drawing the cursor triggers
        for block in self.blocks:
            block.draw()

        for de in self.start_end:
            de.draw()

        for de in self.pathalgo_selection:
            de.draw()
        
        # Constantly updating self.path_data to PathFindingAlgorithms class
        self.pathfinding_algo.update_path_data(self.path_data)

    """
    This function solves the problem of pygame.time.delay or time.wait not working as intended, The function
    Should be reflecting the visual of the pathfinding algorithm search the path tile by tile. If time.delay
    Or time.wait is used. The whole event loop for display_grids() and run function in pathfinder.py will halt
    Untill the delay is done, which destroys the event loop. Thus the application will become unresponsive and
    The tiles will show all at once by passing self.available_path from self.display_path(). This workaround is
    Able to visualize the tiles with a desired cooldown by checking the current tick and comparing it to last
    Operation.

    @reflex_path is for better visuals. For second layering the path visualization   
    """
    def check_visual_path(self):
        if self.available_path == []:
            if self.second_laying:
                while self.reflex_path:
                    now = pygame.time.get_ticks()
                    if now - self.last >= 35: # Should add CONSTANT here
                        self.last = now
                        node = self.reflex_path.pop()
                        self.display_tile(node, self.end_img)
                    else:
                        break
                if len(self.reflex_path) == 0:
                    self.second_laying = False
            else:
                return
        else:
            while self.available_path:
                now = pygame.time.get_ticks()
                if now - self.last >= self.cooldown:
                    self.last = now

                    node = self.available_path.pop()
                    self.display_tile(node, self.start_img)

                    if len(self.available_path) == 0:
                        self.reflex_path = self.pathfinding_algo.shortest_path(self.cur_start, self.cur_end)
                        self.reflex_path.reverse()
                        self.second_laying = True

                else:
                    break
                

    # Converts the path_data to front end and displays visuals to user
    def display_path(self, path):
        path.reverse()
        self.available_path = path

        # tot_path = len(path)-1
        # cur_index = 0

        # newSur = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
        # newSur.blit(self.start_img, (0,0))
        # newSur.fill(Color(0,0,0,0))

        # for node in path:
        #     r = node[0]
        #     c = node[1]

        #     self.path_data[r][c] = 4
        #     print("Bliting")
            
        #     self.display_surface.blit(newSur, (GRID_INIT_X + c*GRID_SIZE, GRID_INIT_Y + r*GRID_SIZE))

        #     time.sleep(0.1)
        
        # while cur_index <= tot_path:
        #     now = pygame.time.get_ticks()
        #     print(".")
        #     if now - self.last >= self.cooldown:
        #         print("Draw")

        #         cur_tile = path[cur_index]
        #         r = cur_tile[0]
        #         c = cur_tile[1]

        #         self.path_data[r][c] = 4
        #         self.display_surface.blit(newSur, (GRID_INIT_X + c*GRID_SIZE, GRID_INIT_Y + r*GRID_SIZE))

        #         self.last = now
        #         cur_index += 1
            
                
                
    # Update image on desired tile
    def display_tile(self, node, tile):
        r = node[0]
        c = node[1]
        self.path_data[r][c] = 4 # setting tile to 4 indicates it as part of destination
        self.grids[r][c].update_image(tile)
            
            
    
    # Check for user mouse input to obtain specific grid cells
    def check_input(self):
        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print(f"Start: {self.cur_start[0]} {self.cur_start[1]}")
                    print(f"End: {self.cur_end[0]} {self.cur_end[1]}")
                    print(self.pathfinding_algo.dfs(self.cur_start, self.cur_end))
                    for row in self.pathfinding_algo.path_data:
                        for cell in row:
                            print(cell, end=" ")
                        print()
                    print("-----------------------------", end="\n")
                    print(self.cur_algo)

                    # if self.cur_algo == 'BFS':
                    #     self.display_path(self.pathfinding_algo.bfs(self.cur_start, self.cur_end))
                    # elif self.cur_algo == 'DFS':
                    #     self.display_path(self.pathfinding_algo.dfs(self.cur_start, self.cur_end))

                    self.display_path(self.pathfinding_algo.dijkstra(self.cur_start, self.cur_end))

                    # self.display_path(self.pathfinding_algo.bfs(self.cur_start, self.cur_end))
                    
            
            # Check on single left click button down
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.mouse_down = True
                    self.on_collide_cell(mouse_pos)
                    self.on_click_block(mouse_pos)
                    self.on_click_startend(mouse_pos)
                    self.on_switch_algo(mouse_pos)
            # No longer holding on mouse click
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse_down = False

            elif event.type == pygame.MOUSEMOTION and self.mouse_down:
                 self.on_collide_cell(mouse_pos)

    def on_switch_algo(self, mouse_pos):
        if self.pathalgo_selection[0].rect.collidepoint(mouse_pos):
            if self.algo_index < 1:
                self.algo_index = len(self.algo_list)-1
            else:
                self.algo_index -= 1            

        elif self.pathalgo_selection[1].rect.collidepoint(mouse_pos):
            if self.algo_index >= len(self.algo_list)-1:
                self.algo_index = 0
            else:
                self.algo_index += 1

        self.cur_algo = self.algo_list[self.algo_index]
        self.algo_text_surface = self.algo_font.render(self.cur_algo, True, (0,0,0))

    # Upon clicking under block selection ui, switch block placement on grid_system
    def on_click_block(self, mouse_pos):
        # self.blocks[0] represents wall, self.blocks[1] represents grass

        if self.blocks[0].rect.collidepoint(mouse_pos):
            self.cur_selected = 1
        elif self.blocks[1].rect.collidepoint(mouse_pos):
            self.cur_selected = 0

    def on_click_startend(self, mouse_pos):
        if self.start_end[0].rect.collidepoint(mouse_pos):
            self.cur_selected = 2
        elif self.start_end[1].rect.collidepoint(mouse_pos):
            self.cur_selected = 3
        

    # On click cell, calculates the specific grid cell by obtaining the mouse position
    def on_collide_cell(self, mouse_pos):
        for row in self.grids:
            for cell in row:
                if cell.rect.collidepoint(mouse_pos):
                    cell_col = int((cell.x-GRID_INIT_X)/30)
                    cell_row = int((cell.y-GRID_INIT_Y)/30)

                    cur = None
                    if self.cur_selected == 0:
                        cur = self.grass_img

                        self.grids[cell_row][cell_col].update_image(cur)
                    elif self.cur_selected == 1:
                        cur = self.wall_img
                        self.grids[cell_row][cell_col].update_image(cur)

                    elif self.cur_selected == 2 and self.path_data[cell_row][cell_col] == 0 and self.path_data[cell_row][cell_col] != 2: # Start can only be placed on grass
                        cur = self.start_img

                        # Since only 1 starting position exists, if a start block is already been placed, replace it previous one with grass
                        if self.prev_start == []:
                            self.prev_start = [cell_row, cell_col]
                        else:
                            self.grids[self.prev_start[0]][self.prev_start[1]].update_image(self.grass_img)
                            self.path_data[self.prev_start[0]][self.prev_start[1]] = 0
                            self.prev_start = [cell_row, cell_col]

                        self.grids[cell_row][cell_col].update_image(cur)
                        self.cur_start = [cell_row, cell_col]

                    elif self.cur_selected == 3 and self.path_data[cell_row][cell_col] == 0 and self.path_data[cell_row][cell_col] != 3: # End can only be placed on grass
                        cur = self.end_img

                        if self.prev_end == []:
                            self.prev_end = [cell_row, cell_col]
                        else:
                            self.grids[self.prev_end[0]][self.prev_end[1]].update_image(self.grass_img)
                            self.path_data[self.prev_end[0]][self.prev_end[1]] = 0
                            self.prev_end = [cell_row, cell_col]

                        self.grids[cell_row][cell_col].update_image(cur)
                        self.cur_end = [cell_row, cell_col]

                    # Modify path_data for backend
                    self.path_data[cell_row][cell_col] = self.cur_selected

                
class GridCell:
    def __init__(self, x, y, image=None):
        self.x = x
        self.y = y
        self.surface = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
        self.rect = self.surface.get_rect(topleft=(x,y))
        self.display_surface = pygame.display.get_surface()

        # Each grid defaults to be a empty cell
        if image:
            self.image = image
        else:
            self.image = None

    def draw(self):
        if self.image:
            self.surface.blit(self.image, (0,0))
        self.display_surface.blit(self.surface, (self.x, self.y))

    def update_image(self, image):
        self.surface.fill(Color(0,0,0,0))
        self.image = image
        

