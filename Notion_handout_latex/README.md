# 编译指南

# 一、Latex安装

### 1.1 主程序

网上很多教程，装一下就行了

### 1.2 安装zhmakeindex

[下载地址](https://iso.mirrors.ustc.edu.cn/CTAN/indexing/zhmakeindex.zip)

解压后，将`zhmakeindex\bin\windows_x86`目录下的主程序放在latex的安装位置的`bin`目录（和`makeindex.exe`是同一个路径）



## 二、编译

### 2.1 步骤

```powershell
# 第一步
xelatex main

# 第二步
zhmakeindex -s styleidx.ist main.idx

# 第三步
xelatex main x 2
```



### 2.2 说明

-   模板和内容都是整理好的，下载配置好环境即可编译



## 三、修改说明

### 3.1 笔记文件处理

笔记源文件是从notion上导出的`csv`文件，经过脚本处理之后生成了`sub_chapter`中的各个章节

如果在notion中修改了笔记的内容，可以参考`auto_gen_latex_v1.0`下的`README.md`文件，重新生成各个章节

