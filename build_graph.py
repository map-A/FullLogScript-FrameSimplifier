from tool_function import *
from graph import *

# 使用解析好的资源构建链表或者图
# 首先是设计图的节点类的结构，然后是边的关系，最后是图的结构
# 读取一个文件，解析每一行，判断每一行语句的种类，然后进行处理
# 1. 读取文件
# 2. 解析每一行
# 3. 判断语句种类
# 4. 处理语句
graph = Graph()
filename = r"output\3DMarkICFWorkload_58.sdx";
line_pos = 0
with open(filename, "r") as f:
    for line in f:
        if is_comment(line):
            pass
        elif is_empty(line):
            pass
        elif is_other(line):
            res = parse_statement(line)
            node = Node(res[1],[filename,line_pos])
            # node.print()
            graph.add_vertex(node)
        elif is_object_func_call(line):
            print(parse_object_func_call(line))
        elif is_func_call(line):
            print(line_pos,parse_func_call(line))
        
        line_pos = line_pos+1
# graph.print_vertices()
# graph.print()