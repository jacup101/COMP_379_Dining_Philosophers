from pyfirmata import Arduino, util
from time import sleep

# Board changes depending on yeah
board = Arduino('/dev/ttyACM0')

def isCompatibleFork(philosopher, fork, max):
    if philosopher.id == 0:
        if fork.id == philosopher.id or fork.id == max:
            return 1
        else:
            return 0
    else:
        if fork.id == philosopher.id or fork.id == (philosopher.id - 1):
            return 1
        else:
            return 0


class Philosopher:

    def __init__(self, id_num, led):
        self.id = id_num
        self.forksInUse = []
        self.isEating = False
        self.ledIndex = led

    def __str__(self):
        return "isEating {eat} id {id} forks {forks}".format(eat=self.isEating, id = self.id, forks=self.forksInUse)

    def giveFork(self, fork):
        global board
        self.forksInUse.append(fork)
        if len(self.forksInUse) == 2:
            self.isEating = True
            board.digital[self.ledIndex].write(1)

    def getLeftFork(self, max):
        if self.id == 0:
            return max
        else:
            return self.id-1


class Fork:
    def __init__(self, id_num, led):
        self.id = id_num
        self.isInUse = False
        self.assignedTo = -1
        self.ledIndex = led

    def __str__(self):
        return "inUse {eat} id {id} ".format(eat=self.isInUse, id = self.id)

    def giveToPhilosopher(self, philosopher):
        global board
        if self.isInUse is False:
            philosopher.giveFork(self)
            self.isInUse = True
            self.assignedTo = philosopher.id
            board.digital[self.ledIndex].write(1)
        else:
            print("Could not give fork {fork} to philosopher {phil}, assigned to {assigned}".format(fork=self.id, phil=philosopher.id, assigned = self.assignedTo))

        # Turn on fork light here


def create_philosophers_problem(num):
    philosophers = []
    forks = []
    philosopherLEDs = [10, 11, 12, 13]
    forkLEDs = [2, 3, 4, 5]

    for i in range(num):
        philosophers.append(Philosopher(i, philosopherLEDs[i]))
        forks.append(Fork(i, forkLEDs[i]))

    for i in range(num):
        if isCompatibleFork(philosophers[i], forks[philosophers[i].getLeftFork(num-1)], num-1) == 1:
            forks[philosophers[i].getLeftFork(num - 1)].giveToPhilosopher(philosophers[i])
            sleep(.2)
    for i in range(num):
        if isCompatibleFork(philosophers[i], forks[i], num-1) == 1:
            forks[i].giveToPhilosopher(philosophers[i])
            sleep(.2)
    for i in range(num):
        print(philosophers[i])
        print(forks[i])


if __name__ == '__main__':
    create_philosophers_problem(4)