# 通过吧名，获取该吧内所有帖子的tid以及相关信息
# reference: https://www.cnblogs.com/hair-is-decreasing/p/18191432

import requests
import json
import datetime
import random
import time

# 吧名
kw = "图片混淆"
# 爬取的页数，必须大于1。实际爬取的页数是该值-1
pages = 2
# 每一页的帖子数量
rn = 100


def get_tids(kw: str, end_page: int, rn: int = 100, start_page: int = 1,
             tidlistfilepath: str = '../output/tid_list.json',
             threadinfofilepath: str = '../output/ThreadInfos.json') -> list:
    # 用来存储所有tid，同时也是函数最后的输出
    tid_list = []

    # 定义header。用谷歌的headers会失败
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv: 11.0) like Gecko'
    }

    # 检查文件是否存在，如果不存在则创建一个空的 JSON 文件
    # try:
    #     with open('ThreadInfos.json', 'r') as file:
    #         filedata = json.load(file)
    # except FileNotFoundError:
    #     filedata = []
    filedata = []

    # 逐页获取信息
    for page in range(start_page, end_page):
        print("current processing page: ", page)
        base_url = "https://tieba.baidu.com/mg/f/getFrsData?kw={}&rn={}&pn={}&is_good=0&cid=0&sort_type=1&fr=&default_pro=0&only_thread_list=0".format(
            kw, rn, page)
        # get json from base_url
        response = requests.get(url=base_url, headers=header)
        tmp = json.loads(response.text)
        thread_list = tmp["data"]["thread_list"]
        # 获取每个帖子的tid、创建时间、标题、摘要
        for thread in thread_list:
            # 获取tid
            tid = thread["tid"]
            # 获取创建时间
            created_timestamp = thread["create_time"]
            dt = datetime.datetime.fromtimestamp(created_timestamp)
            date_str = dt.strftime('%Y-%m-%d %H:%M:%S')
            # 获取标题与摘要
            title = thread["title"]
            tid_list.append(tid)
            # 拼接标题与摘要
            try:
                abstract_texts = [abstract["text"] for abstract in thread["abstract"]]
                title += " " + " ".join(abstract_texts)
            except KeyError:
                continue

            thread_info = {
                "tid": tid,
                "title": title,
                "created_time": date_str,
                "created_timestamp": created_timestamp
            }

            filedata.append(thread_info)
            tid_list.append(tid)

    # 保存到 JSON 文件
    with open(threadinfofilepath, 'w', encoding='utf-8') as file:
        json.dump(filedata, file, ensure_ascii=False, indent=2)

    with open(tidlistfilepath, 'w') as f:
        json.dump(tid_list, f)

    return tid_list


if __name__ == '__main__':
    get_tids(kw, pages, rn)
