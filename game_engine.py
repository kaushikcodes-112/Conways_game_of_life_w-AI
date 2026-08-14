from collections import defaultdict

#neighbour mapping
def get_neighbours(pos,gridw,gridh):
    x,y=pos
    neighbours =[]
    for dx in (-1,0,1):
        for dy in (-1,0,1):
            if dx==0 and dy==0:
                continue
            nx=x+dx
            ny=y+dy
            if 0<=nx<gridw and 0<=ny<gridh:
                neighbours.append((nx,ny))
    return neighbours

def get_neighbour_counts(positions, gridw, gridh):
    # neighbour and its count are stored here to prevent overlap
    # 
    neighbour_count = defaultdict(int)
    for x,y in positions:
        for dx in (-1,0,1):
            for dy in (-1,0,1):
                if dx==0 and dy==0:
                    continue
                nx,ny=x+dx,y+dy
                if 0<=nx<gridw and 0<=ny<gridh:
                    neighbour_count[(nx,ny)]+=1
    return neighbour_count


class UniversalMicroAgent:
    def __init__(self, toggle_budget=3):
        self.toggle_budget=toggle_budget


    def get_interventions(self, positions,birth_rules, survival_rules, gridw, gridh):
        neighbour_counts = get_neighbour_counts(positions,gridw,gridh)
        toggles =set()
        # saving dying cells 1st
        for pos in positions:
            count = neighbour_counts[pos]
            if count not in survival_rules:
                if count<min(survival_rules):
                    x,y=pos
                    for dx in (-1,0,1):
                        for dy in (-1,0,1):
                            n_pos=(x+dx,y+dy)
                            if n_pos not in positions and 0<=n_pos[0]<gridw and 0<=n_pos[1]<gridh:
                                if n_pos not in toggles:
                                    toggles.add(n_pos)
                                    if len(toggles)>=self.toggle_budget:
                                        return toggles
             #flag the positions which need immediate attention
            elif count>max(survival_rules):
                x,y=pos
                for dx in (-1,0,1):
                    for dy in (-1,0,1):
                        if dx==0 and dy==0:
                            n_pos = (x+dx,y+dy)
                            if n_pos in positions:
                                if n_pos not in toggles:
                                    toggles.add(n_pos)
                                    if len(toggles)>= self.toggle_budget:
                                        return toggles
                      
        # birthing dead cells
        for pos,count in neighbour_counts.items(): # for pos and count in the map containing positions mapped to which cell it is common to
            if pos not in positions and (count+1) in birth_rules: # if the pos is a dead cell and if one cell toggle can revive it then DO IT
                toggles.add(pos)
                if len(toggles)>=self.toggle_budget: # if budget exceeded then return
                    return toggles
        return toggles


def advance_physics(positions,neighbour_counts,birth_rules,survival_rules):
    # whatever changes that is made by the micro intervener, is done here
    # Infact any kind of changes made to the board is made by calling this function
    new_positions =set()
    for pos,count in neighbour_counts.items():
        if pos in positions and count in survival_rules:
            new_positions.add(pos)
        elif pos not in positions and count in birth_rules:
            new_positions.add(pos)
    return new_positions
    
def step_simulation(positions,birth_rules,survival_rules, gridw,gridh,agent=None):
    if agent:
        interventions = agent.get_interventions(positions,birth_rules,survival_rules,gridw,gridh)
        for pos in interventions:
            if pos in positions:
                positions.remove(pos)
            else:
                positions.add(pos)

    neighbour_counts= get_neighbour_counts(positions,gridw=gridw, gridh=gridh)
    return advance_physics(positions,neighbour_counts,birth_rules,survival_rules)