"""An SSTable Database. Inspired by Designing Data Intensive Applications."""


class Memtable:
    """
    A sorted in-memory Red Black tree structure. 
    Incoming writes are added to the table.
    """

    def __init__(self):
        pass

    def insert(self):
        """Insert new node in memtable."""
        pass

    def rotate(self):
        """Rotate memtable to meet Red Black Tree restrictions."""
        pass

    def delete(self):
        """Delete a node from the tree."""
        pass


class Node:
    """
    A node containing a piece of data written to a db.
    Either red or black. Part of a Memtable.
    """
    def __init__(self, color):
        self.color = color

    def switch_color(self):
        """Changes color from red to black or vice versa."""
        pass


class TableManager:
    """
    High level manager of various peices of Table in db.

    Ideas:
    - maintain sparse SSTable index
    - manage timing of writing out memtable
    - handles log, including deletion when memtable written to disk
    - handles compaction and merging of SSTable files on disk
    """
    
    def __init__(self):
        self.memtable = Memtable()
        pass

    def write_memtable_to_disk(self):
        """Writes memtable out to file on disk."""
        # does this belong here or in memtable
        pass

    def create_sparse_index(self):
        """Creates sparse index of compressed SSTable blocks."""
        # used when writing memtable to disk
        pass

    def create_log(self):
        """Creates unsorted log for use if db crashes and memtable lost."""
        pass

    def delete_log(self):
        """Removes current log."""
        pass

    def compact(self):
        """Merges several different SSTable files into one using mergesort."""
        pass
