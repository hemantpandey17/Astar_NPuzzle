#Program to implement A* and IDA* algorithm for 8 and 15 puzzle
import sys
import pandas as p
import numpy as np
import copy
import re
import sys
import math
import timeit

start_time = timeit.default_timer()


                                                                              
class  Node:                                                                                  # Class which defines puzzle board
    def __init__(self, n, board_mat, parent):
        self.nsize = n                                                                        # 3 or 4 (size of puzzle)
        self.board_mat = np.array(board_mat.reshape(-1, n), copy='True')                      # converts into 2D Matrix
        self.empty_spc = np.argwhere(self.board_mat == 0)[0]                                  # finds gap position in the puzzle
        self.g = 0                                                                            #g(n) = cost to reach a node from start
        self.f = 0                                                                            #f(n) = cost to reach a node from start + cost from node to goal                     # creates copy recursively
        self.move = ''                                                                        # to store literals for up, dowwn, right, left
        self.parent = parent                                                                  # to store parent node

    def __eq__(self,other):
        return np.array_equal(self.board_mat, other.board_mat)
 

    def  up(self):                                                                             #function to move board_mat up
        i,j = self.empty_spc
    
        if i == 0:
            return -1

        self.board_mat[i][j], self.board_mat[i - 1][j] = self.board_mat[i - 1][j], self.board_mat[i][j]
        self.empty_spc = np.where(self.board_mat == 0)

    def  down(self):                                                                            #function to move board_mat down
        i,j = self.empty_spc
    
        if i == self.nsize - 1:
            return -1
        
        self.board_mat[i][j], self.board_mat[i + 1][j] = self.board_mat[i + 1][j], self.board_mat[i][j]
        self.empty_spc = np.where(self.board_mat == 0)

    def  left(self):                                                                            #function to move board_mat left
        i,j = self.empty_spc
    
        if j == 0:
            return -1

        self.board_mat[i][j], self.board_mat[i][j - 1] = self.board_mat[i][j - 1], self.board_mat[i][j]
        self.empty_spc = np.where(self.board_mat == 0)

    def  right(self):                                                                           #function to move board_mat right
        i,j = self.empty_spc
    
        if j == self.nsize - 1:
            return -1
        
        self.board_mat[i][j], self.board_mat[i][j + 1] = self.board_mat[i][j + 1], self.board_mat[i][j]
        self.empty_spc = np.where(self.board_mat == 0)


 
def get_min(frontier):
    temp_min = []                                                                          # minimum cost node
    for stemp in frontier:
        temp_min.append(stemp.f)

    index_of_min = temp_min.index(min(temp_min))

    return frontier[index_of_min]

def  get_next(node):                                                                        # node to track parent 
    path = []
    while (type(node.parent) != str):
        path.insert(0, node.move)
        node = node.parent
    print(path)
    str1=str(path).strip('[]')
    print(str1)
    outp_file = open(sys.argv[4], 'w')
    outp_file.write(str1)
    print("The values have been written to the output file")
    return 

# TODO Make a calcManDiss
def calcManDis(start, goal):                                                                # Manhattan Distance Heuristic (Used)
    man_dist = 0
    for i in range(start.nsize):
        for j in range(start.nsize):
            if(start.board_mat[i][j] != 0):
                actual_posx, actual_posy = np.where(goal.board_mat == start.board_mat[i][j])
                man_dist += abs(i - actual_posx) + abs(j - actual_posy)

            

    return man_dist

def calcMisplacedTiles(start,goal):                                                          # Misplaced Tile Heuristic (Not used)
    num_board_mat=0
    for i in range(start.nsize):
        for j in range(start.nsize):
            if(start.board_mat[i][j] != 0 and start.board_mat[i][j] != goal.board_mat[i][j]):
                     num_board_mat=num_board_mat + 1
             
            
               
    return num_board_mat
 



