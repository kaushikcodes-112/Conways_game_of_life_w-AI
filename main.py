import pygame
import random

pygame.init()

BLACK = (0,0,0)
GREY = (128,128,128)
YELLOW = (255,255,0)

WIDTH, HEIGHT = 800,800
TILE_SIZE=10
GRID_WIDTH = WIDTH//TILE_SIZE
GRID_HEIGHT = HEIGHT//TILE_SIZE
FPS=60

screen = pygame.display.set_mode((WIDTH,HEIGHT))

clock = pygame.time.Clock()

def gen(num):
    return set([(random.randrange(0,GRID_HEIGHT),random.randrange(0,GRID_WIDTH)) for _ in range (num)])

def draw_grid(positions):
    # fill the positions that i have clicked or the positions given by gen with yellow
    for position in positions:
        col,row = position
        top_left = (col*TILE_SIZE,row*TILE_SIZE)
        #   *top_left is used for unpacking the top_left tuple such that after using it,
        #   it will be read as (col*TILE_SIZE,row*TILE_SIZE,TILE_SIZE,tILE_SIZE) 
        pygame.draw.rect(screen,YELLOW,(*top_left,TILE_SIZE,TILE_SIZE)) 
        

    for row in range(1,GRID_WIDTH):
        pygame.draw.line(screen,BLACK,(0,row*TILE_SIZE),(WIDTH,row*TILE_SIZE)) #horizontal lines
    for col in range(1,GRID_WIDTH):
        pygame.draw.line(screen,BLACK,(col*TILE_SIZE,0),(col*TILE_SIZE,HEIGHT)) #vertical lines

def adjust_grid(positions):
    # main logic that adjusts the grid
    # logic for which cell will remain alive and which cell will die
    all_neighbours=set()
    # a snapshot of all the initial positions is taken and then the logic is applied
    # After logic is applied, a new set of positions is created which is then drawn
    new_positions=set()
    for position in positions:
        # get all the neighbors of a position
        neighbours =get_neighbors(position)
        # dumps all the neighbour position in all_neighbours
        all_neighbours.update(neighbours)
        # check which neighbours are alive and which are not and adds the alive neighbours to new_position
        neighbours = list(filter(lambda x: x in positions, neighbours))
        if len(neighbours) in [2,3]:
            new_positions.add(position)
    for position in all_neighbours:
        # we go through all_neighbours which are a neighbour to some alive cells.
        # we then check the neighbour's neighbours and dump them in the variable "neighbhours"
        neighbours = get_neighbors(position)
        # then we filter the neighbours and find which ones are alive
        neighbours = list(filter(lambda x: x in positions, neighbours))
        # if there are exactly three alive neighbours then congrats, a new cell is born
        if len(neighbours) in [3,6]:
            new_positions.add(position)
    return new_positions

def get_neighbors(pos):
    x,y=pos
    neighbours=[]
    for dx in [-1,0,1]:
        if x+dx<0 or x+dx>=GRID_WIDTH:
            continue
        for dy in [-1,0,1]:
            if dx ==0 and dy==0:
                continue
            if y+dy<0 or y+dy>=GRID_HEIGHT:
                continue
            
            neighbours.append((x+dx,y+dy))
    return neighbours

def main():
    running=True
    playing =False
    count=0
    update_freq=10
    
    positions = set()

    while running:
        clock.tick(FPS) 
        #regulates the speed of the while loop. Only runs 60 times per second
        if playing:
            count+=1
        if count>=update_freq:
            count=0
            positions=adjust_grid(positions)

        pygame.display.set_caption("Playing" if playing else "Paused")

        
        #stopping the game using pygame.event.get()
        #what does pygame.event.get() do? 
        #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type==pygame.MOUSEBUTTONDOWN:
                x,y=pygame.mouse.get_pos()
                col=x//TILE_SIZE
                row=y//TILE_SIZE
                pos = (col,row)
                if pos in positions:
                    positions.remove(pos)
                else:
                    positions.add(pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = not playing
                if event.key == pygame.K_c:
                    positions=set()
                    playing = False
                if event.key==pygame.K_g:
                    positions=gen(random.randrange(8,12)*GRID_WIDTH)

        screen.fill(GREY)
        draw_grid(positions=positions)
        pygame.display.update()

    pygame.quit()

if __name__=="__main__":
    main()
