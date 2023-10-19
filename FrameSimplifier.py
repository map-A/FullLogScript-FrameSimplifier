from tool_function import *
from graph import *
from build_graph import *
from write_new_file import *
import configparser
import sys
import os
import subprocess
import argparse
if __name__ == "__main__":
    src_path = ""
    scene_begins_index= 1
    save_start_index = 1
    numbers_to_simple = 1
    offset = 0


    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--src_path',required=True,help='src script path')
    parser.add_argument('-f','--first_scene_number',required=True,type=int,help="the first scene present number")
    parser.add_argument('-b', '--begin',required=True,type=int,help='Begining Simplified Script Sequence Number')
    parser.add_argument('-n', '--numbers_to_simple',required=False,type=int,default=1, help='number consecutive frames')
    parser.add_argument('-m', '--magic_number',required=False,type=int,default=-1, help='i donnot know how to set it, it better set over 17,when it set -1,it work without wrong,but simple script\
                        will be larger, when is set over than -1,script will be small ,but it might work wrong')
    args = parser.parse_args()
    if(args):
        src_path = args.src_path
        scene_begins_index = args.first_scene_number
        save_start_index = args.begin
        numbers_to_simple = args.numbers_to_simple
        offset = args.magic_number
    else:
    

        config = configparser.ConfigParser()
        config.read('config.ini', encoding='utf-8') 
        # 尝试不同编码转换直到不报错
        # 尝试utf-8解码
        scene_begins_index= int(config['frame_index']['scene_begins_index'])
        save_start_index = int(config['frame_index']['save_start_index'])
        numbers_to_simple = int(config['frame_index']['n'])
        src_path = config['path']['src_path']
        offset  = config['frame_index']['magic_number']
    
    save_end_index = save_start_index+numbers_to_simple-1


    tmp_path = os.path.dirname(os.path.dirname(src_path)) +r"\\temp\\" # 新的src path，原有的变成origin_path
    target_path = os.path.dirname(os.path.dirname(src_path)) +r"\frames\\"
    
    trim_files(src_path,tmp_path)

    graph = Graph()
    nodelist = NodeLists()
    mapstack = MapStack()
    drawvector = DrawVector()

    
    file_list = read_dir(tmp_path)
    inject_file = file_list[0].replace('_0.sdx','_Trim.inject')
    for filename in file_list:
        read_to_graph(tmp_path+filename,graph,nodelist,mapstack)        
        read_to_draw_vector(tmp_path+filename,drawvector)
        """
        在最后需要trim的帧之前的所有改动dump到inject文件中
        inject文件中的语句最后需要添加到trim的帧之前
        """
        generate_inject_file(tmp_path+filename,src_path+inject_file,graph)
   
    simplify_frames(graph,nodelist,drawvector,src_path,tmp_path,target_path,scene_begins_index,save_start_index,save_end_index,offset)
    
    generate_final_inject_file(src_path+inject_file,tmp_path+inject_file,save_start_index)


    # #./qReplay/qReplay.exe -s D:/work/3DMark_SkyDiver-orgSize-FixFPS0.5-gt1/temp/3DMarkSkyDiver_0.sdx --inject 3DMarkSkyDiver_Trim.inject
    cmd = r".\\qReplay\\qReplay.exe -s "+ r"D:\\work\\3DMark_FireStrike-Extreme-orgSize-FixFPS0.5-GT2\\temp\\"+file_list[0]+" --inject "+ inject_file+ " --hide"
    print(cmd)
    p1 = subprocess.Popen(cmd, shell=True)
    p1.wait()

    new_filename_0 = re.sub(r'(\d+)\.sdx$',"F"+str(save_start_index)+'_0'+".sdx", file_list[0])
    upload_files(tmp_path,target_path,new_filename_0,inject_file)
    
    
    

    print("simplify success")
    input("Press enter to exit...")
    sys.exit()
