1 发现处理后的第0帧还有几百个draw。

2 第一帧不是原始的文件完全一样（拷贝后重命名），好像空行被删除了，这样简化后的脚本跟原始脚本的draw的行号就对应不上了，而这个行号在我们后续使用中是需要的。:ballot_box_with_check:

3 相同路径对多个frame分别进行简化时，文件名没有区分冲突了。:ballot_box_with_check:
可以按下面这样做区分：
原始未简化前的文件名：3DMarkICFWorkload_0.sdx   ......  3DMarkICFWorkload_55.sdx......
简化F55的1帧的文件名：3DMarkICFWorkload_F55_0.sdx, 3DMarkICFWorkload_F55_1.sdx,
简化F56的2帧的文件名：3DMarkICFWorkload_F56_0.sdx, 3DMarkICFWorkload_F56_1.sdx, 3DMarkICFWorkload_F56_2.sdx
这样就不会冲突了。
4 要设置3个目录，操作稍微繁杂。:ballot_box_with_check:
tmp_path不用设，工具自己创建并使用后删除。
target_path可以设，不设置的话有默认值，如下：
.\vector\      //比如要简化的目录路径名
.\frame\      //默认自动在vector同级目录创建一个frame目录保存简化后的script文件。
5 ini里边这几个怎么用 :ballot_box_with_check:
scene_begins_index需要设置吗？什么功能？怎么用？
start_draw_index什么功能？怎么用？

答：见readme.md 文件

6 工具名字改为FrameSimplifier.exe  :ballot_box_with_check: 
7 能否支持命令行参数，方便批量处理，比如
FrameSimplifier.exe -s  D:\3DMark\3DMark_CloudGate-orgSize-FixFPS0.5-GT1\vector\3DMarkICFWorkload_0.sdx     55   3
意思是简化这个脚本的第55帧，连续3帧，生成的脚本默认保存到D:\1-ScriptDX\Performance-Script\3DMark\3DMark_CloudGate-orgSize-FixFPS0.5-GT1\frame\中。 :ballot_box_with_check:
8 参考TrimDX看看简化的脚本是否有冗余，有冗余的话修改工具去掉冗余。
一个方法是阅读简化后的3DMarkICFWorkload_F55_0.sdx看是否有冗余。
另外一个方法是借用TrimDX，比如简化原始的F55, 用TrimDX简化F55的第一个draw，得到一个单个draw的简化脚本。
修改原始F55脚本，把第一个draw后面的全部删除，保留最后的present，当成一帧只有1个draw，
然后用FrameSimplifier.exe把它当作一帧来简化，对比简化出来的脚本和TrimDX简化出来的脚本，查查看有没有冗余或者错误。

9 帮忙把NAS /SW/Perf_Scripts/3DMark-Org/中的全部脚本都简化一下；
简化后仅仅把frame目录压缩打包放到NAS同级目录，比如：
3DMark_CloudGate-orgSize-FixFPS0.5-GT1.zip
3DMark_CloudGate-orgSize-FixFPS0.5-GT1_TrimFrame.zip     //frame目录打包命名在原文件名基础上加上_TrimFrame。
简化目标为：
所有有画面的帧的单帧简化，和一个包括所有的有画面帧的连续帧简化
比如说3DMark_CloudGate-orgSize-FixFPS0.5-GT1其中53到66是有画面的。
FrameSimplifier.exe -s   ​*******   53   1
FrameSimplifier.exe -s   ​*******   54   1
FrameSimplifier.exe -s   ​*******   55   1
FrameSimplifier.exe -s   ​*******   56   1
FrameSimplifier.exe -s   ​*******   57   1
FrameSimplifier.exe -s   ​*******   58   1
FrameSimplifier.exe -s   ​*******   59   1
FrameSimplifier.exe -s   ​*******   60   1
FrameSimplifier.exe -s   ​*******   61   1
FrameSimplifier.exe -s   ​*******   62   1
FrameSimplifier.exe -s   ​*******   63   1
FrameSimplifier.exe -s   ​*******   64   1
FrameSimplifier.exe -s   ​*******   65   1
FrameSimplifier.exe -s   ​*******   66   1
FrameSimplifier.exe -s   ​*******   53   14
上面的*******指的是fulllog原始脚本的第0帧，即D:\3DMark\3DMark_CloudGate-orgSize-FixFPS0.5-GT1\vector\3DMarkICFWorkload_0.sdx