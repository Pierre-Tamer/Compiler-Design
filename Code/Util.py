import os
from graphviz import Graph

def is_str(token):
    return token.isalpha()


def is_num(token):
    return token.isdigit()


def is_col(c):
    return True if c == ':' else False


def is_symbol(token):
    symbol = ['+', '-', '*', '/', '=', '<', '>', '(', ')', ';']
    return True if token in symbol else False


def is_comment(token):
    if token[0] == '{' or token[-1] == '}':
        return True
    else:
        return False


def is_statment(Node):
    statment = ["if", "repeat", "assign", "read", "write"]
    str = Node.value.split("\n")
    for token in str:
        if token in statment:
            return True
        return False


def check_left(tokens, it):
    if not (tokens[it - 1][1] == "IDENTIFIER" or tokens[it - 1][1] == "NUMBER" or tokens[it - 1][0] == ')'):
        return False
    else:
        return True


def check_right(tokens, it):
    if not (tokens[it + 1][1] == "IDENTIFIER" or tokens[it + 1][1] == "NUMBER" or tokens[it + 1][0] == '('):
        return False
    else:
        return True


def get_file_text(file_name):
    with open(file_name, 'r') as f:
        input_text = f.read()
        input_text = input_text.replace('\n', ' ')
        input_text += ' '
        return input_text


def generate_Parse_Tree(Nodes):
    parse_tree = Graph(comment='Parse Tree', format='png', graph_attr={'bgcolor': '#b4bcbd', 'width': '500', 'margin': '0.5'}, node_attr={'fontname': 'Poppins', 'fontsize': '30', 'fontcolor': '#b4bcbd', 'fontweight': '800'})  
    home_directory = os.path.expanduser('~')  
    output_path = os.path.join(home_directory, 'Parse-Tree.gv') 

    for Node in Nodes:
        if is_statment(Node):
            parse_tree.node(str(Node.id), Node.value, shape='square', color='#1f292f', fontcolor='#b4bcbd', style="filled")
        elif Node.id % 2 == 0:  # Use a different shape for alternate nodes
            parse_tree.node(str(Node.id), Node.value, shape='circle', color='#d94d04', fontcolor='#1f292f', style='filled')
        else:
            parse_tree.node(str(Node.id), Node.value, shape='diamond', color='#d94d04', fontcolor='#1f292f', style='filled')

    for Node in Nodes:
        if (Node.parent_id != 0) and Node.connect_Parent:
            parse_tree.edge(str(Node.parent_id), str(Node.id))

        elif Node.parent_id != 0:
            parse_tree.edge(str(Node.parent_id), str(Node.id), color='black')

    for i in range(len(Nodes)):
        for j in range(i + 1, len(Nodes)):
            if ((Nodes[i].parent_id == Nodes[j].parent_id) and (not Nodes[j].connect_Parent) and
                    is_statment(Nodes[j]) and (is_statment(Nodes[i]))):
                parse_tree.edge(str(Nodes[i].id), str(Nodes[j].id), constraint='false')
                break

            elif ((Nodes[i].parent_id == Nodes[j].parent_id) and Nodes[j].connect_Parent and
                  is_statment(Nodes[j]) and (is_statment(Nodes[i]))):
                break

    parse_tree.render(output_path, view=True) 

    return



