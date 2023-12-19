#!/bin/sh
# # 定义文件路径变量
base_path="D:\\work\\dx11\\3DMark_FireStrike-orgSize-FixFPS0.5-GT2\\"
first_secene=142
save_secene=145
number=1
output_path="D:\\work\\dx11\\3DMark_FireStrike-orgSize-FixFPS0.5-GT2\\output\\"



simple_nums=1

cp .\\pBuf_for_dispatch.bin $base_path\\data\\
for (( i=1; i<=$simple_nums; i++ )); do
    echo $save_secene
    # 使用变量执行命令
    echo | python ./main.py -s $base_path -f $first_secene -b $save_secene -n $number
    save_secene=$((save_secene+1))
done

filename=$(find $base_path"frames\\" -name "*_0.sdx" -type f)
sed -i '2s#axPath(Path = "..\\data\\; ..\\shader\\; ..\\LogDump\\");#axPath(Path = "..\\data\\; ..\\shader\\; ..\\LogDump\\;..\\ReplayDump\\HW\\");#' $filename

rm -rf $base_path\\temp\\
rm -rf $base_path\\refactor\\
find ${base_path}vector\\ -name "*.inject" -type f -delete


files=($(ls "$base_path\\frames\\"))

# 遍历文件列表
for file in "${files[@]}"; do
    extract_cmd=".\\ExtractScriptResource.exe -s ${base_path}frames\\${file} -o $output_path"
    $extract_cmd > /dev/null 2>&1
done
rm -rf $base_path\\frames\\

echo "finish simplify"