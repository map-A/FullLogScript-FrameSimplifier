#!/bin/sh
# 定义文件路径变量
base_path="D:\\work\\3DMark_FireStrike-orgSize-FixFPS0.5-GT1\\"
first_secene=112
save_secene=119
number=1


# echo "dumping frame"
# ./qReplay/qReplay.exe -s $path2 --dumpF --hide
# mv $base_path\\ReplayDump\\ $base_path\\Frame_dump_origin\\

simple_nums=1
for (( i=1; i<=$simple_nums; i++ )); do
    echo $save_secene
    # 使用变量执行命令
    echo | python ./FrameSimplifier.py -s $base_path -f $first_secene -b $save_secene -n $number

    mv $base_path\\frames\\ $base_path\\vector-F$save_secene\\
    
    mv $base_path\\ReplayDump\\ $base_path\\ReplayDump-F$save_secene\\
    
    sed -i '2s#axPath(Path = "..\\data\\; ..\\shader\\; ..\\LogDump\\");#axPath(Path = "..\\data\\; ..\\shader\\; ..\\LogDump\\;..\\ReplayDump-F'"$save_secene"'\\HW\\");#' $base_path\\vector-F$save_secene\\3DMarkICFWorkload_F${save_secene}_0.sdx

    find $base_path\\vector\\ -name "*.inject" -type f -delete
    # rm -rf $base_path\\temp\\
    save_secene=$((save_secene+1))
done

# echo "injecting"
# ./qReplay/qReplay.exe -s $path2 --inject 3DMarkSkyDiver_Trim.inject --hide
# echo "dumping frame"
# ./qReplay/qReplay.exe -s $path2 --dumpF --hide

# 完成以后，需要在_0.sdx文件修改引用的目录，添加 ; ..\ReplayDump\HW\
# 这个过程可能会很耗时，依据所simple的脚本帧数不同
# TrimDX.exe -s  D:\work\3DMark_FireStrike-orgSize-FixFPS0.5-GT2\vector -f 131 -l 13181