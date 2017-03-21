#!/usr/bin/env python

# Symbol Table

class Table:
    def __init__(self, parent=None, name=None, category=None):
        self.entries = {}
        self.parent_table = parent
        self.name = name
        self.category = category

    def lookup(self, name):
        if name in self.entries:
            return True
        else:
            return False

    def lookup_all(self, name):
        current_table = self
        while(current_table != None):
            if current_table.lookup(name):
                return True
            current_table = current_table.parent_table
        return False

    def get_entry(self, name):
        if self.lookup(name):
            return self.entries[name]
        else:
            return None

    def get_method_entry(self, name):
        current_table = self
        while(current_table != None):
            if current_table.lookup(name):
                return current_table.entries[name]
            current_table = current_table.parent_table
        return None

    def insert(self, name, attributes={}):
        self.entries[name] = attributes
        return self.entries[name]

    def print_table(self):
        for key, value in self.entries.items():
            print("{}:\t\t{}".format(key,value))

class SymbolTable:

    def __init__(self):
        self.table = Table()
        self.classes = {}

    def begin_scope(self, name, category):
        new_table = Table(self.table, name, category)
        self.table = new_table
        return self.table

    def end_scope(self):
        self.table = self.table.parent_table

    def get_entry(self, name):
        return self.table.get_method_entry(name)

    def insert(self, name, attributes={}):
        return self.table.insert(name, attributes)

    def print_table(self):
        self.table.print_table()

    def insert_class(self, name):
        self.classes[name] = self.table

    def lookup_class(self, name):
        if name in self.classes:
            return True
        else:
            return False

    def lookup_method(self, name, method):
        if self.classes[name].lookup(method):
            return self.classes[name].entries[method]
        else:
            return None

    def insert_up(self, name, attributes={}):
        return self.table.parent_table.insert(name, attributes)

    def get_name(self):
        return (self.table.name, self.table.category)

    def get_method_return_type(self):
        current_table = self.table
        while(current_table != None):
            if current_table.category == "method":
                return current_table.parent_table.get_entry(current_table.name)['type'].split(" ", 1)[0]
            current_table = current_table.parent_table
        return None
