# FullLogScript-FrameSimplifier

## Description

简化0-n的脚本，使其更加简洁，易读，易用。
初始：0，1，2，3，n.sdx,
省去中间不显示图像的sdx
结果：0，1，2，3...

## Usage

``python main.py``

main.py的参数说明：

```
python .\FrameSimplifier.py -s D:\test\script\3dmark-org\3DMark_FireStrike-orgSize-FixFPS0.5-GT1\vector\ -f 112 -b 113 -n 1
```

默认保存在 `vector` 的同级目录frame下
-f 第一个有画面的索引
-b 想要dump的文件索引号
-n 想要dump几个
-m -1 保留所有Draw

简化之后，在Frame目录下有0.sdx和1.sdx 两个文件，0.sdx 没有包含resource目录，在该文件首行axdpath函数中添加“ReplayDump\HW”

最后用ExtractScriptResource 重新生成脚本目录，生成要为0和1都指定一下。命令为

```
./ExtractScriptResource.exe -s 0.sdx -o output_path
./ExtractScriptResource.exe -s 1.sdx -o output_path
```

打包成exe可执行文件

```
pyinstaller -F --console FrameSimplifier.py
```
