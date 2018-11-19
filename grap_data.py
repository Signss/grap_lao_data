import requests
import json
from pymysql import *
from lxml import etree

class YiLaoData(object):

    def __init__(self):
        self.url = 'http://detail.1818lao.com/leading/searchProduct.aspx?searchStr=%E7%94%B7%E8%A3%85&ctgId=3001&currPage={}'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        }
        self.offset = 2
        self.file = open('yilulao.txt', 'w')

    def get_data(self, url):
        response = requests.get(url, headers=self.headers)
        return response.content

    def parse_list_page(self, data):
        html = etree.HTML(data)
        goods_list = html.xpath("//div[@class='db_xk']/input")
        data_list = []
        for good in goods_list:
            data_dict = {}
            data_dict['name'] = good.xpath('./@goodstitle')[0]
            data_dict['imgurl'] = good.xpath('./@imgurl')[0]
            data_dict['price'] = good.xpath('./@price')[0]
            data_list.append(data_dict)
        return data_list
    def save_data_mysql(self, data_list):
        # 创建Connection连接
        conn = connect(host='localhost', port=3306, database='yilulao', user='root', password='mysql', charset='utf8')
        # 获得Cursor对象
        cs1 = conn.cursor()
        for data in data_list:
            name = data['name']
            imgurl = data['imgurl']
            price = data ['price']
            count = cs1.execute("insert into goods(name, price, imgurl) values('%s','%s','%s')"%(name,price,imgurl))
        conn.commit()
        cs1.close()
    def save_data(self, data_list):
        for data in data_list:
            str_data = json.dumps(data, ensure_ascii=False) + '\n'
            self.file.write(str_data)

    def run(self):
        while self.offset < 10:
            next_url = self.url.format(self.offset)
            html_data = self.get_data(next_url)
            data_list = self.parse_list_page(html_data)
            self.save_data(data_list)
            self.save_data_mysql(data_list)
            self.offset += 1
        self.file.close()


if __name__ == '__main__':
    grap_lao = YiLaoData()
    grap_lao.run()
#
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# import time
#
# chrome_options = Options()
# chrome_options.add_argument('--headless')
# driver = webdriver.Chrome(chrome_options=chrome_options)
# driver.get('http://detail.1818lao.com/leading/searchProduct.aspx?searchStr=%E7%94%B7%E8%A3%85&ctgId=3001&currPage=3')
# time.sleep(5)
# obs = driver.find_elements_by_xpath("//div[@class='db_xk']/input")
# goods_list = []
# for ob in obs:
#     print(ob.get_attribute('imgurl'))
#     print(ob.get_attribute('goodstitle'))
#     print(ob.get_attribute('price'))
#     content = {
#         'name': ob.get_attribute('goodstitle'),
#         'imgurl': ob.get_attribute('imgurl'),
#         'price': ob.get_attribute('price')
#     }
#     goods_list.append(content)
#
# print(goods_list)
#
# with open('goodinfo', 'w') as f:
#     f.write(str(goods_list))
