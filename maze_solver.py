#This maze generator will be using the recursive backtrack algorithim.
import turtle
import random

#--------------------FUNCTIONS---------------------------------
#function which helps keep track of how many cells have been visited
def listsum(input):
    my_sum = 0
    for row in input:
        my_sum += sum(row)
    return my_sum

#function which generates the maze in a 3d array initially
def mazegenerate(sizex,sizey):
    #declaring needed variables
    walls=[[[1,1,1,1] for a in range(sizex)] for b in range(sizey)]
    x=0
    y=0
    visitedsum=0
    currentcell=[x,y] 
    visited=[[0 for a in range(sizex)] for b in range(sizey)]
    visited[x][y]=1
    visitn=[[x,y]] #Stack keeps track of coordinates of cells visited
    n=0 #needed later on in the code to backtrack

    #while loop which stops running when all cells have been visited
    while visitedsum!=(sizex*sizey):
        options=[0,0,0,0] #start with no walls can be removed
        if x!=0:
            if visited[y][x-1]==0:
                options[0]=1
                #west wall can be removed
        if y!=sizey-1:
            if visited[y+1][x]==0:
                options[1]=1
                #north wall can be removed
        if x!=sizex-1:
            if visited[y][x+1]==0:
                options[2]=1
                #east wall can be removed
        if y!=0:
            if visited[y-1][x]==0:
                options[3]=1
                #south wall can be removed

        #if no wall can be broken down the program backtracks
        if options==[0,0,0,0]:
            currentcell=visitn[n-1]
            x=currentcell[0]
            y=currentcell[1]
            n=n-1
            
        else:
            cellfound=False
            while cellfound==False:
                randomint=random.randint(0,3)
                if options[randomint]==1:
                    if randomint==0:
                        oppisitecell=[currentcell[0]-1,currentcell[1]]#moves into west cell
                        walls[currentcell[1]][currentcell[0]][0]=0#removes west wall
                        walls[oppisitecell[1]][oppisitecell[0]][2]=0
                    elif randomint==1:
                        oppisitecell=[currentcell[0],currentcell[1]+1]#moves into north cell
                        walls[currentcell[1]][currentcell[0]][1]=0#removes north wall
                        walls[oppisitecell[1]][oppisitecell[0]][3]=0
                    elif randomint==2:
                        oppisitecell=[currentcell[0]+1,currentcell[1]]#moves into east cell
                        walls[currentcell[1]][currentcell[0]][2]=0#removes east wall
                        walls[oppisitecell[1]][oppisitecell[0]][0]=0
                    else:
                        oppisitecell=[currentcell[0],currentcell[1]-1]#moves into south cell
                        walls[currentcell[1]][currentcell[0]][3]=0#removes south wall
                        walls[oppisitecell[1]][oppisitecell[0]][1]=0
                    n=n+1
                    visitn.insert(n,oppisitecell)
                    currentcell=oppisitecell
                    visited[currentcell[1]][currentcell[0]]=1
                    x=currentcell[0]
                    y=currentcell[1]
                    cellfound=True
        visitedsum=listsum(visited)
    return(walls)

#Displaying the maze using turtle
def printmaze(sizex,sizey,walls):
    
    #setting up size of maze
    startx=200
    starty=-startx
    gridsize=(2*(-startx))/sizex

    #setting up how turtle will work
    turtle.color()
    turtle.clear()
    turtle.speed(0)
    
    #drawing the north walls edge and the west wall edge
    turtle.penup()
    turtle.goto(startx,starty)
    turtle.pendown()
    turtle.goto(-startx,starty)
    turtle.goto(-startx,-starty)
    turtle.setheading(0)

    #south wall of each cell
    for y in range(sizex):
        turtle.penup()
        turtle.goto(startx,-starty+gridsize*(y))
        for x in range(sizey):
            if walls[y][x][3]==1:
                turtle.pendown()
            else:
                turtle.penup()
            turtle.forward(gridsize)
    turtle.left(90)
    
    #east wall of each cell
    for x in range(sizex):
        turtle.penup()
        turtle.goto(startx+gridsize*(x),-starty)
        for y in range(sizey):
            if walls[y][x][0]==1:
                turtle.pendown()
            else:
                turtle.penup()
            turtle.forward(gridsize)

