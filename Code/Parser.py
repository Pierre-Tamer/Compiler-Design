from Code.Tree_node import Tree_node
from Code import Util


class Parser:

    def __init__(self):
        self.tokens = []
        self.iterator = 0
        self.Nodes = []
        self.Parents = []
        self.Parents.append(0)
        self.error = False
        self.current_node_id = 1
        self.connect_Parent = True
        self.nested_op = 0
        self.nested_parents_to_pop = 0
        self.nested_conditions = 0

    def match(self, expectedtoken):
        if (self.tokens[self.iterator][0] == expectedtoken) or (self.tokens[self.iterator][1] == expectedtoken):
            self.iterator += 1
        else:
            raise ValueError()

    def program(self):
        self.stmtsequence()
        if self.iterator < len(self.tokens) or self.nested_conditions > 0:
            raise ValueError()

    def stmtsequence(self):

        self.connect_Parent = True
        self.statment()

        while self.iterator < len(self.tokens) and self.tokens[self.iterator][0] == ';':

            self.connect_Parent = False
            self.match(";")
            if self.iterator >= len(self.tokens):
                raise ValueError()
            self.statment()


    def statment(self):

        if len(self.tokens):
            newnode = Tree_node(self.tokens[self.iterator][0], self.current_node_id, self.Parents[-1])
            newnode.connect_Parent = self.connect_Parent
            self.Nodes.append(newnode)
            self.current_node_id = newnode.get_id() + 1
            self.Parents.append(newnode.get_id())
            if self.tokens[self.iterator][0] == "if":
                ret = self.if_stmt()
                ret.parent_id = newnode.get_id()
                self.Parents.pop()
            elif self.tokens[self.iterator][0] == "repeat":
                self.repeat_stmt()
                self.Parents.pop()
            elif self.tokens[self.iterator][0] == "read":
                self.read_stmt()
                self.Parents.pop()
            elif self.tokens[self.iterator][0] == "write":
                ret = self.write_stmt()
                ret.parent_id = newnode.get_id()
                self.Parents.pop()
            else:
                self.Nodes[-1].value = "assign\n(" + self.tokens[self.iterator][0] + ")"
                ret = self.assign_stmt()
                ret.parent_id = newnode.get_id()
                self.Parents.pop()
            return newnode

    def if_stmt(self):
        self.nested_conditions+=1
        self.match("if")
        ret = self.exp()
        self.match("then")
        self.stmtsequence()
        if self.iterator < len(self.tokens):
            if self.tokens[self.iterator][0] == "else":
                self.match("else")
                self.stmtsequence()
            self.match("end")
            self.nested_conditions-=1
        return ret

    def repeat_stmt(self):

        self.match("repeat")
        self.stmtsequence()
        self.match("until")
        self.exp()

    def read_stmt(self):

        self.match("read")
        self.Nodes[-1].value = "read\n(" + self.tokens[self.iterator][0] + ")"
        self.match("IDENTIFIER")

    def write_stmt(self):
        self.match("write")
        if (not (self.tokens[self.iterator][1] == "IDENTIFIER" or
                 self.tokens[self.iterator][1] == "NUMBER" or self.tokens[self.iterator][0] == '(')):
            raise ValueError()


        return self.exp()

    def assign_stmt(self):
        self.match("IDENTIFIER")
        self.match(":=")
        return self.exp()


    def exp(self): # x > 5
        e1 = self.simple_exp()
        represent = e1
        self.nested_op = 0
        if self.iterator < len(self.tokens):
            if self.tokens[self.iterator][0] == "<" or self.tokens[self.iterator][0] == "=" or self.tokens[self.iterator][0] == ">":
                op = self.comparison_exp()
                e2 = self.simple_exp()
                e1.parent_id = op.get_id()
                e2.parent_id = op.get_id()
                represent = op
                self.Parents.pop()
        return represent
