# 笔记生成

# 一、环境配置

### 1.1 python

网上很多教程，装一下就行了，可以在`powershell`中执行`py -V`看一下版本信息

### 1.2 配置文件

配置文件名为`config.json`，内容为

```json
{
    "token": "secret_Hexxxxxxxxxxxxxxxxxxx",
    "input_dir" : "input",
    "classify_file": "classify_dic.csv",
    "request_format": {
        "section_col" : "题目",
        "content_col" : "思路",
        "classify_col" : "章节"
    },
    "database_list": [
        "c98ddf9781cf4108bcb5c1c992d4fdf9",
        "c667ae985d384e4eb57bae50e7e2d030",
        "90f8890d9c8641eca4377678484204bd",
        "13e4650ace214206994df403ab803ffb"
    ],
    "output_filename": "sub_chapter"
}
```

-   token：notion官方API token
-   input_dir：分类文件所在目录
-   classify_file：分类文件（见1.3解释）
-   request_format：需要的列，其中section_col是用来生成标题的列，content_col是内容列，classify_col是分章节的列，后边是在具体的数据库中列的名字
-   database_list：是需要导出的数据库ID
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

