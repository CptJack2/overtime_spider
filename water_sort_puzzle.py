import copy

current_stack=[]
current_available_moves_stack=[]
bottles=[]
bottles_copy=[]
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
    global bottles_copy
    # bottles=[
    #     [green,blue,blue,blue],
    #     [blue,green,green,green],
    #     []
    # ]
    bottles=[
        [yellow,yellow,yellow,],
        [yellow],
        []
    ]
    # bottles=[
    #     [grey,blue,navy_blue,pale_green],
    #     [navy_blue,grey,pink,green],
    #     [purple,sky_blue,sea_green,green],
    #     [orange,blue,pink,sea_green],
    #     [pink,navy_blue,yellow,sea_green],
    #     [red,blue,sea_green,orange],
    #     [pale_green,purple,green,purple],
    #     [purple,pale_green,green,red],
    #     [orange,sky_blue,sky_blue,navy_blue],
    #     [pale_green,pink,blue,red],
    #     [yellow,sky_blue,orange,grey],
    #     [yellow,red,grey,yellow],
    #     [],
    #     []
    # ]
    bottles_copy=copy.deepcopy(bottles)

class move:
    def __init__(self,i,j,c,n=1):
        self.from_bottle=i
        self.to_bottle=j
        self.color=c
        self.num=n

# def no
#
# rule_filters=[
#
# ]

def find_all_available_moves():
    moves=[]
    for i,b in enumerate(bottles):
        if len(b)==0:
            continue
        for j,b2 in enumerate(bottles):
            if i==j:
                continue
            #两个瓶子最顶上的颜色相同,或者b2是空瓶,就可以倒过去.
            if len(b2)==0 or b2[0]==b[0] and len(b2)<4:
                #b瓶里相同颜色的需要一次倒过去
                n=0
                for c in b:
                    if c==b[0]:
                        n+=1
                    else:
                        break
                #需要b2有足够的空间一次装满才能倒过去,避免两瓶反复倒
                if n<=4-len(b2):
                    moves.append(move(i,j,b[0],n))
    return moves

def found_solution(arg_bottles):
    for b in arg_bottles:
        if len(b)==0:
            continue
        if len(b)!=4:
            return False
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
        if found_solution(bottles):
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
    for i in range(m.num):
        bottles[m.from_bottle].insert(0,m.color)
        bottles[m.to_bottle].pop(0)

def push_stack(move):
    current_stack.append(move)
    for i in range(move.num):
        bottles[move.to_bottle].insert(0,move.color)
        bottles[move.from_bottle].pop(0)
    current_available_moves_stack.append(find_all_available_moves())

def verify_solution():
    for sin,s in enumerate(available_solution):
        bs=copy.deepcopy(bottles_copy)
        for move in s:
            for i in range(move.num):
                bs[move.to_bottle].insert(0,move.color)
                bs[move.from_bottle].pop(0)
        if not found_solution(bs):
            print("bad solution")

def main():
    current_stack.append("dummy_head")
    current_available_moves_stack.append(find_all_available_moves())
    while True:
        #如果当前是可行解,存下并推出栈
        if found_solution(bottles):
            available_solution.append(current_stack[1:])
            pop_stack()
            continue
        #从当前最顶的可行队列取第一个move,加入栈
        elif len(current_available_moves_stack[-1])>0:
            m=current_available_moves_stack[-1][0]
            del current_available_moves_stack[-1][0]
            push_stack(m)
        #当前无可用move,只能倒退一步
        elif len(current_stack)>1:
            pop_stack()
        #可行方案处理完毕，退出
        else:
            break
            print("hello")

    verify_solution()
    print("hello")
    #recur_find()


init()
main()