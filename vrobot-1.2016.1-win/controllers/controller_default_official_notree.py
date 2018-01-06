"""
Orientation will be logged as an integer between 0 and 3,
with 0 being the starting orientation, right 1, left 3, and
back 2.
"""

def scanVirus(robot, scanPos, viruses_list):
    list = robot.sense_viruses()
    for i in list:
        viruses_list.append((i[0] + scanPos[0], i[1] + scanPos[1])) 
        #viruses are given as 2-element arrays, which are mutable: [x, y]. you have to change it to a tuple (x, y) to make it immutable so it is hashable into a set() later on
    return viruses_list

def findMin(iterable, pos):
    smallest = iterable[0]
    for i in iterable:
            if abs(i[0]-pos[0]) + abs(i[1]-pos[1]) < abs(smallest[0]) + abs(smallest[1]):
                smallest = i
    return smallest

def goLeft(robot, dir): #turn, step forward, and update direction
    robot.turn_left()
    robot.step_forward()
    dir = updateDir(dir, 3)
    return dir

def goRight(robot, dir): #turn, step forward, and update direction
    robot.turn_right()
    robot.step_forward()
    dir = updateDir(dir, 1)
    return dir

def goForward(robot):
    robot.step_forward()
    
def uTurn(robot, dir): #turn 180 degrees, step forward, and update direction
    robot.turn_left(2)
    robot.step_forward()
    dir = updateDir(dir, 2)
    return dir

def updateDir(dir, num): #update direction; 1: right, 2: uturn, 3: left
    dir += num
    dir %= 4
    return dir

def intersectionPos(dir, curPos, i):
    """special position comparison method exclusively for intersections
    dir is robot orientation, curPos is robot position, i is position of virus (element from viruses_list)"""
    temp = (i[0] - curPos[0], i[1] - curPos[1]) #relative positioning; nearest virus coordinates subtracted from robot position coordinates
    if dir == 1: #adjusts the relative position based on direction robot faces. (Draw the maze out and rotate the coordinate grids and these are the changes that are derived)
        temp = (-temp[1], temp[0])
    elif dir == 2:
        temp = (-temp[0], -temp[1])
    elif dir == 3:
        temp = (temp[1], -temp[0])
    return temp

def updatePos(dir, curPos):  #update robot position; dir = orientation, track = from goLeft, goRight, etc, curPos = robot position
    if dir == 0:
        temp = (curPos[0], curPos[1] + 1)
    elif dir == 1:
        temp = (curPos[0] + 1, curPos[1])
    elif dir == 2:
        temp = (curPos[0], curPos[1] - 1)
    else:
        temp = (curPos[0] - 1, curPos[1])
    return temp

def getAccessible(robot, pos, open, dir):
    smallest = findMin(open, pos)
    if smallest[0] > 0:
        dir = goRight(robot, dir)
    elif smallest[0] < 0:
        dir = goLeft(robot, dir)
    else:
        goForward(robot)
    return dir

def correctMinPos(intersectionArr):
    #precondition: the minPos chosen was a faulty min coordinate (a coordinate that is directly behind the robot, and the robot will enter an infinite loop approaching it)
    minTallyList = intersectionArr[1][:] #copy tally elements of intersectionArr to new list
    minPosList = intersectionArr[0][:] #copy position elements of intersectionArr to new list
    
    oldMinTally = min(minTallyList) #find the faulty minimum tally (pos the robot has been to least)
    oldMinTallyIndex = minTallyList.index(oldMinTally) #get its index
    
    del minPosList[oldMinTallyIndex]
    del minTallyList[oldMinTallyIndex]
    
    minTallyIndex = minTallyList.index(min(minTallyList)) #find index of new minimum
    minPos = minPosList[minTallyIndex] #minPos = corresponding minimum tally index of minPosList
    return minPos
    
