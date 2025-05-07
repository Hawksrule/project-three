class DirectoryNode:
    def __init__(self, name, size = 0, is_leaf = False):
        self.name = name
        self.size = size
        self.is_leaf = is_leaf
        if not is_leaf:
            self.children = []

    def add_child(self, child):
        self.children.append(child)

    def remove_child(self, child):
        self.children.remove(child)

class Directory:
    def __init__(self, root):
        self.root = root
        
    def insert_child(self, root, path, child_node):
        if root:
            if root.name == path:
                root.add_child(child_node)
            else:
                if not root.is_leaf:
                    for child in root.children:
                        if child.name == path[len(root.name)+1:len(root.name)+1 + len(child.name)]:
                            self.insert_child(child, path[len(root.name)+1:], child_node)
                    

    def traverse_preorder(self, node):
        if node:
            print(node.name, node.size, end=" ")
            if not node.is_leaf:
                for child in node.children:
                    self.traverse_preorder(child)
                
if __name__ == "__main__":
    root = DirectoryNode("Root")
    files = Directory(root=root)
    files.insert_child(root, "Root", DirectoryNode(name="Folder1"))
    files.insert_child(root, "Root", DirectoryNode(name="Folder2"))
    files.insert_child(root, "Root/Folder1", DirectoryNode(name="SubFolder1"))
    files.insert_child(root, "Root/Folder1", DirectoryNode(name="File1.txt", size=10, is_leaf=True))
    files.insert_child(root, "Root/Folder1", DirectoryNode(name="File2.txt", size=5, is_leaf=True))
    files.insert_child(root, "Root/Folder1/SubFolder1", DirectoryNode(name="File3.txt", size=20, is_leaf=True))
    files.insert_child(root, "Root/Folder2", DirectoryNode(name="SubFolder1"))
    files.insert_child(root, "Root/Folder2/SubFolder1", DirectoryNode(name="SubFolder2"))
    files.insert_child(root, "Root/Folder2/SubFolder1/SubFolder2", DirectoryNode(name="File4.txt", size=15, is_leaf=True))
    files.insert_child(root, "Root/Folder2", DirectoryNode(name="File5.pdf", size=30, is_leaf=True))
    files.traverse_preorder(root)
    
    