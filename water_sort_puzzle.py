current_stack=[]
current_available_moves_stack=[]
current_move_index_stack=[]
bottles=[]
available_solution=[]

red="red"
pink="pink"
green="green"
grey="grey"
blue="blue"
purple="purple"
navy_blue="navy_blue"
sky_blue="sky_blue"
yellow="yellow"
sea_green="sea_green"
pale_green="pale_green"
orange="orange"

def init():
    global bottles
    bottles=[
        [grey,blue,navy_blue,pale_green],
        [navy_blue,grey,pink,green],
        [purple,sky_blue,sea_green,green],
        [orange,blue,pink,sea_green],
        [pink,navy_blue,yellow,sea_green],
        [red,blue,sea_green,orange],
        [pale_green,purple,green,purple],
        [purple,pale_green,green,red],
        [orange,sky_blue,sky_blue,navy_blue],
        [pale_green,pink,blue,red],
        [yellow,sky_blue,orange,grey],
        [yellow,red,grey,yellow],
        [],
        []
    ]

class move:
    def __init__(self,i,j,c):
        self.from_bottle=i
        self.to_bottle=j
        self.color=c

def find_all_available_moves():
    moves=[]
    for i,b in enumerate(bottles):
        if len(b)==0:
            continue
        for j,b2 in enumerate(bottles):
            if i==j:
                continue
            if len(b2)==0 or b2[0]==b[0] and len(b2)<4:
                moves.append(move(i,j,b[0]))
    return moves

def found_solution():
    for b in bottles:
        if len(b)==0:
            continue
        color=b[0]
        for c in b:
            if c!=color:
                return False
    return True

def recur_find():
    for m in current_available_moves_stack[-1]:
        #选择一个可行move，并处理bottles
        current_stack.append(m)
        bottles[m.to_bottle].insert(m.color)
        del bottles[m.from_bottle][0]
        #检查是否一个可行solution
        if found_solution():
            available_solution.append(current_stack)
            pop_stack()
            continue
        #DFS递归处理下一个可行move
        available_moves=find_all_available_moves()
        current_available_moves_stack.append(available_moves)
        recur_find()

def pop_stack():
    m=current_stack.pop()
    current_available_moves_stack.pop()
    bottles[m.from_bottle].insert(0,m.color)
    bottles[m.to_bottle].pop(0)

def push_stack(move):
    current_stack.append(move)
    current_available_moves_stack.append(find_all_available_moves())
    current_move_index_stack.append(0)
    bottles[move.to_bottle].insert(move.color)
    bottles[move.from_bottle].pop(0)

def main():
    current_stack.append("dummy_head")
    current_available_moves_stack.append(find_all_available_moves())
    current_move_index_stack.append(0)
    while True:
        i=current_move_index_stack[0]
        while i<len(current_available_moves_stack[-1]):
            
        #可行方案处理完毕，退出
        if len(current_stack)==1:
            break

    #recur_find()



main()