# author: delta1037
# Date: 2022/01/08
# mail:geniusrabbit@qq.com
import logging
import shutil

from notion_client import Client
from notion_client import AsyncClient
from notion_client import APIErrorCode, APIResponseError
import json
from json import JSONDecodeError
from notion_api.database_parser import DatabaseParser


class Database:
    # 初始化
    def __init__(self, token, database_id, client_handle=None, async_api=False):
        self.token = token
        self.database_id = database_id
        if client_handle is None:
            if not async_api:
                self.client = Client(auth=self.token)
            else:
                self.client = AsyncClient(auth=self.token)
        else:
            self.client = client_handle
        self.database_parser = DatabaseParser(self.database_id)

    # 获取到所有的数据库数据(JSon格式)
    def query_database(self):
        try:
            database_json = self.client.databases.query(
                **{
                    "database_id": self.database_id,
                }
            )
            return database_json
        except APIResponseError as error:
            if error.code == APIErrorCode.ObjectNotFound:
                logging.exception("Database is invalid")
            else:
                # Other error handling code
                logging.exception(error)

        return None

    # 获取到所有的数据库数据(CSV格式)(数据库导出均是CSV)
    def query_database_to_csv(self, csv_name, col_name_list=None):
        db_json = self.query_database()
        if db_json is None:
            return False

        tmp_csv_filename = self.database_parser.database_result_csv(db_json, col_name_list)
        shutil.copyfile(tmp_csv_filename, csv_name)
        return True

    def query_database_to_db(self, col_name_list=None):
        # 从配置文件中获取数据库配置，打开数据库，并将csv文件写入到数据库中
        db_json = self.query_database()
        if db_json is None:
            return None

        tmp_csv_filename = self.database_parser.database_result_csv(db_json, col_name_list)
        return

    # 源文件，直接输出成json
    def query_database_to_json(self, json_name):
        db_json = self.query_database()
        if db_json is None:
            return None
        json_handle = None
        try:
            json_handle = json.dumps(db_json, ensure_ascii=False, indent=4)
        except JSONDecodeError:
            print("json decode error")
            return

        file = open(json_name, "w+", encoding="utf-8")
        file.write(json_handle)
        return
