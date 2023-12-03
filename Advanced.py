import pygame 
import Main
import Game
pygame.init()
class Advanced():
    def __init__(self,screen):
        self.screen = screen
        self.create = Game.Run(screen)
        self.create.cell_size = 6
        self.create.rows = 100
        self.create.cols = 100
        self.start = [0,0]
        self.end = [100,100]
        self.create.grid = [[0]*100 for i in range(100)]
        self.d = [0,0]
    def update_start_grid(self,start,end):
        #direction
        i = start[0]
        j = start[1]
        for i in range(0,2):
            if end[i] > start[i]:
                self.d[i] = 1
            elif end[i] < start[i]:
                self.d[i] = -1 
            else:
                if start[i] < 50:
                    self.d[i] = 1
                else:
                    self.d[i] = -1
        self.create.grid[i+self.d[0]][j+self.d[1]] = 1
        self.create.grid[i][j+self.d[1]] = 1
        self.create.grid[i+self.d[0]][j] = 1
        self.create.grid[i-self.d[1]][j+self.d[0]] = 1
        if self.d[0]*self.d[1] > 0:
            self.create.grid[i][j-self.d[1]] = 1
        else:
            self.create.grid[i-self.d[0]][j] = 1
        print(start)
    def move_pos(self,text,i):
        return self.create.draw_input(text,i)
    def main(self):
        self.screen.fill((202, 228, 241))
        start_pos = self.move_pos(f"Start: {self.start}",100)
        end_pos = self.move_pos(f"End: {self.end}",200)
        run = True
        pause = False
        start = False
        check = False
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.create.button_rect.collidepoint(event.pos): 
                        if start_pos.collidepoint(event.pos):
                            self.start = self.create.input_screen("Start: ",700,100,False)
                            self.create.COUNT = 0
                        elif end_pos.collidepoint(event.pos):
                            self.end = self.create.input_screen("End: ",700,200,False)
                            self.create.COUNT = 0
                        elif self.create.reset_button.collidepoint(event.pos):
                            self.create.grid = [[0]*100 for i in range(100)]
                            start = False
                            self.create.COUNT = 0
                            self.create.draw_generation(False)
                        elif pygame.Rect((0,0,600,600)).collidepoint(event.pos):
                            pass
                        elif self.create.back_button.collidepoint(event.pos):
                            Main.main()
                        else:
                            pass
                    else:
                        pause = not pause
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.update_start_grid(self.start,self.end)
                        start = True
                        pause = False

            # Draw the grid and cells
            self.create.draw_grid()
            self.create.draw_cells()
            pygame.draw.rect(self.screen,"yellow",(self.start[0]*self.create.cell_size +2, self.start[1]*self.create.cell_size + 2,self.create.cell_size - 2,self.create.cell_size - 2))
            pygame.draw.rect(self.screen,"red",(self.end[0]*self.create.cell_size +2, self.end[1]*self.create.cell_size + 2,self.create.cell_size - 2,self.create.cell_size - 2))
            #draw button
            self.create.draw_pause_button(pause,start)
            self.create.draw_reset_button()
            self.create.draw_back_button()

            if not pause and start:
                self.create.draw_generation(check)
                self.create.grid = self.create.next_generation(self.create.grid)
            if self.create.grid == self.create.next_generation(self.create.grid):
                check = False
            else:
                check = True

            # Update the display
            pygame.display.update()
    

        # Quit Pygame
        pygame.quit()
            
            