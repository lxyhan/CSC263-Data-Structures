class Queue:
    """
    A priority-based queue implemented using a binary min-heap.

    The queue internally stores QueueNode objects in an array-based
    binary heap. Lower priority values correspond to objects that
    are removed earlier.
    """

    class QueueNode:
        """
        A container storing an object and its associated priority.
    
        Args:
        obj (object): The object to store in the queue.
        pri (int): The priority associated with the object. Lower values
            indicate higher priority.
    
        Returns:
        None
        """
        def __init__(self, obj, pri):
            self.obj = obj
            self.pri = pri

    """
    Initialize the Queue data structure.

    Args:
    cap (int): The initial capacity of the queue.

    Returns:
    None
    """
    def __init__(self, cap):
        self.cap = cap
        self.heap = []

    def add(self, obj, pri):
        """
        Add a new object to the queue with the given priority.

        A new QueueNode is created and appended to the internal heap
        array. The method then restores the min-heap property by
        performing a heap-up operation.

        Args:
        obj (object): The object to insert.
        pri (int): The priority associated with the object. Lower values
            indicate higher priority.
        """
        # we start by adding the new obj to the end of the heap
        newObj = Queue.QueueNode(obj, pri)
        self.heap.append(newObj)

        # we bubble up repeatedly until the heap property is restored w.r.t priority
        currentIndex = len(self.heap)-1
        # print(f"Items: {[(node.obj, node.pri) for node in self.heap]}")
        while currentIndex != 0 and newObj.pri > self.heap[(currentIndex-1)//2].pri:
            # print(f"Items: {[(node.obj, node.pri) for node in self.heap]}")
            # print((currentIndex-1)//2)
            # print(currentIndex)
            self.heap[(currentIndex-1)//2], self.heap[currentIndex] = self.heap[currentIndex], self.heap[(currentIndex-1)//2]
            currentIndex = (currentIndex-1)//2
        

    def pop(self):
        """
        Remove and return the object with the largest priority value.

        The root of the heap is removed. The last element in the heap is
        moved to the root position, and a heap-down operation is
        performed to restore the heap property.

        Args:
        None

        Returns:
        object: The object stored in the QueueNode with the largest
            priority value (or None if the Queue is empty).
        """
        # if queue is empty return none
        if len(self.heap) == 0:
            return None

        # swap the last and root node
        self.heap[-1], self.heap[0] = self.heap[0], self.heap[-1]
        root = self.heap.pop()

        # if root was the last element in the heap
        if len(self.heap) == 0:
            return root
        
        currentIndex = 0

        while currentIndex < len(self.heap):
            if 2*currentIndex+2 < len(self.heap):

                # both children exist
                leftIndex = 2*currentIndex+1
                rightIndex = 2*currentIndex+2

                childIndex = leftIndex if self.heap[leftIndex].pri >= self.heap[rightIndex].pri else rightIndex
                if self.heap[currentIndex].pri < self.heap[childIndex].pri:
                    self.heap[currentIndex], self.heap[childIndex] = self.heap[childIndex], self.heap[currentIndex]
                    currentIndex = childIndex
                else:
                    break
            elif 2*currentIndex+1 < len(self.heap):
                leftChild = self.heap[2*currentIndex+1]
                # rightChild = None
                if self.heap[currentIndex].pri < leftChild.pri:
                    self.heap[currentIndex], self.heap[2*currentIndex+1] = self.heap[2*currentIndex+1], self.heap[currentIndex]
                    currentIndex = 2*currentIndex+1
                else:
                    break
            else:
                # curr is a leaf node
                # leftChild = None
                # rightChild = None
                break

        return root


class Tower:
    def __init__(self):
        # Initialize any internal state here
        self.in_flight = {}  # keyed by packet_id, value is (sent_time, packet)
        self.time = 0
        self.queue = Queue(10)

    def process(self, new_packets):
        """
        Called once per time step.

        Parameters:
            new_packets: a list of packets that arrived at this time step

        Returns:
            read_packets: packets that were read/received this step
            sent_packets: packets that were sent out this step
            acked_packets: packets that were acknowledged this step
        """

        packet_type_processing_times = {
            "text": 1,
            "picture": 2,
            "audio": 3,
            "video": 4,
            "ack": 1,
        }


        # Step 1: advance time
        self.time += 1

        # Step 2: record or process newly arrived packets
        read_packets = []

        # Step 3: logic determining which packets get acknowledged

        acked_packets = []

        # Step 4: logic determining which packets get sent this step
        sent_packets = []

        for packet in new_packets:
            if packet.packet_type != "ack":
                priority = packet_type_processing_times[packet.packet_type] + packet.ack_time_tolerance
                self.queue.add(packet, -1 * priority)
            else:
                acked_packets.append(packet)
                self.in_flight.pop(packet.packet_id, None)
        
        # send the packet
        popped_packet = self.queue.pop()
        if popped_packet is not None:
            sent_packets.append(popped_packet.obj)
            self.in_flight[popped_packet.obj.packet_id] = (self.time, popped_packet.obj)

        # check for expired packets and resend them
        for packet_id in list(self.in_flight.keys()):
            sent_time, packet = self.in_flight[packet_id]

            # if expired we resend it
            if self.time - sent_time > packet.ack_time_tolerance:
                self.in_flight.pop(packet_id)
                priority = packet_type_processing_times[packet.packet_type] + packet.ack_time_tolerance
                self.queue.add(packet, -1 * priority)

        return read_packets, sent_packets, acked_packets