# 笔记生成

# 一、环境配置

### 1.1 python

网上很多教程，装一下就行了，可以在`powershell`中执行`py -V`看一下版本信息

### 1.2 配置文件

配置文件名为`config.json`，内容为

```json
{
    "input_dir" : "input",
    "classify_file": "classify_dic.csv",
    "handout_file": [
        "handout_0.csv",
        "handout_1.csv",
        "handout_2.csv",
        "handout_3.csv"
    ],
    "csv_src_format": [
        "topic",
        "ideas",
        "chapter"],
    "output_filename": "sub_chapter"
}
```

-   input_dir：源文件目录文件夹（包括分类文件和手动导出的CSV文件）
-   classify_file：分类文件（见1.3解释）
-   handout_file：手动导出的CSV文件列表，与input文件夹中的文件名一致
-   csv_src_format：CSV文件的列格式，必须包含`["topic","ideas","chapter"]`，其中topic是用来生成标题的列，ideas是内容列，chapter是分章节的列
-   output_filename：生成的latex文件目录（相对于当前目录上一级目录）

## 1.3 分类文件

用记事本打开`classify_dic.csv`，逗号前边是数据库中的分类名，逗号后边是输出文件名

```
函数极限连续,01-func_lim.tex
一元微分,02-differential.tex
多元微分,03-differential_multi.tex
一元积分,04-integral.tex
多元积分,05-integral_multi.tex
向量代数与空间几何,06-vector_algebra.tex
无穷级数,07-series.tex
常微分方程,08-differential_equation.tex
微积分通识,09-general.tex
行列式,11-determinant.tex
```

## 二、执行

在`powershell`中执行`py main.py`即可，生成好的文件会输出到配置中`output_filename`所指定的目录中