def siblings(node, goal):                                                                       # what will happen if any move is made
    siblings = []
    moves = ['U','D','L','R']
    dict_node={0:"up", 1:"down", 2:"left", 3:"right"}

    for i in range(4):
        node_temp =  Node(node.nsize, node.board_mat, node)
        functocall = getattr(node_temp, dict_node[i])
        if functocall() != -1:
            node_temp.move = moves[i]
            node_temp.g = node.g + 1
            siblings.append(node_temp)
    return siblings


def A_star(start, goal):
    frontier = []                                                                                # frontier node
    closed = []                                                                                  # closed node
    count=0                                                                                      # number of states which will be traversed
    frontier.append(start)
    start.g = 0
    start.f = start.g + calcManDis(start, goal)
    print(start.f)


    while frontier:
        current = get_min(frontier)
        if current == goal:
            print("Using A* algorithm")
            print(current.board_mat)
            print(count)

            return  get_next(current)
            path = get_next(current)
            print(frontier.length)
        frontier.remove(current)
        closed.append(current)
        
        for sibling in siblings(current, goal):
            sibling.f = sibling.g + calcManDis(sibling, goal)
            if sibling not in frontier and sibling not in closed:
                    frontier.append(sibling)
                    count=count+1
    return 0
 
    

def IDA_star(start,goal):

    start.g = 0

    bound = start.g + calcManDis(start,goal)
    while(1):
        temp = IDA(start,goal,bound)
        if temp==SUCCESS:
            return SUCCESS
        if temp == float("inf"):
            return FAIL
        bound=temp

def IDA(node,goal,bound):
    node.f = node.g + calcManDis(node,goal)
     
    if node.f > bound:
        return node.f

    if node==goal:
        print("Using IDA star")
        print(node.board_mat)
        path = get_next(node)
        return SUCCESS
    minval = float("inf")
    for sibling in siblings(node,goal):
        temp = IDA(sibling,goal,bound)
        if temp == SUCCESS:
            return SUCCESS
        if temp < minval:
            minval = temp

    return temp


SUCCESS = -1
FAIL = -2
path = []      
path1 = []   

def main():
    #taking command line arguments
    alg_id = int(sys.argv[1])                                                                                           
    n = int(sys.argv[2])
    inp = open(sys.argv[3], 'r')
    outp = open(sys.argv[4], 'w')
    # declaring lists to hold input and goal matrices
    ele_list =[]
    goal_list1=[]
    goal_list2=[]
    #assigning the blank position a value 0 to be used in the program
    
    for i in range (int(n)):
        inp_text= inp.read()                                                      # raeding file generated from puzzleenerator.py
        inp_text = re.split('\n|,', inp_text)
        inp_text = inp_text[:-1]
        #print(inp_text)
        if '' in inp_text:                                         
            gappos = inp_text.index('')
            inp_text[gappos]='0' 
        for j in inp_text:
            if j!='':
                ele_list.append(int(j))
    print(ele_list)
    # defining goal states for both the size 3 and 4
    goal_list1 = [1,2,3,4,5,6,7,8,0]
    goal_list2 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0]
        #print(goal_list1)
   



    # initial start board    
    start =  Node(n, np.array(ele_list), '\0')
    
    

    #boardstart =  Board(3, np.array([1,3,0,4,2,5,7,8,6]))
    #boardgoal =  Board(3, np.array([1,2,3,4,5,6,7,8,0]))

    if n==3:
        goal =  Node(n, np.array(goal_list1), '\0')
        print(np.array(goal_list1).reshape(-1,n))
    elif n==4:
        goal=  Node(n, np.array(goal_list2), '\0')
        print(np.array(goal_list2).reshape(-1,n))

    global path

    #A_star(start, goal)
    #IDA_star(start,goal)

    if len(sys.argv) < 4:
        print("Please enter all the four arguments while giving inputs");

    if alg_id==1:
        print("A Star")
        path=A_star(start,goal)
         

    elif alg_id==2:
        print("IDA*")
        sys.setrecursionlimit(1500)
        path=IDA_star(start,goal)

    else:
        print("Press only 1 or 2")


    
   
    inp.close()
    outp.close()

stop_time = timeit.default_timer()
print (stop_time - start_time)

if __name__ == "__main__":
    main()





