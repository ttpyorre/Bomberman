
import heapq

class PriorityQueue:
    def __init__(self):
        self.elements = [] # elements of the queue

    def empty(self):
        '''
        return True if empty
        '''
        return len(self.elements) == 0

    def put(self, element, priority):
        ''' put an element to the queue
        element: [any type] of element
        priority: [int or float] of priority of element
        '''
        for i in range(0, len(self.elements)):
            (ePriority, eElement) = self.elements[i]
            if eElement == element:
                if ePriority > priority:
                    self.elements[i] = (priority, element)
                    heapq.heapify(self.elements)    # shuffle based on priority
                return
        heapq.heappush(self.elements, (priority, element))

    # Get
    def get(self):
        '''
        Return an element with top priority
        '''
        return heapq.heappop(self.elements)[1]

    def get_queue(self):
        '''
        Returns queue as a list
        '''
        return self.elements