# author: delta1037
# Date: 2022/01/08
# mail:geniusrabbit@qq.com
import logging


class BlockParser:
    def __init__(self, block_id):
        self.block_id = block_id

    # 讲Text块，Json格式获取到纯文本(去除格式)
    def __text_plain(self, block_handle):
        if block_handle["type"] != "text":
            logging.exception("text type error! id=" + self.block_id)
            print(block_handle)
            return ""
        text_str = block_handle["plain_text"]
        return text_str

    def __user_plain(self, block_handle):
        if block_handle["object"] != "user":
            logging.exception("user type error! id=" + self.block_id)
            return ""
        user_id = block_handle["id"]
        return user_id

    def __file_plain(self, block_handle):
        if block_handle["type"] != "file":
            logging.exception("file type error! id=" + self.block_id)
            return ""
        filename = block_handle["name"]
        file_url = block_handle["file"]["url"]
        # 格式处理简单格式（也可以转换成markdown格式[]()）
        return filename + "|" + file_url

    # "$ equation_inline $"
    def __equation_inline_plain(self, block_handle):
        if block_handle["type"] != "equation":
            logging.exception("equation inline type error! id=" + self.block_id)
            return ""
        eq_str = "$" + block_handle["plain_text"] + "$"
        return eq_str

    # "$$ equation_inline $$"
    def __equation_block_plain(self, block_handle):
        if block_handle["type"] != "equation":
            logging.exception("equation block type error! id=" + self.block_id)
            return ""
        eq_str = "$$" + block_handle["plain_text"] + "$$"
        return eq_str

    def title_plain(self, block_handle):
        if block_handle["type"] != "title":
            logging.exception("title type error! id=" + self.block_id)
            return ""
        title_list = block_handle["title"]
        ret_str = ""
        if title_list is None:
            return ret_str
        for title in title_list:
            if title["type"] == "text":
                ret_str += self.__text_plain(title)
            elif title["type"] == "equation":
                ret_str += self.__equation_inline_plain(title)
        return ret_str

    def rich_text_plain(self, block_handle):
        if block_handle["type"] != "rich_text":
            logging.exception("rich_text type error! id=" + self.block_id)
            return ""
        rich_list = block_handle["rich_text"]
        ret_str = ""
        if rich_list is None:
            return ret_str
        for block in rich_list:
            block_type = block["type"]
            if block_type == "text":
                ret_str += self.__text_plain(block)
            elif block_type == "equation":
                ret_str += self.__equation_inline_plain(block)
            else:
                logging.exception("unknown block type:" + block_type)
        return ret_str

    def multi_select_plain(self, block_handle):
        if block_handle["type"] != "multi_select":
            logging.exception("multi_select type error! id=" + self.block_id)
            return ""
        multi_select_list = block_handle["multi_select"]
        ret_str = ""
        if multi_select_list is None:
            return ret_str
        for multi_select in multi_select_list:
            if ret_str != "":
                ret_str += ","  # 多个选项之间用“,”分割
            ret_str += multi_select["name"]
        return ret_str

    def select_plain(self, block_handle):
        if block_handle["type"] != "select":
            logging.exception("select type error! id=" + self.block_id)
            return ""
        select = block_handle["select"]
        ret_str = ""
        if select is None:
            return ret_str
        ret_str = select["name"]
        return ret_str

    def url_plain(self, block_handle):
        if block_handle["type"] != "url":
            logging.exception("url type error! id=" + self.block_id)
            return ""
        url = block_handle["url"]
        # print(url)
        ret_str = ""
        if url is not None:
            ret_str = url
        return ret_str

    def email_plain(self, block_handle):
        if block_handle["type"] != "email":
            logging.exception("email type error! id=" + self.block_id)
            return ""
        email = block_handle["email"]
        # print(email)
        ret_str = ""
        if email is not None:
            ret_str = email
        return ret_str

    def checkbox_plain(self, block_handle):
        if block_handle["type"] != "checkbox":
            logging.exception("checkbox type error! id=" + self.block_id)
            return ""
        checkbox = block_handle["checkbox"]
        # print(email)
        ret_str = ""
        if checkbox is True:
            ret_str = "true"
        else:
            ret_str = "false"
        return ret_str

    def phone_number_plain(self, block_handle):
        if block_handle["type"] != "phone_number":
            logging.exception("phone_number type error! id=" + self.block_id)
            return ""
        phone_number = block_handle["phone_number"]
        # print(email)
        ret_str = ""
        if phone_number is not None:
            ret_str = phone_number
        return ret_str

    def date_plain(self, block_handle):
        if block_handle["type"] != "date":
            logging.exception("date type error! id=" + self.block_id)
            return ""
        date = block_handle["date"]
        # print(date)
        ret_str = ""
        if date is None:
            return ret_str

        if date["start"] is not None:
            ret_str = date["start"]
        if date["end"] is not None:
            ret_str += " ~ " + date["end"]  # 日期之间用“~”分割
        return ret_str

    def people_plain(self, block_handle):
        if block_handle["type"] != "people":
            logging.exception("people type error! id=" + self.block_id)
            return ""
        people_list = block_handle["people"]
        ret_str = ""
        if people_list is None:
            return ret_str
        for people in people_list:
            if ret_str != "":
                ret_str += ","  # 多个用户之间用“,”分割
            ret_str += self.__user_plain(people)
        return ret_str

    def number_plain(self, block_handle):
        if block_handle["type"] != "number":
            logging.exception("number type error! id=" + self.block_id)
            return ""
        number = block_handle["number"]
        ret_str = ""
        if number is None:
            return ret_str
        ret_str = number
        return ret_str

    def files_plain(self, block_handle):
        if block_handle["type"] != "files":
            logging.exception("files type error! id=" + self.block_id)
            return ""
        files_list = block_handle["files"]
        ret_str = ""
        if files_list is None:
            return ret_str
        for file in files_list:
            if ret_str != "":
                ret_str += ","  # 多个文件之间用“,”分割
            ret_str += self.__file_plain(file)
        return ret_str
