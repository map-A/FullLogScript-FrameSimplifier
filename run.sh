#!/bin/sh
# 定义文件路径变量
base_path="D:\work\3DMark_CloudGate-orgSize-FixFPS0.5-GT1\\"
first_secene=53
save_secene=54
number=1
path1="${base_path}\\vector\\"
path2="${base_path}temp\\3DMarkICFWorkload_0.sdx"

# 使用变量执行命令
echo | python ./FrameSimplifier.py -s $path1 -f $first_secene -b $save_secene -n $number -m -1
find $path1 -name "*.inject" -type f -delete
# rm -rf $base_path/ReplayDump
# echo "injecting"
# ./qReplay/qReplay.exe -s $path2 --inject 3DMarkSkyDiver_Trim.inject --hide
echo "dumping frame"
./qReplay/qReplay.exe -s $path2 --dumpF --hide

# 完成以后，需要在_0.sdx文件修改引用的目录，添加 ; ..\ReplayDump\HW\
# 这个过程可能会很耗时，依据所simple的脚本帧数不同
# TrimDX.exe -s  D:\work\3DMark_FireStrike-orgSize-FixFPS0.5-GT2\vector -f 131 -l 13181