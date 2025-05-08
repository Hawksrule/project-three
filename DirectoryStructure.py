import time
import re

class DirectoryNode:
    def __init__(self, name, size = 0, is_leaf = False):
        self.name = name
        self.size = size
        self.is_leaf = is_leaf
        self._cached_total_size = None
        if not is_leaf:
            self.children = []

    def add_child(self, child):
        self.children.append(child)
        self._cached_total_size = None

    def remove_child(self, child):
        self.children.remove(child)
        self._cached_total_size = None

class Directory:
    def __init__(self, root):
        self.root = root
        
    def insert_child(self, node, path, child_node):
        parts = path.strip('/').split('/')
        for part in parts[1:]:  # Skip the root, already passed in
            node = next((c for c in node.children if c.name == part and not c.is_leaf), None)
            if node is None:
                return  # Path invalid, optionally raise an error
        node.add_child(child_node)
    
    def find_file(self, root, child_name, path=""):
        if root.name == child_name:
            return (path + '/' + root.name).lstrip('/')
        if not root.is_leaf:
            for child in root.children:
                result = self.find_file(child, child_name, path + '/' + root.name)
                if result:
                    return result
        return None


    def find_wildcard(self, parent, search_term, total_files, path =""):
        if parent.is_leaf: #Ensures Leafs only appear once in total_files
            result = self.match_terms(parent, search_term)
            if result is True:
                return total_files.append(f"{path + "/" + parent.name}")
            return
        path = path + "/" + parent.name
        for child in parent.children:
            self.find_wildcard(child, search_term, total_files, path)
        return total_files


    def match_terms(self, child_name, search_term):
        try:
            reg_search_term = search_term.replace('*', '.*').replace('?', '.').replace('!', '^').replace('#', '\\d+')
            pattern = re.compile(reg_search_term)
            match = re.match(pattern, child_name.name)
            
            return bool(match)
        except re.PatternError: #Stops crash when invalid search syntax is entered
            return "Error"
    
    def find_size(self, root, folder_name=None):
        if root.name == folder_name:
            return self._cached_or_sum(root)
        if not root.is_leaf:
            for child in root.children:
                result = self.find_size(child, folder_name)
                if result is not None:
                    return result

    def _cached_or_sum(self, node):
        if node._cached_total_size is not None:
            return node._cached_total_size
        if node.is_leaf:
            node._cached_total_size = node.size
        else:
            node._cached_total_size = sum(self._cached_or_sum(child) for child in node.children)
        return node._cached_total_size
    
    def traverse_preorder(self, node):
        if node:
            print(node.name, node.size, end=" ")
            if not node.is_leaf:
                for child in node.children:
                    self.traverse_preorder(child)
                
if __name__ == "__main__":
    root = DirectoryNode("Root")
    files = Directory(root=root)
    
    #Building tree mirroring Root directory in repo
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
    
    print("Welcome to the Root Directory!",
          "\nYou can select from a handful",
          "\nof queries to withdraw data and",
          "\nstatistics from the directory.",)
    

    while True:
        query = input("\n\tFind file: 'FileName' \n\tFolder size: 'FolderName' \n\tShortest Path: 'FileName' \n\tFind all: 'Type' (Folder, File, .txt, .pdf) \n\tFind files: '(>, <, ==)' 'Size': \n\tWildcard Search: To quit q:\n\nEnter Choice: ").split(':')
        
        while len(query) < 2:
            query = input("You must provide a query formatted as such: 'Find file: File3.txt': ").split(':')
            
        query = [x.strip() for x in query]
            
        if query[0].lower() == "find file":
            print(f"Finding {query[1]} in Root...")
            start_time = time.time()
            print(f"Path: {files.find_file(root, query[1])}")
            end_time = time.time()
            print(f"Elapsed time: {end_time - start_time}")
            
        elif query[0].lower() == "folder size":
            print(f"Calculating {query[1]} size...")
            start_time = time.time()
            print(f"Total size: {files.find_size(root, query[1])}mb")
            end_time = time.time()
            print(f"Elapsed time: {end_time - start_time}")
            
        elif query[0].lower() == "wildcard search":
            found_files = None
            print(f"Finding files containing {query[1]}")
            start_time = time.time()
            found_files = files.find_wildcard(root, query[1], [])
            print(f"Files containing {[None if found_files is None else len(found_files)]}")
            if found_files is not None:
                for i in found_files:
                    print(i)
            end_time = time.time()
            print(f"Elapsed time: {end_time - start_time}")

        elif query[0].lower() == "q":
            print("Thank you! Goodbye.")
            break


