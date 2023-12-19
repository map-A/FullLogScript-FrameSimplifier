# FullLogScript-FrameSimplifier

## Description

简化0-n的脚本，使其更加简洁，易读，易用。
初始有脚本：0，1，2，3，n.sdx,在某一帧 `i`开始显示画面，现在直接想提取帧 `i`，省去中间sdx文件
结果：生成两个sdx文件，0.sdx 文件，1.sdx 文件

## Dependency

项目依赖于qReplay,trimdx,来dump数据，ExtractScriptResource.exe，请将这三个可执行文件放在同级目录下。

-qReplay\qreplay.exe

-ExtractScriptResource.exe

-Trimdx.exe

## Usage

``python main.py``

main.py的参数说明：

```
python .\FrameSimplifier.py -s D:\test\script\3dmark-org\3DMark_FireStrike-orgSize-FixFPS0.5-GT1\vector\ -f 112 -b 113 -n 1
```

简化结果默认保存在 `vector` 的同级目录frame下
-f 第一个有画面的索引，比如112 表示这个脚本集从112.sdx 开始显示画面的
-b 想要dump的文件索引号，113表示我们想从113.sdx 开始提取
-n ，1 表示从113.sdx 提取几个sdx

简化之后，在frame目录下有0.sdx 和1-n.sdx两种文件。0.sdx 文件是跑脚本前的数据准备工作，1-n是每一帧画面。

0.sdx 文件没有包含resource目录，请在文件的首行的axdpath函数中添加“ReplayDump\HW”

最后用ExtractScriptResource 重新生成脚本目录，为每一个sdx都指定重新生成一下。如命令为

```
./ExtractScriptResource.exe -s 0.sdx -o output_path
./ExtractScriptResource.exe -s 1.sdx -o output_path
```

打包成exe可执行文件，后续可以用exe可执行文件代替项目。

```
pyinstaller -F --console main.py
```

## bash一键运行

提供了bash脚本 `run.sh`。

`run.sh`需要指定简化脚本目录和一些参数来运行。修改好参数后，执行bash run.sh 即可在设置目录找到简化后的脚本。
