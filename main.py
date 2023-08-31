from tool_function import *
from graph import *
from build_graph import *
from write_new_file import *


start_draw_index=968
first_frame_index=49

src_path = r"vector\\"
tmp_path = "output\\"
target_path = "test-script\\"

if __name__ == "__main__":
    
    trim_files(src_path,tmp_path)

    graph = Graph()
    nodelist = NodeLists()
    mapstack = MapStack()
    drawvector = DrawVector()

    folder_path = r'output\\'
    file_list = read_dir(folder_path)
    for filename in file_list:
        read_to_graph(folder_path+filename,graph,nodelist,mapstack)
        
        read_to_draw_vector(folder_path+filename,drawvector)

    simplify_one_frame(graph,nodelist,drawvector,tmp_path,first_frame_index,target_path,start_draw_index)
