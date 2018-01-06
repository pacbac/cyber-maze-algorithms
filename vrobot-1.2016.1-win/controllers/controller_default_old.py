from array import array
from math import hypot
def control_robot(robot):
	""" control robot.

	Keyword arguments:
	robot -- Robot object that must be throught the maze

	"""

	curx = 0
	cury = 0
	orientation = 1
	listX = array('l',[0])
	listY = array('l',[0])
	coordNum = 0
	listMoves = array('I',[0])
	movesNum = 0
	canMoveRight = False
	canMoveForward = False
	canMoveLeft = False
	tally = 0
	while robot.num_viruses_left() > 0:
		tally = 0
		canMoveRight = True
		canMoveForward = True
		canMoveLeft = True
		while tally <= coordNum:
			if orientation == 1:
				if listX[tally] == curx + 1 and listY[tally] == cury:
					canMoveRight = False
				if listX[tally] == curx - 1 and listY[tally] == cury:
					canMoveLeft = False
				if listY[tally] == cury + 1 and listX[tally] == curx:
					canMoveForward = False
			elif orientation == 2:
				if listX[tally] == curx + 1 and listY[tally] == cury:
					canMoveForward = False
				if listY[tally] == cury + 1 and listX[tally] == curx:
					canMoveLeft = False
				if listY[tally] == cury - 1 and listX[tally] == curx:
					canMoveRight = False
			elif orientation == 3:
				if listX[tally] == curx + 1 and listY[tally] == cury:
					canMoveLeft = False
				if listX[tally] == curx - 1 and listY[tally] == cury:
					canMoveRight = False
				if listY[tally] == cury - 1 and listX[tally] == curx:
					canMoveForward = False
			elif orientation == 4:
				if listX[tally] == curx - 1 and listY[tally] == cury:
					canMoveForward = False
				if listY[tally] == cury + 1 and listX[tally] == curx:
					canMoveRight = False
				if listY[tally] == cury - 1 and listX[tally] == curx:
					canMoveLeft = False
			else:
				canMoveRight = canMoveRight
			tally = tally + 1
		if robot.sense_steps(robot.SENSOR_RIGHT) >= 1 and canMoveRight:
			orientation = orientation + 1
			if orientation == 5:
				orientation = 1
			robot.turn_right()
			robot.step_forward()
			if orientation == 1:
				cury = cury + 1
			elif orientation == 2:
				curx = curx + 1
			elif orientation == 3:
				cury = cury - 1
			elif orientation == 4:
				curx = curx - 1
			coordNum = coordNum + 1
			listX.append(curx)
			listY.append(cury)
			listMoves.append(0)
			listMoves[movesNum] = 1
			movesNum = movesNum + 1
		elif robot.sense_steps(robot.SENSOR_FORWARD) >= 1 and canMoveForward:
			robot.step_forward()
			if orientation == 1:
				cury = cury + 1
			elif orientation == 2:
				curx = curx + 1
			elif orientation == 3:
				cury = cury - 1
			elif orientation == 4:
				curx = curx - 1
			coordNum = coordNum + 1
			listX.append(curx)
			listY.append(cury)
			listMoves.append(0)
			listMoves[movesNum] = 2
			movesNum = movesNum + 1	
		elif robot.sense_steps(robot.SENSOR_LEFT) >= 1 and canMoveLeft:
			orientation = orientation - 1
			if orientation == 0:
				orientation = 4
			robot.turn_left()
			robot.step_forward()
			if orientation == 1:
				cury = cury + 1
			elif orientation == 2:
				curx = curx + 1
			elif orientation == 3:
				cury = cury - 1
			elif orientation == 4:
				curx = curx - 1
			coordNum = coordNum + 1
			listX.append(curx)
			listY.append(cury)
			listMoves.append(0)
			listMoves[movesNum] = 3
			movesNum = movesNum + 1
		else:
			if listMoves[movesNum - 1] == 1:
				if orientation == 1:
					cury = cury - 1
				elif orientation == 2:
					curx = curx - 1
				elif orientation == 3:
					cury = cury + 1
				elif orientation == 4:
					curx = curx + 1
				robot.step_backward()
				robot.turn_left()
				orientation = orientation - 1
				if orientation == 0:
					orientation = 4
			elif listMoves[movesNum - 1] == 2:
				if orientation == 1:
					cury = cury - 1
				elif orientation == 2:
					curx = curx - 1
				elif orientation == 3:
					cury = cury + 1
				elif orientation == 4:
					curx = curx + 1
				robot.step_backward()
			elif listMoves[movesNum - 1] == 3:
				if orientation == 1:
					cury = cury - 1
				elif orientation == 2:
					curx = curx - 1
				elif orientation == 3:
					cury = cury + 1
				elif orientation == 4:
					curx = curx + 1
				robot.step_backward()
				robot.turn_right()
				orientation = orientation + 1
				if orientation == 5:
					orientation = 1
			if movesNum > 0:
				movesNum = movesNum - 1
	curx = 0
	cury = 0
	orientation = 1
	listX = array('l',[0])
	listY = array('l',[0])
	coordNum = 0
	listMoves = array('I',[0])
	movesNum = 0
	canMoveRight = False
	canMoveForward = False
	canMoveLeft = False
	tally = 0
	while True:
		tally = 0
		canMoveRight = True
		canMoveForward = True
		canMoveLeft = True
		while tally <= coordNum:
			if orientation == 1:
				if listX[tally] == curx + 1 and listY[tally] == cury:
					canMoveRight = False
				if listX[tally] == curx - 1 and listY[tally] == cury:
					canMoveLeft = False
				if listY[tally] == cury + 1 and listX[tally] == curx:
					canMoveForward = False
			elif orientation == 2:
				if listX[tally] == curx + 1 and listY[tally] == cury:
					canMoveForward = False
				if listY[tally] == cury + 1 and listX[tally] == curx:
					canMoveLeft = False
				if listY[tally] == cury - 1 and listX[tally] == curx:
					canMoveRight = False
			elif orientation == 3:
				if listX[tally] == curx + 1 and listY[tally] == cury:
					canMoveLeft = False
				if listX[tally] == curx - 1 and listY[tally] == cury:
					canMoveRight = False
				if listY[tally] == cury - 1 and listX[tally] == curx:
					canMoveForward = False
			elif orientation == 4:
				if listX[tally] == curx - 1 and listY[tally] == cury:
					canMoveForward = False
				if listY[tally] == cury + 1 and listX[tally] == curx:
					canMoveRight = False
				if listY[tally] == cury - 1 and listX[tally] == curx:
					canMoveLeft = False
			else:
				canMoveRight = canMoveRight
			tally = tally + 1
		if robot.sense_steps(robot.SENSOR_RIGHT) >= 1 and canMoveRight:
			orientation = orientation + 1
			if orientation == 5:
				orientation = 1
			robot.turn_right()
			robot.step_forward()
			if orientation == 1:
				cury = cury + 1
			elif orientation == 2:
				curx = curx + 1
			elif orientation == 3:
				cury = cury - 1
			elif orientation == 4:
				curx = curx - 1
			coordNum = coordNum + 1
			listX.append(curx)
			listY.append(cury)
			listMoves.append(0)
			listMoves[movesNum] = 1
			movesNum = movesNum + 1
		elif robot.sense_steps(robot.SENSOR_FORWARD) >= 1 and canMoveForward:
			robot.step_forward()
			if orientation == 1:
				cury = cury + 1
			elif orientation == 2:
				curx = curx + 1
			elif orientation == 3:
				cury = cury - 1
			elif orientation == 4:
				curx = curx - 1
			coordNum = coordNum + 1
			listX.append(curx)
			listY.append(cury)
			listMoves.append(0)
			listMoves[movesNum] = 2
			movesNum = movesNum + 1	
		elif robot.sense_steps(robot.SENSOR_LEFT) >= 1 and canMoveLeft:
			orientation = orientation - 1
			if orientation == 0:
				orientation = 4
			robot.turn_left()
			robot.step_forward()
			if orientation == 1:
				cury = cury + 1
			elif orientation == 2:
				curx = curx + 1
			elif orientation == 3:
				cury = cury - 1
			elif orientation == 4:
				curx = curx - 1
			coordNum = coordNum + 1
			listX.append(curx)
			listY.append(cury)
			listMoves.append(0)
			listMoves[movesNum] = 3
			movesNum = movesNum + 1
		else:
			if listMoves[movesNum - 1] == 1:
				if orientation == 1:
					cury = cury - 1
				elif orientation == 2:
					curx = curx - 1
				elif orientation == 3:
					cury = cury + 1
				elif orientation == 4:
					curx = curx + 1
				robot.step_backward()
				robot.turn_left()
				orientation = orientation - 1
				if orientation == 0:
					orientation = 4
			elif listMoves[movesNum - 1] == 2:
				if orientation == 1:
					cury = cury - 1
				elif orientation == 2:
					curx = curx - 1
				elif orientation == 3:
					cury = cury + 1
				elif orientation == 4:
					curx = curx + 1
				robot.step_backward()
			elif listMoves[movesNum - 1] == 3:
				if orientation == 1:
					cury = cury - 1
				elif orientation == 2:
					curx = curx - 1
				elif orientation == 3:
					cury = cury + 1
				elif orientation == 4:
					curx = curx + 1
				robot.step_backward()
				robot.turn_right()
				orientation = orientation + 1
				if orientation == 5:
					orientation = 1
			else:
				if orientation == 1:
					cury = cury - 1
				elif orientation == 2:
					curx = curx - 1
				elif orientation == 3:
					cury = cury + 1
				elif orientation == 4:
					curx = curx + 1
				robot.step_backward()
				movesNum = movesNum + 1
			if movesNum > 0:
				movesNum = movesNum - 1