#to be understood
    def simple_exp(self):

        c1 = self.term()
        p = c1
        while ((self.iterator < len(self.tokens)) and (
                self.tokens[self.iterator][0] == "+" or self.tokens[self.iterator][0] == "-")):
            p = self.addop()
            c2 = self.term()

            c1.parent_id = p.get_id()
            c2.parent_id = p.get_id()
            c1 = p
            self.nested_parents_to_pop += 1
            if self.iterator < len(self.tokens):

                if (self.tokens[self.iterator][0] == "+" or self.tokens[self.iterator][0] == "-" or
                        self.tokens[self.iterator][0] == "*" or self.tokens[self.iterator][0] == "/"):
                    self.nested_op += 1
                else:
                    self.nested_op = 0

        while self.nested_parents_to_pop > 0 and self.nested_op == 0:
            self.Parents.pop()
            self.nested_parents_to_pop -= 1
        return p

    def comparison_exp(self):

        newnode = Tree_node("Op\n(" + self.tokens[self.iterator][0] + ")", self.current_node_id, self.Parents[-1])
        self.Nodes.append(newnode)
        self.Parents.append(newnode.get_id())
        self.current_node_id = newnode.get_id() + 1
        if self.tokens[self.iterator][0] == "<":

            if Util.check_left(self.tokens, self.iterator) and Util.check_right(self.tokens, self.iterator):
                self.match("<")
            else:
                raise ValueError()

        elif self.tokens[self.iterator][0] == "=":

            if Util.check_left(self.tokens, self.iterator) and Util.check_right(self.tokens, self.iterator):
                self.match("=")
            else:
                raise ValueError()

        elif self.tokens[self.iterator][0] == ">":

            if Util.check_left(self.tokens, self.iterator) and Util.check_right(self.tokens, self.iterator):
                self.match(">")
            else:
                raise ValueError()
        return newnode

    def addop(self):

        newnode = Tree_node("Op\n(" + self.tokens[self.iterator][0] + ")", self.current_node_id, self.Parents[-1])
        self.Nodes.append(newnode)
        self.Parents.append(newnode.get_id())

        self.current_node_id = newnode.get_id() + 1

        if self.tokens[self.iterator][0] == "+":
            if Util.check_left(self.tokens, self.iterator) and Util.check_right(self.tokens, self.iterator):
                self.match("+")
            else:
                raise ValueError()

        elif self.tokens[self.iterator][0] == "-":
            if Util.check_left(self.tokens, self.iterator) and Util.check_right(self.tokens, self.iterator):
                self.match("-")
            else:
                raise ValueError()
        return newnode

    def term(self): # 6 / 3 * 2

        f1 = self.factor()
        represent = f1
        while ((self.iterator < len(self.tokens)) and (
                self.tokens[self.iterator][0] == "*" or self.tokens[self.iterator][0] == "/")):
            represent = self.mulop()
            f2 = self.factor()
            f1.parent_id = represent.get_id()
            f2.parent_id = represent.get_id()
            f1 = represent

            self.nested_parents_to_pop += 1
            if self.iterator < len(self.tokens):

                if (self.tokens[self.iterator][0] == "*" or self.tokens[self.iterator][0] == "/" or
                        self.tokens[self.iterator][0] == "+" or self.tokens[self.iterator][0] == "-"):
                    self.nested_op += 1
                else:
                    self.nested_op = 0

        while self.nested_parents_to_pop > 0 and self.nested_op == 0:
            self.Parents.pop()
            self.nested_parents_to_pop -= 1

        return represent

    def mulop(self):

        newnode = Tree_node("Op\n(" + self.tokens[self.iterator][0] + ")", self.current_node_id, self.Parents[-1])
        self.Nodes.append(newnode)
        self.Parents.append(newnode.get_id())
        represent = newnode
        self.current_node_id = newnode.get_id() + 1
        if self.tokens[self.iterator][0] == "*":
            if Util.check_left(self.tokens, self.iterator) and Util.check_right(self.tokens, self.iterator):
                self.match("*")
            else:
                raise ValueError()
        elif self.tokens[self.iterator][0] == "/":
            if Util.check_left(self.tokens, self.iterator) and Util.check_right(self.tokens, self.iterator):
                self.match("/")
            else:
                raise ValueError()
        return represent

    def factor(self):

        if self.iterator < len(self.tokens):

            if self.tokens[self.iterator][0] == "(":
                self.match("(")
                represent = self.exp()
                self.match(")")
                return represent
            elif self.tokens[self.iterator][1] == "NUMBER":
                newnode = Tree_node("const\n(" + self.tokens[self.iterator][0] + ")", self.current_node_id,
                                    self.Parents[-1])

                self.Nodes.append(newnode)
                self.current_node_id = newnode.get_id() + 1
                self.match("NUMBER")
                represent = newnode
                return represent
            elif self.tokens[self.iterator][1] == "IDENTIFIER":
                newnode = Tree_node("Identifier\n(" + self.tokens[self.iterator][0] + ")", self.current_node_id,
                                    self.Parents[-1])
                represent = newnode
                self.Nodes.append(newnode)
                self.current_node_id = newnode.get_id() + 1
                self.match("IDENTIFIER")
                return represent
        return Tree_node("Op\n(" + self.tokens[self.iterator][0] + ")", 0, self.Parents[-1])
