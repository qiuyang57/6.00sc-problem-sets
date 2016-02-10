# Problem Set 6: Simulating robots
# Name:
# Collaborators:
# Time:

import math
import random

import ps6_visualize
import matplotlib.pyplot as plt

# === Provided classes

class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

# === Problems 1

class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        assert width > 0 and height > 0, 'Width and height should be larger than 0!'
        assert isinstance(width, int), 'Width should be integer!'
        assert isinstance(height, int), 'Height should be integer!'
        self.width = width
        self.height = height
        self.tile_cleaned = []
    
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        x = pos.getX()
        y = pos.getY()
        tile_cleaned_coordination = (math.floor(x), math.floor(y))
        if tile_cleaned_coordination not in self.tile_cleaned:
            self.tile_cleaned.append(tile_cleaned_coordination)

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        assert isinstance(m, int), 'm should be integer!'
        assert isinstance(n, int), 'n should be integer!'
        if (m, n) in self. tile_cleaned:
            return True
        else:
            return False
    
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        num = self.width * self.height
        return num


    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        n = len(self.tile_cleaned)
        return n

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        x_random = random.random() * self.width
        y_random = random.random() * self.height

        return Position(x_random, y_random)


    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        if 0 < pos.getX() < self.width and 0 < pos.getY() < self.height:
            return True
        else:
            return False


class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.speed = speed
        self.room = room
        self.position = self.room.getRandomPosition()
        self.direction = random.random() * 360

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.position

    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.direction

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        if self.room.isPositionInRoom(position):
            self.position = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.direction = direction

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        self.position = self.position.getNewPosition(self.direction, self.speed)
        self.room.cleanTileAtPosition(self.position)




# === Problem 2
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current direction; when
    it hits a wall, it chooses a new direction randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        # position = self.position.getNewPosition(self.direction, self.speed)
        # while not self.room.isPositionInRoom(position):
        #     self.direction = random.random() * 360
        #     position = self.position.getNewPosition(self.direction, self.speed)
        # self.setRobotPosition(position)
        # self.room.cleanTileAtPosition(self.position)

        position = self.position.getNewPosition(self.direction, self.speed)
        if self.room.isPositionInRoom(position):
            self.setRobotPosition(position)
            self.room.cleanTileAtPosition(self.position)
        else:
            self.direction = random.random() * 360

# === Problem 3

def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. Robot or
                RandomWalkRobot)
    """
    visual = False
    sum_time_steps = 0.0
    for trial in range(num_trials):
        if visual:
            anim = ps6_visualize.RobotVisualization(num_robots, width, height)
        robot_list = []
        room = RectangularRoom(width, height)
        for _ in range(num_robots):
            robot_list.append(robot_type(room, speed))

        coverage = 0
        num_time_steps = 0
        if visual:
            anim.update(room, robot_list)
        while coverage < min_coverage:
            for robot in robot_list:
                robot.updatePositionAndClean()
            coverage = room.getNumCleanedTiles() / float(room.getNumTiles())
            num_time_steps += 1
            if visual:
                anim.update(room, robot_list)
        if visual:
            anim.done()
        sum_time_steps += num_time_steps
    avg_time_steps = sum_time_steps / float(num_trials)
    return avg_time_steps

avg = runSimulation(1, 1, 20, 20, 1, 1, StandardRobot)
print avg




# === Problem 4
#
# 1) How long does it take to clean 80% of a 20*20 room with each of 1-10 robots?
#
# 2) How long does it take two robots to clean 80% of rooms with dimensions 
#	 20*20, 25*16, 40*10, 50*8, 80*5, and 100*4?

def showPlot1():
    """
    Produces a plot showing dependence of cleaning time on number of robots.
    """
    mean_time = []
    for robot_num in range(1, 11):
        mean_time.append(runSimulation(robot_num, 1, 20, 20, 0.8, 100, RandomWalkRobot))
    plt.plot(range(1, 11), mean_time, 'b-')
    plt.title('Time to clean 80% of a 20*20 room with each of 1-10 robots')
    plt.xlabel('Number of robots')
    plt.ylabel('Time steps')
    plt.show()



def showPlot2():
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    mean_time = []
    dimensions = [(20, 20), (25, 16), (40, 10), (50, 8), (80, 5), (100, 4)]
    for dimension in dimensions:
        mean_time.append(runSimulation(2, 1, dimension[0], dimension[1], 0.8, 100, StandardRobot))
    plt.plot(range(1, 7), mean_time, 'b-')
    plt.title('Time to clean 80% of a 20*20 room with each of 1-10 robots')
    plt.xlabel('Dimensions')
    plt.ylabel('Time steps')
    plt.xticks(range(1, 7), ['20*20', '25*16', '40*10', '50*8', '80*5', '100*4'])
    plt.show()






# === Problem 5

class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random after each time-step.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        # position = self.position.getNewPosition(self.direction, self.speed)
        # while not self.room.isPositionInRoom(position):
        #     self.direction = random.random() * 360
        #     position = self.position.getNewPosition(self.direction, self.speed)
        # self.setRobotPosition(position)
        # self.room.cleanTileAtPosition(self.position)
        self.direction = random.random() * 360
        position = self.position.getNewPosition(self.direction, self.speed)
        if self.room.isPositionInRoom(position):
            self.setRobotPosition(position)
            self.room.cleanTileAtPosition(self.position)




# === Problem 6

# For the parameters tested below (cleaning 80% of a 20x20 square room),
# RandomWalkRobots take approximately twice as long to clean the same room as
# StandardRobots do.
def showPlot3():
    """
    Produces a plot comparing the two robot strategies.
    """
    mean_time1 = []
    mean_time2 = []
    for robot_num in range(1, 11):
        mean_time1.append(runSimulation(robot_num, 1, 20, 20, 0.8, 100, StandardRobot))
        mean_time2.append(runSimulation(robot_num, 1, 20, 20, 0.8, 100, RandomWalkRobot))
    plt.plot(range(1, 11), mean_time1, 'b-')
    plt.plot(range(1, 11), mean_time2, 'r-')
    plt.title('Time to clean 80% of a 20*20 room with each of 1-10 robots')
    plt.xlabel('Number of robots')
    plt.ylabel('Time steps')
    plt.legend(('StandardRobot', 'RandomWalkRobot'))
    plt.show()

if __name__ == '__main__':
    # showPlot1()
    # showPlot2()
    showPlot3()
