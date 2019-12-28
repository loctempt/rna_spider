# -*- coding: utf-8 -*-
import os
import requests
import lxml
from lxml import html

headers = {
    'Host': 'www.zhihu.com',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    # 2017.12 经网友提醒，知乎更新后启用了网页压缩，所以不能再采用该压缩头部
    # !!!注意, 请求头部里使用gzip, 响应的网页内容不一定被压缩，这得看目标网站是否压缩网页
    # 'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
}

savingPath = ''
baseUrl = 'http://dude.docking.org/targets'
totalFiles = 0

def save_dir(path):
    global savingPath
    if not os.path.exists(path):
        print('path \'{}\' does not exists, creating...'.format(path))
        os.mkdir(path)
        print('successfully creating path')
    print('current in use saving path: {}'.format(path))
    savingPath = path

def save(text, filename):
    file_path = os.path.join(savingPath, filename+".tar.gz")
    with open(file_path, 'wb') as f:
        f.write(text)

def get_html_page(url):
    resp = requests.get(url)
    ctnt = resp.content
    return html.fromstring(ctnt)

def extract_rna_names(page: html):
    global totalFiles
    row_collection:list = page.xpath('//*[@id="content"]/table/tbody/tr')
    print("length of row_collection:", len(row_collection))
    # print((row_collection[0].xpath('td[2]/a/@href')))
    mapped_list = list(map(lambda tr_elem: tr_elem.xpath('td[2]/a')[0].text, row_collection))
    totalFiles = len(mapped_list)
    print(totalFiles)
    return mapped_list

def get_download_link(name: str):
    return "{0}/{1}/{1}.tar.gz".format(baseUrl, name.lower())

def loop_detail_page_link_list(names: list):
    for idx in range(len(names)):
        print("download process: {} out of {}".format(idx + 1, totalFiles))
        download_file(names[idx])

def download_file(filename: str):
    resp = requests.get(get_download_link(filename))
    ctnt = resp.content
    save(ctnt, filename)

def main():
    print('cwd:{}'.format(os.getcwd()))
    save_dir('./save_dir')
    name_list = extract_rna_names(get_html_page("http://dude.docking.org/targets"))
    loop_detail_page_link_list(name_list)


if __name__ == '__main__':
    main()
