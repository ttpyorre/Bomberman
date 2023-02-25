#!/usr/bin/enb python3

from priorityQueue import PriorityQueue


elementsLol = PriorityQueue()

pri1 = 4
elA = "A"
A = (pri1, elA)

pri2 = 1
elB = "B"
B = (pri2, elB)

pri3 = 2
elC = "C"
C = (pri3, elC)


elementsLol.put(A[1], A[0])
print(elementsLol.get)
print(elementsLol.get_queue)
elementsLol.put(B[1], B[0])
print(elementsLol.get)
print(elementsLol.get_queue)
elementsLol.put(C[1], C[0])
get = elementsLol.get
print(get)
print(elementsLol.get_queue)
















































