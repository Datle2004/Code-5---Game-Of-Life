import pygame 
import Main
import Game
pygame.init()
class Advanced():
    def __init__(self,screen):
        self.screen = screen
        self.create = Game.Run(screen, False)
        self.create.cell_size = 6
        self.create.rows = 100
        self.create.cols = 100
        self.start = [1,1]
        self.end = [99,99]
        self.middle = [0,0]
        self.create.grid = [[0]*100 for i in range(100)]
        self.d = [0,0]
        self.m = [0,0]
    def update_direction(self,start,end):
        x1,y1 = start
        x2,y2 = end
        for i in range(0,2):
            if end[i] > start[i]:
                self.d[i] = 1
            else:
                self.d[i] = -1
        self.update_middle_direction()

        middle_point = self.find_middle()
        
        if max(middle_point) >= 99 or min(middle_point) <= 1:
            if abs(x2-x1) > abs(y2-y1):
                self.d[1] = -self.d[1]
            else:
                self.d[0] = -self.d[0] 
            self.update_middle_direction()
        
                    
    def update_middle_direction(self):
        x1,y1 = self.start
        x2,y2 = self.end
        if self.d[0] * (x2 - x1) > self.d[1] * (y2 - y1):
            self.m[0] = self.d[0]
            self.m[1] = -1 * self.d[1]
        elif self.d[0]*(x2 - x1) < self.d[1]*(y2 - y1):
            self.m[0] = -1 * self.d[0]
            self.m[1] = self.d[1]
        else:
            self.m[0] = self.d[0]
            self.m[1] = self.d[1]
    def update_start_grid(self,start,d):
        #direction
        i,j = start 
        self.create.grid[i + d[0]][j + d[1]] = 1
        self.create.grid[i][j + d[1]] = 1
        self.create.grid[i + d[0]][j] = 1
        self.create.grid[i - d[1]][j + d[0]] = 1
        if d[0] * d[1] > 0:
            self.create.grid[i][j - d[1]] = 1
        else:
            self.create.grid[i - d[0]][j] = 1
    def finish(self,d):
        i,j = self.end
        self.create.grid[i + 1][j] = 1
        self.create.grid[i-1][j] = 1
        self.create.grid[i][j + 1] = 1
        self.create.grid[i][j - 1] = 1
        self.create.grid[i + d[0]][j + d[1]] = 1
    def find_middle(self):
        x1,y1 = self.start
        x2,y2 = self.end
        D = -1 * self.d[0] * self.m[1] + self.d[1] * self.m[0]
        Dx = -1 *(self.d[0] * x1 - self.d[1]*y1)*self.m[1] + self.d[1]*(self.m[0]*x2-self.m[1]*y2)
        Dy = self.d[0]*(self.m[0]*x2 - self.m[1]*y2) - self.m[0]*(self.d[0]*x1-self.d[1]*y1)
        return [Dx//D,Dy//D]
        

    def move_pos(self,text,i):
        return self.create.draw_input(text,i)
    
    def main(self):
        pop_sound = pygame.mixer.Sound('pop_sound.mp3')
        pop_sound.set_volume(0.2)
        self.screen.fill((202, 228, 241))
        start_pos = self.move_pos("Start: 1 1",100)
        end_pos = self.move_pos("End: 99 99",200)
        run = True
        pause = False
        start = False
        check = False
        check_middle = False
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.create.button_rect.collidepoint(event.pos): 
                        if start_pos.collidepoint(event.pos):
                            pop_sound.play()
                            self.start = self.create.input_screen("Start: ",700,100,False, True)
                            self.create.COUNT = 0
                        elif end_pos.collidepoint(event.pos):
                            pop_sound.play()
                            self.end = self.create.input_screen("End: ",700,200,False, True)
                            self.create.COUNT = 0
                        elif self.create.reset_button.collidepoint(event.pos):
                            pop_sound.play()
                            self.create.grid = [[0]*100 for i in range(100)]
                            start = False
                            self.create.COUNT = 0
                            self.create.draw_generation(False)
                        elif pygame.Rect((0,0,600,600)).collidepoint(event.pos):
                            pass
                        elif self.create.back_button.collidepoint(event.pos):
                            pop_sound.play()
                            Main.main()
                        else:
                            pass
                    else:
                        pause = not pause
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.update_direction(self.start,self.end)
                        if (sum(self.start) + sum(self.end)) % 2 == 1:
                            self.end[1] -= self.d[1]
                        if self.m != self.d:
                            check_middle = True
                            middle = self.find_middle()

                        self.create.COUNT = 0        
                        self.update_start_grid(self.start,self.d)
                        start = True
                        pause = False

            # Draw the grid and cells
            self.create.draw_grid()
            self.create.draw_cells()
            pygame.draw.rect(self.screen,"yellow",(self.start[1]*self.create.cell_size +2, self.start[0]*self.create.cell_size + 2,self.create.cell_size - 2,self.create.cell_size - 2))
            pygame.draw.rect(self.screen,"red",(self.end[1]*self.create.cell_size +2, self.end[0]*self.create.cell_size + 2,self.create.cell_size - 2,self.create.cell_size - 2))
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
            if check_middle:
                if self.create.COUNT ==  abs(middle[0] - self.start[0]) * 4:
                    self.create.grid = [[0]*100 for i in range(100)]
                    self.update_start_grid(middle,self.m)
                if self.create.COUNT == (abs(middle[0] - self.start[0]) + abs(self.end[0] - middle[0])) * 4:
                    self.create.grid = [[0]*100 for i in range(100)]
                    self.finish(self.m)
            else:
                if self.create.COUNT == abs(self.end[0]-self.start[0])*4:
                    self.create.grid = [[0]*100 for i in range(100)]
                    self.finish(self.d)

            # Update the display
            pygame.display.update()
    

        # Quit Pygame
        pygame.quit()
            
            
