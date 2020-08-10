import sys
from node import Node

class Decoder():
    def __init__(self, encoded_file):
        self.encoded_file = encoded_file
        self.tree_byte_length = 0
        self.uncompressed_length = 0
        self.tree_info = ""
        self.compressed_data = ""
        self.root = None
    
    def read_in_file_data(self):
        f = open(self.encoded_file, "rb")
        bytes_in_file = f.read()
        try:
            self.tree_byte_length = int.from_bytes(bytes_in_file[0:4], "big")
            self.uncompressed_length = int.from_bytes(bytes_in_file[4:8], "big")
        except ValueError:
            print("Compressed file is incorrectly formatted")
            return
        try:
            self.tree_info = bytes_in_file[8:(8 + self.tree_byte_length)].decode()
        except ValueError:
            print("Error trying to decode tree")
            return 
        for compressed_byte in bytes_in_file[(8 + self.tree_byte_length):]:
            self.compressed_data += format(compressed_byte, "08b")
        f.close()

    def construct_tree(self):
        if self.tree_info == "":
            print("No tree data to construct tree")
            return
        node_stack = []
        for i in range(self.tree_byte_length):
            if self.tree_info[i] == "1":
                node_stack.append(Node(value = self.tree_info[i+1]))
            elif self.tree_info[i] == "0":
                if len(node_stack) == 1:
                    self.root = node_stack.pop()
                    break
                parent_node = Node()
                parent_node.right_child = node_stack.pop()
                parent_node.left_child = node_stack.pop()
                node_stack.append(parent_node)

    def decode_data(self):
        if (self.compressed_data == ""):
            print("No data to decode")
            return
        if self.root is None:
            print("No tree with which to decode data")
            return
        decoded_string = ""
        searcher = self.root
        counter = 0
        for step in self.compressed_data:
            if counter >= self.uncompressed_length:
                break
            if searcher is None:
                break
            if searcher.value is not None:
                decoded_string += searcher.value
                searcher = self.root
                counter += 1
            if step == "0":
                searcher = searcher.left_child
            else:
                searcher = searcher.right_child
        return decoded_string
    


check = Decoder("output.data")
check.read_in_file_data()
check.construct_tree()
decoded = check.decode_data()
print(decoded)
