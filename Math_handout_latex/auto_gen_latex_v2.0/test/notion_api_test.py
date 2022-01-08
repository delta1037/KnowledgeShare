from notion_api.database import Database
from configuration_service import ConfigurationService

if __name__ == '__main__':
    config = ConfigurationService()
    db_handle = Database(token=config.get_key("token"), database_id=config.get_key("database_id"))
    db_handle.query_database_to_csv("test_result.csv", col_name_list=["题目", "思路", "属性", "类型"])
    # db_handle.query_database_to_json("database.json")

# Snipaste_2022-01-08_12-45-07.png|https://s3.us-west-2.amazonaws.com/secure.notion-static.com/9511792f-ca3c-4c25-8991-dde1e1376b60/Snipaste_2022-01-08_12-45-07.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20220108%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20220108T134258Z&X-Amz-Expires=3600&X-Amz-Signature=86e2e35c92fa7f7bf92a03d4eccfb107c440a850a1cb953d309a784a84ec888a&X-Amz-SignedHeaders=host&x-id=GetObject,Snipaste_2021-12-30_12-58-00.png|https://s3.us-west-2.amazonaws.com/secure.notion-static.com/d44829d7-33b4-4ffa-b495-96c43da18726/Snipaste_2021-12-30_12-58-00.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20220108%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20220108T134258Z&X-Amz-Expires=3600&X-Amz-Signature=57d2d4cfa6c58a2e1c6df9437f208ecf70947390dc6391a8879d57af1ccd81ec&X-Amz-SignedHeaders=host&x-id=GetObject
