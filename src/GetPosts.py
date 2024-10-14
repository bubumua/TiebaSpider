import requests
import json
import time
import random
import datetime

# post content type：
# 0 text
# 1 link
# 2 emoji
# 3 image

headers = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
]

# img idx
count = 0


def get_random_header():
    header = {'User-Agent': random.choice(headers), 'refer': 'https://tieba.baidu.com'}
    return header


# define retry function
def retry_request(url, headers, max_retries=4, wait_time=5):
    retries = 0
    while retries < max_retries:
        res = requests.get(url, headers=get_random_header())

        if res.status_code != 200:
            print("{} received not 200 status. Retrying in {} seconds...".format(url, wait_time))
            time.sleep(wait_time)
            retries += 1
        else:
            return res

    return None


def download_image(url: str, idx, save_path: str) -> bool:
    # 发起 GET 请求获取图片数据
    response = requests.get(url)

    if response.status_code == 200:
        # 将获取的图片数据写入本地文件
        save_path += (str(idx) + '.jpg')
        with open(save_path, 'wb') as file:
            file.write(response.content)
        return True
    else:
        print(f"下载失败：{url}")
        return False


def process_content_item(ct: dict, outputpath: str = "../output/images/"):
    """
    处理帖子内容中的每一项
    post content type：
    0 text
    1 link
    2 emoji
    3 image
    :param ct: dict with content item
    :return: None
    """
    global count
    # text
    if ct["type"] == 0:
        pass
    # link
    elif ct["type"] == 1:
        pass
    # emoji
    elif ct["type"] == 2:
        pass
    # image
    elif ct["type"] == 3:
        # download
        download_image(ct["src"], count, outputpath)
        count += 1
    else:
        print("Unknown type: ", ct["type"])

    return None


def capture_in_post(post: dict):
    """
    遍历帖子内容（包括二级评论）
    :param post: dict with post content and sub-post (if it has)
    :return: None
    """
    content = post["content"]

    for ct in content:
        process_content_item(ct)

    if ("sub_post_number" in post) and post["sub_post_number"] > 0:
        sub_post_list = post["sub_post_list"]
        for sp in sub_post_list:
            capture_in_post(sp)

    return None


def search_by_tid(tid_list: list) -> list:
    # record 403 tid
    list403 = []
    # search content for each tip
    for tid in tid_list:
        thread_url = "https://tieba.baidu.com/mg/p/getPbData?kz={}".format(tid)
        header = {'User-Agent': random.choice(headers), 'refer': 'https://tieba.baidu.com'}
        response = retry_request(thread_url, header)
        if response is None:
            if tid not in list403:
                list403.append(tid)
            continue
        else:
            tmp = json.loads(response.text)
            try:
                post_list = tmp["data"]["post_list"]
                for post in post_list:
                    capture_in_post(post)
            except KeyError:
                continue

    print(list403)
    return list403


if __name__ == '__main__':
    with open('../output/tid_list.json', 'r') as tl:
        tid_list = json.load(tl)
    tidlist403 = search_by_tid(tid_list)
    with open('../output/tid_list_403.json', 'w') as tl403:
        json.dump(tidlist403, tl403)
