#Dining Philosophers

import time
import threading
import random
import time
from pyfirmata import Arduino, util

#inheriting threading class in Thread module
class Philosopher(threading.Thread):
    running = True  #used to check if everyone is finished eating

 #Since the subclass overrides the constructor, it must make sure to invoke the base class constructor (Thread.__init__()) before doing anything else to the thread.
    def __init__(self, index, lightPin, forkOnLeft, forkOnRight):
        threading.Thread.__init__(self)
        self.index = index
        self.lightPin = lightPin
        self.forkOnLeft_ledPin = forkOnLeft[0]
        self.forkOnRight_ledPin = forkOnRight[0]
        self.forkOnLeft = forkOnLeft[1]
        self.forkOnRight = forkOnRight[1]
        self.lightPin = lightPin


    def run(self):
        while(self.running):
            # Philosopher is thinking (but really is sleeping).
            time.sleep(30)
            print ('Philosopher %s is hungry.' % self.index)
            flash(self.lightPin,3)
            self.dine()

    def dine(self):
        # if both the semaphores(forks) are free, then philosopher will eat
        fork1, fork2 = self.forkOnLeft, self.forkOnRight
        led1, led2 = self.forkOnLeft_ledPin, self.forkOnRight_ledPin
        while self.running:
            fork1.acquire() # wait operation on left fork
            locked = fork2.acquire(False) 
            if locked: break #if right fork is not available leave left fork
            fork1.release()
            print ('Philosopher %s swaps forks.' % self.index)
            fork1, fork2 = fork2, fork1
            led1, led2 = led2, led1
        else:
            return
        self.dining(led1,led2)
        #release both the fork after dining
        fork2.release()
        fork1.release()
 
    def dining(self,fork1,fork2):
        print ('Philosopher %s starts eating. '% self.index)
        on(self.lightPin)
        on(fork1)
        on(fork2)
        time.sleep(30)
        print ('Philosopher %s finishes eating and leaves to think.' % self.index)
        off(self.lightPin)
        off(fork1)
        off(fork2)

def on(ledPin):
    board.digital[ledPin].write(1)
    return

def flash(ledPin,n):
    for _ in range(n):
        board.digital[ledPin].write(1)
        time.sleep(0.2)
        board.digital[ledPin].write(0)
        time.sleep(0.2)

def off(ledPin):
    board.digital[ledPin].write(0)
    return

def main():
    #parameters:
    led_pins_philosopher = [5,6,7,8]
    num_philosopher = len(led_pins_philosopher)
    led_pins_forks = [1,2,3,4]

    board = Arduino('/dev/ttyUSB0')
    global board

    #initialize arduino
    forks = [(pin,threading.Semaphore()) for pin in led_pins_forks]

    #here (i+1)%num_philosopher is used to get right and left forks circularly between 1-num_philosopher
    philosophers= [Philosopher(i, led_pins_philosopher[i],forks[i%num_philosopher], forks[(i+1)%num_philosopher])
            for i in range(num_philosopher)]

    Philosopher.running = True
    for p in philosophers: p.start()
    time.sleep(100)
    Philosopher.running = False
    print ("Now we're finishing.")
    for i in led_pins_philosopher:
        off(i)
 

if __name__ == "__main__":
    main()


