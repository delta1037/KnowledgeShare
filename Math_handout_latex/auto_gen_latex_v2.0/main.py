# author: delta1037
# Date: 2022/01/02
# mail:geniusrabbit@qq.com

import csv
import logging
import os.path
from configuration_service import ConfigurationService
import NotionDump
from NotionDump.Dump.database import Database
from NotionDump.Notion.Notion import NotionQuery

SUBSECTION_SPLIT_STR = "——————————————————————————\n"
SUBSECTION_SPLIT_STR_WITHOUT_N = "——————————————————————————"


class AutoGenLatex:
    def __init__(self, _query_handle: NotionQuery, _database_list, _classify_file, _col_name_dic, _output_dir):
        self.query_handle = _query_handle
        self.database_path = "./database/"
        if not os.path.exists(self.database_path):
            os.mkdir(self.database_path)
        self.database_list = _database_list
        self.col_name_dic = _col_name_dic
        self.classify_file = _classify_file
        self.output_dir = _output_dir
        self.csv_list = []
        self.col_name_list = []
        # print(self.col_name_dic)

    # 获取所有的数据库，下载成CSV的格式
    def __get_database(self):
        for item in self.col_name_dic:
            self.col_name_list.append(self.col_name_dic[item])

        for database in self.database_list:
            print("get database " + database)
            logging.log(logging.INFO, "get database " + database)
            output_file_name = self.database_path + database + ".csv"

            # 数据库操作句柄，这是个bug，把解析类型当作内部变量了，只能2了
            db_handle = Database(database_id=database, query_handle=self.query_handle, parser_type=2)
            # print("export col ", self.col_name_list)
            ret = db_handle.dump_to_file(file_name=output_file_name, col_name_list=self.col_name_list)
            if ret != "":
                logging.log(logging.INFO, "save csv file " + output_file_name)
                self.csv_list.append(output_file_name)

    # 读取csv格式文件成表格形式
    def __get_csv_src(self, csv_name):
        logging.log(logging.INFO, "read csv file " + csv_name)
        src_csv_file = open(csv_name, "r", encoding='UTF-8')
        reader = csv.reader(src_csv_file)

        res_table = []
        for item in reader:
            if reader.line_num == 1:
                continue
            item_construct = {}
            index = 0  # 行索引
            for i in self.col_name_list:
                item_construct[i] = item[index]
                index = index + 1
            res_table.append(item_construct)
        src_csv_file.close()
        return res_table

    # 读取输出分类格式
    @staticmethod
    def get_csv_classify(csv_name):
        classify_csv_file = open(csv_name, "r", encoding='UTF-8')
        reader = csv.reader(classify_csv_file)

        res_dic = {}
        for item in reader:
            res_dic[item[0]] = item[1]
        classify_csv_file.close()
        return res_dic

    # latex文件输出格式控制
    # 1、文件头内容
    @staticmethod
    def latex_head(handle, chapter):
        head = "\\chapterimage{chapter_head_2.pdf}\n\\chapter{%s}\n\n" % chapter
        # print(head)
        handle.write(head)

    # 2、章节头 section
    @staticmethod
    def latex_section(handle, topic):
        section = "\\section{%s}\\index{%s}\n\n" % (topic, topic)
        handle.write(section)
        handle.write("\n\n")

    # 2、章节头 section，只有单个内容的输出
    @staticmethod
    def latex_section_single(handle, topic, idea):
        section = "\\section{%s}\\index{%s}\n\n" % (topic, topic)
        handle.write(section)
        handle.write(idea.replace('\r', '').replace("\n", "\n\n"))
        handle.write("\n\n")

    # 2、章节头 section，section的注意事项
    @staticmethod
    def latex_section_attention(handle, idea):
        handle.write(idea.replace('\r', '').replace("\n", "\n\n"))
        handle.write("\n\n")

    # 3、子章节 subsection
    @staticmethod
    def latex_subsection(handle, topic, subtopic, idea):
        subsection = "\\subsection{%s}\\index{%s!%s}\n\n" % (subtopic, topic, subtopic)
        handle.write(subsection)
        handle.write(idea.replace('\r', '').replace("\n", "\n\n"))
        handle.write("\n\n")

    # 解析content的内容，分解成section和subsection
    def parser_content(self, handle, line):
        # 先解析line["topic", "ideas", "attributes", "chapter"]

        # 一行内有多个内容的先做分割
        if line[self.col_name_dic["content_col"]].find(SUBSECTION_SPLIT_STR) != -1:
            # 多个内容分解成subsection
            ideas_array = line[self.col_name_dic["content_col"]].split(SUBSECTION_SPLIT_STR)
            self.latex_section(handle=handle, topic=line[self.col_name_dic["section_col"]])
            for idea_raw in ideas_array:
                # 判断是否是注意事项或者备注
                if idea_raw[0:2] == "注意" or idea_raw[0:2] == "备注":
                    self.latex_section_attention(
                        handle=handle,
                        idea=idea_raw.replace(SUBSECTION_SPLIT_STR_WITHOUT_N, '')
                    )
                else:
                    # 对每一个idea解析出来subtopic
                    # print("############# idea_raw:" + idea_raw)
                    subtopic = idea_raw.split('\n')[0].strip(': ：')  # 获取到第一行内容，处理成subsection
                    idea = idea_raw[idea_raw.index('\n') + 1:]
                    # print("############# idea:" + idea)
                    self.latex_subsection(
                        handle=handle,
                        topic=line[self.col_name_dic["section_col"]],
                        subtopic=subtopic,
                        idea=idea.replace(SUBSECTION_SPLIT_STR_WITHOUT_N, '')
                    )
        else:
            # 单个内容直接输出
            self.latex_section_single(handle=handle,
                                      topic=line[self.col_name_dic["section_col"]],
                                      idea=line[self.col_name_dic["content_col"]].replace(SUBSECTION_SPLIT_STR_WITHOUT_N, '')
                                      )

    # 查找表格，按照指定的内容输出
    def output_latex(self, ideas_table):
        classify_dic = self.get_csv_classify(self.classify_file)
        # 遍历classify字典
        for item in classify_dic:
            # 获取到输出文件句柄
            output_file = classify_dic[item]
            file_handle = open(self.output_dir + "\\" + output_file, "w+", encoding='UTF-8')
            # 输出文件头
            self.latex_head(file_handle, item)
            # 遍历源table文件
            for line in ideas_table:
                # 过滤不属于本章节的内容，如果属于多个章节按照第一个算
                # print(line[self.col_name_dic["classify_col"]])
                chapter_name = line[self.col_name_dic["classify_col"]].split(',')[0]
                if chapter_name != item:
                    # print("not line ", chapter_name)
                    continue

                # 解析内容，并写入到文件中
                self.parser_content(file_handle, line)

            # 关闭文件
            file_handle.flush()
            file_handle.close()

    def auto_gen(self):
        # 获取所有的数据库
        self.__get_database()

        # 将CSV表格读入
        csv_table = []
        for file in self.csv_list:
            csv_table = csv_table + self.__get_csv_src(csv_name=file)
        print("笔记条目数", len(csv_table))

        # 送入解析
        self.output_latex(ideas_table=csv_table)


if __name__ == '__main__':
    config = ConfigurationService()
    input_dir = config.get_key("input_dir")
    classify_file = input_dir + "\\" + config.get_key("classify_file")

    # 合成输出路径
    root_dir = os.path.abspath(os.path.dirname(os.getcwd())) + "\\"
    output_path = root_dir + config.get_key("output_filename")
    print("output dir path: ", output_path)

    # 获取数据库需要输出的字段
    col_name_dic = config.get_key("request_format")
    if col_name_dic is None:
        logging.exception("request_format is NULL !!!")
        exit(-1)
    # 获取需要输出的数据库
    database_list = config.get_key("database_list")
    if len(database_list) == 0:
        logging.exception("no database to process !!!")
        exit(0)

    # 获取Notion查询句柄
    query_handle = NotionQuery(token=config.get_key("token"))
    if query_handle is None:
        logging.exception("query handle init error")
        exit(-1)

    print("Start parser...")
    gen_handle = AutoGenLatex(
        _query_handle=query_handle,
        _database_list=database_list,
        _classify_file=classify_file,
        _col_name_dic=col_name_dic,
        _output_dir=output_path,
    )
    gen_handle.auto_gen()
    print("End parser")
