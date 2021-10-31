# Dining Philosophers
Arduino + Raspberry Pi to provide a visual representation for the Dining Philosophers Problem
## Premise
For this project, we decided to examine how small form factor systems commonly used in projects, like the Arduino and Raspberry Pi devices, interact with operating systems. As a part of this, we decided to program the dining philosophers problem and use it to show a visual representation on LEDs.
## The Dining Philosopher Problem
The Dining Philosopher Problem is a problem where N philosophers and N forks are arranged in a circle, such that each philosopher has a fork to their right and left. Each philosopher eats and thinks, and to eat, they must have both the left and right fork. The problem is that many solutions lead to a deadlock, where each philosopher is stuck in a state where they can not eat. One solution involves the use of semaphores, which help prevent deadlock. 
## Code
In this repository, there are two separate files, which both attempt to offer a solution to the dining philosophers problem. The first, dining_philosopher_deadlock.py, takes a naive approach by having every philosopher reach for their left fork first, and then for the right fork which is now taken, resulting in an instant deadlock. The second, dining_philosopher.py, implements the semaphore approach and allows for every philosopher to go from the eating to thinking state without getting stuck.
## Why Python?
Arduino provides an IDE that allows for code to be written in C++; however, given the short time we had to learn how to work with the Arduino, we opted instead to use Python, which is familiar to us and allows for simple communication with the Arduino. Rather than run the entire algorithm on the device, the Arduino only handles the turning on and off of the LEDs, while the Raspberry Pi takes care of the rest of the algorithm. This is accomplished using Firmata, an intermediate protocol that connects an embedded system to a host computer.