#----------------------SOLVER FUNCTIONS------------------------
#The maze solver will be using the dijkstra algorithm to solve the maze and to find the shortest 
def oppcell(b,currentcell):
    if b==0:
        oppcell=[currentcell[0]-1,currentcell[1]]
    elif b==1:
        oppcell=[currentcell[0],currentcell[1]+1]
    elif b==2:
        oppcell=[currentcell[0]+1,currentcell[1]]
    else:
        oppcell=[currentcell[0],currentcell[1]-1]
    return(oppcell)

def search(walls,sizey,sizex):
    visited=[[0 for a in range(sizex)] for b in range(sizey)]
    visited[0][0]=1#starts bottom left with 1
    currentcells=[[0,0]]
    new=True
    while new==True:
        new=False
        #for loop searching all current cells
        for a in range(len(currentcells)):
            currentcell=currentcells[0]
            for b in range(4):#checks all 4 allowed directions
                if walls[currentcell[1]][currentcell[0]][b]==0:#check for wall
                    cellotherside=oppcell(b,currentcell)
                    if visited[cellotherside[1]][cellotherside[0]]==0:#check if hasnt been visited
                        visited[cellotherside[1]][cellotherside[0]]=visited[currentcell[1]][currentcell[0]]+1
                        currentcells.append(cellotherside)#adds the new cell to the list of cells curently at
                        new=True
                        cellpath(cellotherside[0],cellotherside[1],gridsize,-200,-200,sizex,visited[currentcell[1]][currentcell[0]]+1)
            currentcells.remove(currentcell)#removes the previous cell because it has been searched
    return(visited)

#function with the suspected fault
def route(visited,sizex,sizey,walls):
    distance=visited[sizex-1][sizey-1]
    routexy=[[sizex-1,sizey-1]]#sets finish to top right

    #while loops until the programs finds its way back at the start
    while routexy[0]!=[0,0]:
        if walls[routexy[0][1]][routexy[0][0]][0]==0:#backtracks by looking at each square and chosing the correct one to go in so no wall and distance=distance-1
            if visited[routexy[0][1]][routexy[0][0]-1]==distance-1:
                routexy.insert(0,[routexy[0][0]-1,routexy[0][1]])
                distance=distance-1
        if walls[routexy[0][1]][routexy[0][0]][1]==0:
            if visited[routexy[0][1]+1][routexy[0][0]]==distance-1:
                routexy.insert(0,[routexy[0][0],routexy[0][1]+1])
                distance=distance-1
        if walls[routexy[0][1]][routexy[0][0]][2]==0:
            if visited[routexy[0][1]][routexy[0][0]+1]==distance-1:
                routexy.insert(0,[routexy[0][0]+1,routexy[0][1]])
                distance=distance-1
        if walls[routexy[0][1]][routexy[0][0]][3]==0:
            if visited[routexy[0][1]-1][routexy[0][0]]==distance-1:
                routexy.insert(0,[routexy[0][0],routexy[0][1]-1])
                distance=distance-1
    return(routexy)

#Function with the suspected fault
def routeturtle(routexy,startx,starty,gridsize):
    turtle.speed(0)
    turtle.penup()
    x=startx+gridsize/2
    y=starty+gridsize/2
    turtle.goto(x,y)
    turtle.pendown()
    turtle.pensize(gridsize/2)
    turtle.color("blue")
    for a in range(len(routexy)-1):
        x=x+(routexy[a+1][0]-routexy[a][0])*gridsize
        y=y+(routexy[a+1][1]-routexy[a][1])*gridsize
        turtle.goto(x,y)

def cellpath(x,y,gridsize,startx,starty,sizex,colour):
    turtle.penup()
    turtle.goto(startx+gridsize/2+x*gridsize,starty+gridsize/2+y*gridsize)
    turtle.pendown()
    turtle.pencolor((0,0.99-colour/(sizex*sizex),0))
    turtle.pensize(gridsize/2)
    turtle.forward(1)

#----------------------MAIN----------------------------------
#size of maze
sizex=5
sizey=5
startx=-200
starty=startx
gridsize=(2*(-starty))/sizey

#calling functions
walls=mazegenerate(sizex,sizey)
printmaze(sizex,sizey,walls)
visited=search(walls,sizey,sizex)
routexy=route(visited,sizex,sizey,walls)
input()
routeturtle(routexy,startx,starty,gridsize)

#needed to keep maze window
quit= input("press any key to quit: ")

