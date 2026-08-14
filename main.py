import pygame
import random
import game_engine as ge

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

# deprecated: this function is no more required as the adjust grid logic is moved to advanced physics function in game_engine.py
# def adjust_grid(positions):
#     # main logic that adjusts the grid
#     # logic for which cell will remain alive and which cell will die
#     all_neighbours=set()
#     # a snapshot of all the initial positions is taken and then the logic is applied
#     # After logic is applied, a new set of positions is created which is then drawn
#     new_positions=set()


#     #also add game engine here
#     for position in positions:
#         # get all the neighbors of a position
#         neighbours =get_neighbors(position)
#         # dumps all the neighbour position in all_neighbours
#         all_neighbours.update(neighbours)
#         # check which neighbours are alive and which are not and adds the alive neighbours to new_position
#         neighbours = list(filter(lambda x: x in positions, neighbours))
#         if len(neighbours) in [2,3]:
#             new_positions.add(position)
#     for position in all_neighbours:
#         # we go through all_neighbours which are a neighbour to some alive cells.
#         # we then check the neighbour's neighbours and dump them in the variable "neighbhours"
#         neighbours = get_neighbors(position)
#         # then we filter the neighbours and find which ones are alive
#         neighbours = list(filter(lambda x: x in positions, neighbours))
#         # if there are exactly three alive neighbours then congrats, a new cell is born
#         if len(neighbours) == 3:
#             new_positions.add(position)
#     return new_positions

def get_neighbors(pos):
    x,y=pos
    neighbours=[]
    # logic: get all the neighbours of alive cells, cause only they need to stay alive or dead
    for dx in [-1,0,1]:
        if x+dx<0 or x+dx>=GRID_WIDTH:
            continue # boundary conditions: no need to evaluate for those squares which are not in my domain
        for dy in [-1,0,1]:
            if dx ==0 and dy==0:
                continue 
            if y+dy<0 or y+dy>=GRID_HEIGHT:
                continue # boundary conditions
            
            neighbours.append((x+dx,y+dy))
    return neighbours

def get_user_config():
    print("==============================")
    print("=    CONWAY'S GAME OF LIFE   =")
    print("==============================")
    print("\nLeave blank and press enter for default settings (B3/S23)\n")
    # birth_rules
    b= input("Enter Birth Rules (e.g. 3 for B3): ") or "3" #default input is set to 3
    birth_rules=set(int(x) for x in b if x.isdigit()) # generator expression that checks if the input string is digit or not
    # if it is, then add it to the set
    # survival rules
    s = input("Enter Survival Rules (e.g 23 for S23): ") or"23"
    survival_rules = set(int(x) for x in s if x.isdigit())
    # toggle budget
    tb = input("Enter AI's budget (e.g. 7): ") or "7"
    budget = int(tb)
    print("\nStarting simulation...")
    return birth_rules,survival_rules,budget
def main():
    running=True
    playing =False
    ai_enabled=True
    BIRTH_RULES, SURVIVAL_RULES,TOGGLE_BUDGET = get_user_config()

    agent = ge.UniversalMicroAgent(toggle_budget=TOGGLE_BUDGET)
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
                positions=ge.step_simulation(positions=positions,birth_rules=BIRTH_RULES,survival_rules=SURVIVAL_RULES,gridh=GRID_HEIGHT,gridw=GRID_WIDTH,agent=agent if ai_enabled else None)

        ai_status="ON" if ai_enabled else "OFF"
        play_status="Playing" if playing else "Paused"

        pygame.display.set_caption(f"Status: {play_status} | AI intervention: {ai_status}")

        
        #stopping the game using pygame.event.get()
        #what does pygame.event.get() do? 
        # it gets all the events that have happened in the game, like pressing a key or mouse click
        # it gets them out in a queue and drains the queue empty
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
                if event.key == pygame.K_a:
                    ai_enabled = not ai_enabled
                if event.key == pygame.K_c:
                    positions=set()
                    playing = False
                if event.key==pygame.K_g:
                    positions=gen(random.randrange(8,12)*GRID_WIDTH)
                if event.key == pygame.K_UP:
                    update_freq=max(1,update_freq-1)
                if event.key == pygame.K_DOWN:
                    update_freq+=1

        screen.fill(GREY)
        draw_grid(positions=positions)
        pygame.display.update()

    pygame.quit()

if __name__=="__main__":
    main()
