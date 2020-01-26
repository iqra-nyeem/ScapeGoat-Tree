import math


class Node():
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

    def __repr__(self):
        return str(self.key)


class ScapeGoatTree():
    def __init__(self, a):
        self.a = a
        self.size = 0
        self.max_size = 0
        self.root = None

    def sizeOf(self, x):
        if x == None:
            return 0
        return 1 + self.sizeOf(x.left) + self.sizeOf(x.right)

    def haT(self):
        return math.floor(math.log(self.size, 1.0 / self.a))
    def isDeep(self, depth):
        return depth > self.haT()
    def brotherOf(self, node, parent):
        if parent.left != None and parent.left.key == node.key:
            return parent.right
        return parent.left
    def myRebuildTree(self, root, length):
        def flatten(node, nodes):
            if node == None:
                return
            flatten(node.left, nodes)
            nodes.append(node)
            flatten(node.right, nodes)

        def buildTreeFromSortedList(nodes, start, end):
            if start > end:
                return None
            mid = int(math.ceil(start + (end - start) / 2.0))
            node = Node(nodes[mid].key)
            # node = nodes[mid]
            node.left = buildTreeFromSortedList(nodes, start, mid - 1)
            node.right = buildTreeFromSortedList(nodes, mid + 1, end)
            return node

        nodes = []
        flatten(root, nodes)
        return buildTreeFromSortedList(nodes, 0, length - 1)

    def minimum(self, x):
        while x.left != None:
            x = x.left
        return x
    def delete(self, delete_me):
        node = self.root
        parent = None
        is_left_child = True
        while node.key != delete_me:
            parent = node
            if delete_me > node.key:
                node = node.right
                is_left_child = False
            else:
                node = node.left
                is_left_child = True

        successor = None
        if node.left == None and node.right == None:
            pass
        elif node.left == None:
            successor = node.right
        elif node.right == None:
            successor = node.left
        else:
            successor = self.minimum(node.right)
            if successor == node.right:
                successor.left = node.left
            else:
                print("finding successor")
                successor.left = node.left
                tmp = successor.right
                successor.right = node.right
                node.right.left = tmp

        if parent == None:
            self.root = successor
        elif is_left_child:
            parent.left = successor
        else:
            parent.right = successor

        self.size -= 1
        if self.size < self.a * self.max_size:
            self.root = self.myRebuildTree(self.root, self.size)
            self.max_size = self.size

    def search(self, key):
        x = self.root
        while x != None:
            if x.key > key:
                x = x.left
            elif x.key < key:
                x = x.right
            else:
                return x;

        return None

    def insert(self, key):
        z = Node(key)
        y = None
        x = self.root
        depth = 0
        parents = []
        while x != None:
            parents.insert(0, x)
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right
            depth += 1

        if y == None:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z

        self.size += 1
        self.max_size = max(self.size, self.max_size)

        if self.isDeep(depth):
            scapegoat = None
            parents.insert(0, z)
            sizes = [0] * len(parents)
            I = 0
            for i in range(1, len(parents)):
                sizes[i] = sizes[i - 1] + self.sizeOf(self.brotherOf(parents[i - 1], parents[i])) + 1
                if not self.isAWeightBalanced(parents[i], sizes[i] + 1):
                    scapegoat = parents[i]
                    I = i

            tmp = self.myRebuildTree(scapegoat, sizes[I] + 1)

            scapegoat.left = tmp.left
            scapegoat.right = tmp.right
            scapegoat.key = tmp.key

    def isAWeightBalanced(self, x, size_of_x):
        a = self.sizeOf(x.left) <= (self.a * size_of_x)
        b = self.sizeOf(x.right) <= (self.a * size_of_x)
        return a and b

    # def flatten(self, root, head):
    #    if root == None:
    #        return head
    #    root.right = self.flatten(root.right, head)
    #    return self.flatten(root.left, root)

    # def buildTree(self, size, head):
    #    if size == 1:
    #        return head
    #    elif size == 2:
    #        (head.right).left = head
    #        return head.right
    #    root = (self.buildTree(math.floor((size-1)/2.0), head)).right
    #    last = self.buildTree(math.floor((size-1)/2.0), root.right)
    #    root.left = head
    #    return last

    # def rebuildTree(self, scapegoat, size):
    #    head = self.flatten(scapegoat, None)
    #    self.buildTree(size, head)
    #    return head

    def preOrder(self, x):
        if x != None:
            print(x.key)
            self.preOrder(x.left)
            self.preOrder(x.right)

    def printTree(self):
        self.preOrder(self.root)


if __name__ == '__main__':
    import sys
    import re

    # Use tree.txt or command line for file
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'C:/Users/18b-037-cs/Desktop/tree.txt'

    f = open(filename, 'r')
    t = None
    for line in f.readlines():
        line = re.split(r'\s+', line)
        cmd = line[0]
        if cmd == "BuildTree":
            t = ScapeGoatTree(float(line[1]))
            t.insert(int(line[2]))
        elif cmd == "Insert":
            t.insert(int(line[1]))
        elif cmd == "Print":
            t.printTree()
        elif cmd == "Delete":
            t.delete(int(line[1]))
        elif cmd == "Done":
            print("Exiting")
            exit(0)
        elif cmd == "Search":
            val = t.search(int(line[1]))
            if val != None:
                print("Found %d" % (val.key))
            else:
                print("Error: Key %d not found" % (int(line[1])))
        else:
            print("Error: Command not recognized")