def control_robot(robot): #main method, robot object
    """Packet setup"""
    packet_list = list(robot.sense_packets().values())  # obtain packet coords in the form of a list
    for i in range(len(packet_list)):
        packet_list[i] = tuple(packet_list[i])
    packetPos = packet_list.pop(0) #get the first (and only available) packet to track for
    packetsExist = True #whether or not to to jump. This is used to determine whether or not to jump at the last packet's position if we've collected already and passing through there again
    """Packet backtracking setup"""
    pointer = {} #track the paths of the unavailable packets: {packet: [[intersection], [pointer]]}
    reversePointer = [[], []]
    firstInstance = True #first instance of getting packet
    """Position/direction setup"""
    curPos = (0, 0)  # absolute position
    prevPos = curPos
    dir = 0 #absolute direction
    intersection = {} #dictionary to store intersection coords. It's in the form {pos1: [[positionsAdjacent], [tallies]], pos2: [[positionsAdjacent], [tallies]], etc}
    """Virus setup"""
    viruses_list = []
    scanPos = curPos #position at which the robot last scanned for viruses
    viruses_list = scanVirus(robot, scanPos, viruses_list)
    packetChosen = False
    ignored = False #if we have a virus to ignore so we can get packets
    virusesLeft = robot.num_viruses_left()
    while robot.num_viruses_left() > 0:
        print "pointer: " + str(pointer)
        if robot.num_viruses_left() == 1 and packetsExist:
            print "robot.num_viruses_left(): " + str(robot.num_viruses_left())
            print "viruses list: " + str(viruses_list)
            robot.turn_left(2) #uTurn to go back to previousNode
            dir = updateDir(dir, 2)
            print "prevNode: " + str(previousNode)
            """move to the last intersection to prepare for backtracking"""           
            while curPos != previousNode:
                if robot.sense_steps(robot.SENSOR_FORWARD) > 0:  # prioritize forward
                    goForward(robot)
                elif robot.sense_steps(robot.SENSOR_RIGHT) > 0:  # prioritize right last
                    dir = goRight(robot, dir)
                elif robot.sense_steps(robot.SENSOR_LEFT) > 0:  # prioritize left second
                    dir = goLeft(robot, dir)
                else:
                    dir = uTurn(robot, dir)
                prevPos = curPos
                curPos = updatePos(dir, curPos)
                print "curPos: " + str(curPos)
                print "prevPos: " + str(prevPos)
            
            """if the intersection we finished at while backtracking the last packet is not in the backtrack path of the new packet, 
            we have to backtrack our previous backtracking (lol) until we find an intersection that is shared"""
            if not firstInstance: #different case if it's not the first packet
                while curPos not in pointer[packetPos][0]: #if our intersection does not happen to be equal to starting point of pointer[packetPos][0]
                    goal = reversePointer[0].pop() #get the target intersection, which is always the last index
                    goalPointer = reversePointer[1].pop() #get the target intersection's pointer, which is also always last index
                    while curPos != goal: #while it has to first get there and it's not yet at the intersection
                        if robot.sense_steps(robot.SENSOR_FORWARD) > 0:  # prioritize forward so it moves to target as fast as possible
                            goForward(robot)
                        elif robot.sense_steps(robot.SENSOR_RIGHT) > 0:  # prioritize right last
                            dir = goRight(robot, dir)
                        elif robot.sense_steps(robot.SENSOR_LEFT) > 0:  # prioritize left second
                            dir = goLeft(robot, dir)
                        else:
                            dir = uTurn(robot, dir)
                        prevPos = curPos
                        curPos = updatePos(dir, curPos)
                        print "curPos: " + str(curPos)
                        print "prevPos: " + str(prevPos)
                        print "reversePtr: " + str(reversePointer)
                    if dir == 0: #set up all the adjacent positions depending on orientation
                        forwardPos = (curPos[0], curPos[1] + 1)
                        rightPos = (curPos[0] + 1, curPos[1])
                        leftPos = (curPos[0] - 1, curPos[1])
                    elif dir == 1:
                        forwardPos = (curPos[0] + 1, curPos[1])
                        rightPos = (curPos[0], curPos[1] - 1)
                        leftPos = (curPos[0], curPos[1] + 1)
                    elif dir == 2:
                        forwardPos = (curPos[0], curPos[1] - 1)
                        rightPos = (curPos[0] - 1, curPos[1])
                        leftPos = (curPos[0] + 1, curPos[1])
                    else:
                        forwardPos = (curPos[0] - 1, curPos[1])
                        rightPos = (curPos[0], curPos[1] + 1)
                        leftPos = (curPos[0], curPos[1] - 1)
                    if forwardPos == goalPointer: #else use pointers to continue to guide the robot
                        goForward(robot)
                    elif rightPos == goalPointer:
                        dir = goRight(robot, dir)
                    elif leftPos == goalPointer:
                        dir = goLeft(robot, dir)
                    else:
                        dir = uTurn(robot, dir)
                    prevPos = curPos
                    curPos = updatePos(dir, curPos)
                    print "curPos: " + str(curPos)
                    print "prevPos: " + str(prevPos)
                    print "reversePtr: " + str(reversePointer)
                cutOffIndex = pointer[packetPos][0].index(curPos)
                del pointer[packetPos][0][cutOffIndex+1:]
                del pointer[packetPos][1][cutOffIndex+1:]
            
            jump = False
            """Once we've reached a valid intersection for backtracking, we can actually backtrack to the packet"""
            while pointer[packetPos][0]: #iterate through the list of intersections in the pointer list
                goal = pointer[packetPos][0].pop() #get the target intersection, which is always the last index
                goalPointer = pointer[packetPos][1].pop() #get the target intersection's pointer, which is also always last index
                while curPos != goal: #while it has to first get there and it's not yet at the intersection
                    if robot.sense_steps(robot.SENSOR_FORWARD) > 0:  # prioritize forward so it moves to target as fast as possible
                        goForward(robot)
                    elif robot.sense_steps(robot.SENSOR_LEFT) > 0:  # prioritize left second
                        dir = goLeft(robot, dir)
                    elif robot.sense_steps(robot.SENSOR_RIGHT) > 0:  # prioritize right last
                        dir = goRight(robot, dir)
                    else:
                        dir = uTurn(robot, dir)
                    prevPos = curPos
                    curPos = updatePos(dir, curPos)
                    print "curPos: " + str(curPos)
                    print "prevPos: " + str(prevPos)
                if dir == 0: #set up all the adjacent positions depending on orientation
                    forwardPos = (curPos[0], curPos[1] + 1)
                    rightPos = (curPos[0] + 1, curPos[1])
                    leftPos = (curPos[0] - 1, curPos[1])
                elif dir == 1:
                    forwardPos = (curPos[0] + 1, curPos[1])
                    rightPos = (curPos[0], curPos[1] - 1)
                    leftPos = (curPos[0], curPos[1] + 1)
                elif dir == 2:
                    forwardPos = (curPos[0], curPos[1] - 1)
                    rightPos = (curPos[0] - 1, curPos[1])
                    leftPos = (curPos[0] + 1, curPos[1])
                else:
                    forwardPos = (curPos[0] - 1, curPos[1])
                    rightPos = (curPos[0], curPos[1] + 1)
                    leftPos = (curPos[0], curPos[1] - 1)
                if curPos not in reversePointer[0]:
                    reversePointer[0].append(curPos)
                    reversePointer[1].append(prevPos)
                else:
                    delIndex = reversePointer[0].index(curPos)
                    del reversePointer[0][delIndex+1:]
                    del reversePointer[1][delIndex+1:]
                previousNode = curPos
                """REACHED THE INTERSECTION"""
                """if the packet is at the intersection, just jump. else, use the pointers to keep moving closer"""
                if curPos == packetPos: #if the intersection happens to be the packet position, then jump
                    robot.jump()
                    jump = True
                else:
                    if forwardPos == goalPointer: #else use pointers to continue to guide the robot
                        goForward(robot)
                    elif rightPos == goalPointer:
                        dir = goRight(robot, dir)
                    elif leftPos == goalPointer:
                        dir = goLeft(robot, dir)
                    else:
                        dir = uTurn(robot, dir)
                    prevPos = curPos
                    curPos = updatePos(dir, curPos)
                print "packetPtr: " + str(pointer[packetPos][0])
                print "reversePtr: " + str(reversePointer)
                print "pointer: " + str(pointer)
                print "curPos: " + str(curPos)
                print "prevPos: " + str(prevPos)
                        
            """"if the robot is at the last intersection and just has to go a little further to get the packet"""
            while curPos != packetPos:
                if robot.sense_steps(robot.SENSOR_FORWARD) > 0:  # prioritize forward so it moves to target as fast as possible
                    goForward(robot)
                elif robot.sense_steps(robot.SENSOR_LEFT) > 0:  # prioritize left second
                    dir = goLeft(robot, dir)
                elif robot.sense_steps(robot.SENSOR_RIGHT) > 0:  # prioritize right last
                    dir = goRight(robot, dir)
                prevPos = curPos
                curPos = updatePos(dir, curPos)
                print "curPos: " + str(curPos)
                print "prevPos: " + str(prevPos)
            firstInstance = False
            """robot has finally reached the packet"""
            if not jump: 
                robot.jump()
            pointer.pop(packetPos)
            if packet_list:
                packetPos = packet_list.pop(0)
            else:
                packetsExist = False #so it won't jump at the last packet's coordinate when we pass through, after we collected the last packet:
            
            if not packetsExist:
                robot.turn_left(2)
                dir = updateDir(dir, 2)
                while reversePointer[0]:
                    goal = reversePointer[0].pop() #get the target intersection, which is always the last index
                    goalPointer = reversePointer[1].pop() #get the target intersection's pointer, which is also always last index
                    while curPos != goal: #while it has to first get there and it's not yet at the intersection
                        if robot.sense_steps(robot.SENSOR_FORWARD) > 0:  # prioritize forward so it moves to target as fast as possible
                            goForward(robot)
                        elif robot.sense_steps(robot.SENSOR_RIGHT) > 0:  # prioritize right last
                            dir = goRight(robot, dir)
                        elif robot.sense_steps(robot.SENSOR_LEFT) > 0:  # prioritize left second
                            dir = goLeft(robot, dir)
                        prevPos = curPos
                        curPos = updatePos(dir, curPos)
                        print "curPos: " + str(curPos)
                        print "prevPos: " + str(prevPos)
                        print "reversePtr: " + str(reversePointer)
                    if dir == 0: #set up all the adjacent positions depending on orientation
                        forwardPos = (curPos[0], curPos[1] + 1)
                        rightPos = (curPos[0] + 1, curPos[1])
                        leftPos = (curPos[0] - 1, curPos[1])
                    elif dir == 1:
                        forwardPos = (curPos[0] + 1, curPos[1])
                        rightPos = (curPos[0], curPos[1] - 1)
                        leftPos = (curPos[0], curPos[1] + 1)
                    elif dir == 2:
                        forwardPos = (curPos[0], curPos[1] - 1)
                        rightPos = (curPos[0] - 1, curPos[1])
                        leftPos = (curPos[0] + 1, curPos[1])
                    else:
                        forwardPos = (curPos[0] - 1, curPos[1])
                        rightPos = (curPos[0], curPos[1] + 1)
                        leftPos = (curPos[0], curPos[1] - 1)
                    if forwardPos == goalPointer: #else use pointers to continue to guide the robot
                        goForward(robot)
                    elif rightPos == goalPointer:
                        dir = goRight(robot, dir)
                    elif leftPos == goalPointer:
                        dir = goLeft(robot, dir)
                    prevPos = curPos
                    curPos = updatePos(dir, curPos)
        else:
            """Sense surroundings, pick target virus"""
            forward = robot.sense_steps(robot.SENSOR_FORWARD)
            right = robot.sense_steps(robot.SENSOR_RIGHT)
            left = robot.sense_steps(robot.SENSOR_LEFT)
            canMoveForward = forward > 0
            canMoveRight = right > 0
            canMoveLeft = left > 0

            print viruses_list
            if curPos in viruses_list: #sometimes viruses_list has an element that is already equal to curPos. just a safety measure
                viruses_list.remove(curPos)
            
            #break out of everything once there is one virus left. aka stop going for old target because WE NEED TO GET PACKETS NOW
            if curPos in packet_list: 
                putInPointer = curPos #packet position waiting to be put in the tree
                packetChosen = True
                
            if not ignored and viruses_list <= len(packet_list) + 2: #if there is one last virus left that is not below a packet (to ensure we get packets before getting this virus)
                for i in viruses_list: #find the virus and log it as ignoreVirus
                    if  i != packetPos and i not in packet_list:
                        ignoreVirus = i
                        break
                ignored = True

            """decision-making at intersections"""
            isIntersection = False
            open = [] #stores virus positions that the robot can directly access
            
            """use distance formula to determine if it's out of the sensing radius (means there's new viruses in the area)"""
            if ((curPos[0] - scanPos[0]) ** 2 + (curPos[1] - scanPos[1]) ** 2) ** 0.5 >= 9: #9 is a safety measure since 10 sometimes makes robot less sensitive to unknown viruses
                scanPos = curPos #recalibrate last scanned position
                viruses_list = scanVirus(robot, scanPos, viruses_list)
                viruses_list = list(set(viruses_list)) #remove all duplicate elements. this is where turning [x, y] into (x, y) is crucial, so it's compatible with sets and pairs are immutable
            
            """if it's reached an intersection (aka it can move in multiple directions), get accessible viruses"""
            if canMoveForward and canMoveRight and canMoveLeft:
                isIntersection = True
                for i in viruses_list:
                    i = intersectionPos(dir, curPos, i) #i is adjusted so it's relative to the robot's pos at intersection
                    if (i[0] == 0 and i[1] > 0 and forward >= i[1]) or (i[0] > 0 and i[1] == 0 and right >= i[0]) or (i[0] < 0 and i[1] == 0 and abs(i[0]) <= left):
                        #if virus isn't blocked off by wall, so we can access it directly by going straight forward, straight left, straight right
                        open.append(i)
            elif canMoveForward and canMoveRight:
                isIntersection = True
                for i in viruses_list:
                    i = intersectionPos(dir, curPos, i)
                    if (i[0] == 0 and i[1] > 0 and forward >= i[1]) or (i[0] > 0 and i[1] == 0 and right >= i[0]):
                        open.append(i)
            elif canMoveForward and canMoveLeft:
                isIntersection = True
                for i in viruses_list:
                    i = intersectionPos(dir, curPos, i)
                    if (i[0] == 0 and i[1] > 0 and forward >= i[1]) or (i[0] < 0 and i[1] == 0 and abs(i[0]) <= left):
                        open.append(i)
            elif canMoveRight and canMoveLeft:
                isIntersection = True
                for i in viruses_list:
                    i = intersectionPos(dir, curPos, i)
                    if (i[0] > 0 and i[1] == 0 and right >= i[0]) or (i[0] < 0 and i[1] == 0 and abs(i[0]) <= left):
                        open.append(i)
           
            """if we've reached an intersection we've been to before, 
            figure out which direction's we've gone and block them off so we don't potentially loop infinitely"""            
            if isIntersection: #if it's an intersection
                previousNode = curPos             
                if dir == 0: #set up all the adjacent positions depending on orientation
                    forwardPos = (curPos[0], curPos[1] + 1)
                    rightPos = (curPos[0] + 1, curPos[1])
                    leftPos = (curPos[0] - 1, curPos[1])
                elif dir == 1:
                    forwardPos = (curPos[0] + 1, curPos[1])
                    rightPos = (curPos[0], curPos[1] - 1)
                    leftPos = (curPos[0], curPos[1] + 1)
                elif dir == 2:
                    forwardPos = (curPos[0], curPos[1] - 1)
                    rightPos = (curPos[0] - 1, curPos[1])
                    leftPos = (curPos[0] + 1, curPos[1])
                else:
                    forwardPos = (curPos[0] - 1, curPos[1])
                    rightPos = (curPos[0], curPos[1] + 1)
                    leftPos = (curPos[0], curPos[1] - 1)   
                    
                FLR = canMoveForward and canMoveRight and canMoveLeft #simplify boolean values
                FR = canMoveForward and canMoveRight
                FL = canMoveForward and canMoveLeft
                RL = canMoveRight and canMoveLeft
                if curPos not in intersection: #if this is a new intersection, then we need to add in data
                    if FLR:
                        intersection[curPos] = [[rightPos, leftPos, forwardPos, prevPos], [0, 0, 0, 1]]
                    elif FR:
                        intersection[curPos] = [[rightPos, forwardPos, prevPos], [0, 0, 1]]
                    elif FL:
                        intersection[curPos] = [[leftPos, forwardPos, prevPos], [0, 0, 1]]
                    elif RL:
                        intersection[curPos] = [[rightPos, leftPos, prevPos], [0, 0, 1]]
                    
                    """only happens if curPos == prevPos == origin. A safety measure"""
                    if curPos == prevPos:
                        for i in intersection[curPos]:
                            i.pop() #remove origin from prevPos
                        robot.turn_right()
                        if robot.sense_steps(robot.SENSOR_RIGHT) > 0: #check if backwards option is valid for initial starting point when it's an intersection
                            intersection[curPos][0].append((curPos[0], curPos[1] - 1))
                            intersection[curPos][1].append(0)
                            
                        robot.turn_left()
                
                if FLR or FR or FL or RL:
                    minTallyIndex = intersection[curPos][1].index(min(intersection[curPos][1]))
                    minPos = intersection[curPos][0][minTallyIndex]
                    if minPos == prevPos:
                        minPos = correctMinPos(intersection[curPos])
                if minPos == rightPos: #only RHR True
                    canMoveLeft = False
                    canMoveForward = False
                elif minPos == leftPos: #only LHR True
                    canMoveRight = False
                    canMoveForward = False
                elif minPos == forwardPos: #only SHR True
                    canMoveLeft = False
                    canMoveRight = False
            
            if ignored and packetsExist: #if we have a virus to ignore
                if dir == 0: #set up all the adjacent positions depending on orientation
                    forwardPos = (curPos[0], curPos[1] + 1)
                    rightPos = (curPos[0] + 1, curPos[1])
                    leftPos = (curPos[0] - 1, curPos[1])
                elif dir == 1:
                    forwardPos = (curPos[0] + 1, curPos[1])
                    rightPos = (curPos[0], curPos[1] - 1)
                    leftPos = (curPos[0], curPos[1] + 1)
                elif dir == 2:
                    forwardPos = (curPos[0], curPos[1] - 1)
                    rightPos = (curPos[0] - 1, curPos[1])
                    leftPos = (curPos[0] + 1, curPos[1])
                else:
                    forwardPos = (curPos[0] - 1, curPos[1])
                    rightPos = (curPos[0], curPos[1] + 1)
                    leftPos = (curPos[0], curPos[1] - 1)

                if forwardPos == ignoreVirus and canMoveForward:
                    canMoveForward = False
                elif rightPos == ignoreVirus and canMoveRight:
                    canMoveRight = False
                elif leftPos == ignoreVirus and canMoveLeft:
                    canMoveLeft = False
            elif ignored and not packetsExist:
                ignored = False

            print "curPos: " + str(curPos)
            print "prevPos: " + str(prevPos)
            print intersection
            print "pointer: " + str(pointer)
            print "packet_list" + str(packet_list)
            print "robot.num_viruses_left(): " + str(robot.num_viruses_left())
            print "packetsExist: " + str(packetsExist)
            if ignored:
                print "ignoreVirus: " + ignoreVirus
                
            """movement"""
            if curPos not in intersection:
                if not open: #if open is empty
                    "left hand rule"
                    if canMoveLeft:  # prioritize left first
                        dir = goLeft(robot, dir)
                    elif canMoveForward:  # prioritize forward second
                        goForward(robot)
                    elif canMoveRight:  # prioritize right last
                        dir = goRight(robot, dir)
                    else:  #dead end
                        dir = uTurn(robot, dir)
                
                else: #if open has elements
                    """shouldn't have to worry about intersection dictionary
                     interfering with these block of statements"""
                    dir = getAccessible(robot, (0, 0), open, dir)
                        
            else:
                if not open: #force the robot to not follow the traditional right/left/straight hand rule so it can break out of the loop
                    if canMoveRight:
                        dir = goRight(robot, dir)
                    elif canMoveForward:
                        goForward(robot)
                    elif canMoveLeft:
                        dir = goLeft(robot, dir)
                    else:
                        dir = uTurn(robot, dir)
                else: #if open has elements
                    """shouldn't have to worry about intersection dictionary 
                    interfering with these block of statements"""
                    dir = getAccessible(robot, (0, 0), open, dir)

            if isIntersection:
                for i in pointer.keys(): #update entire pointer dictionary
                    if curPos not in pointer[i][0]: #if curPos is not a repeated intersection, add in the new intersection and its pointer as normal
                        pointer[i][0].append(curPos)
                        pointer[i][1].append(prevPos)
                    elif curPos in pointer[i][0]: #if curPos is a repeated intersection, we don't want any loops when backtracking
                        delIndex = pointer[i][0].index(curPos) #find where curPos occurs
                        del pointer[i][0][delIndex+1:] #delete all the intersections after it (takes away loops when backtracking)
                        del pointer[i][1][delIndex+1:]
                if packetChosen: #if it's the first time adding the packet in, also add in the nearest intersection to it
                    pointer[putInPointer] = [[curPos], [prevPos]]
                    packetChosen = False            
                    
            prevPos = curPos #keep track of previous position for logging intersection data                    
            curPos = updatePos(dir, curPos) #update robot position
            
            """add anti-looping data"""
            if curPos in intersection and prevPos in intersection[curPos][0]:
                intersection[curPos][1][intersection[curPos][0].index(prevPos)] += 1
            if prevPos in intersection: #log coordinates (we logged prevPos in case it was an intersection and we needed it)
                intersection[prevPos][1][intersection[prevPos][0].index(curPos)] += 1
            #the coordinate elements in intersection[prevPos][1] are always adjacent to prevPos
            """since we don't sense viruses often, 
            we will manually remove viruses from our list of 
            available viruses. Also saves time"""
            print "viruses list: " + str(viruses_list)
            if curPos in viruses_list:
                viruses_list.remove(curPos)
                #virusesLeft -= 1

            """jump when we reach the green packet"""
            if curPos == packetPos and packetsExist:
                robot.jump()
                if packet_list:
                    packetPos = tuple(packet_list.pop(0))
                else:
                    packetsExist = False #so it won't jump at the last packet's coordinate when we pass through, after we collected the last packet 
            print "MOVE" #log robot movement in output