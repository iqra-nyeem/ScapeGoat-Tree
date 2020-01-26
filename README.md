# ScapeGoat-Tree
A ScapeGoat tree is a self-balancing Binary Search Tree like AVL Tree, Red-Black Tree, Splay Tree, ..etc.

Search time is O(Log n) in worst case. Time taken by deletion and insertion is amortized O(Log n)

The balancing idea is to make sure that nodes are α size balanced. Α size balanced means sizes of left and right subtrees are at most α * (Size of node). The idea is based on the fact that if a node is Α weight balanced, then it is also height balanced: height <= log1/&aplpha;(size) + 1

Unlike other self-balancing BSTs, ScapeGoat tree doesn’t require extra space per node. For example, Red Black Tree nodes are required to have color.
