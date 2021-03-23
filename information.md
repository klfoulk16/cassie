# Things to Learn About and Act On:

- Red Black Tree vs AVL Tree

The AVL trees are more balanced compared to Red-Black Trees, but they may cause more rotations during insertion and deletion. So if your application involves frequent insertions and deletions, then Red-Black trees should be preferred. And if the insertions and deletions are less frequent and search is a more frequent operation, then AVL tree should be preferred over Red-Black Tree.

[Source](https://www.geeksforgeeks.org/red-black-tree-set-1-introduction-2/)

Currently, I plan to focus on setting up my database for easy insertions. Later I may readjust if I decide to be more search-heavy. Hence, Red Black Tree it is. Transaction oriented vs analytics oriented, as this is where LSM trees tend to shine.