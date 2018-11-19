from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json

class GrapLao(object):
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.url = 'http://detail.1818lao.com/leading/searchProduct.aspx?searchStr=%E7%94%B7%E8%A3%85&ctgId=3001&currPage={}'
        self.offset = 2
        self.file = open('yilulao.txt', 'w')

    def get_data(self,url):
        self.driver.get(url)
        # 隐式等待5s
        self.driver.implicitly_wait(5)
        obs = self.driver.find_elements_by_xpath("//div[@class='db_xk']/input")
        return obs

    def analysis_data(self,obs):
        goods_list = []
        for ob in obs:
            print(ob.get_attribute('imgurl'))
            print(ob.get_attribute('goodstitle'))
            print(ob.get_attribute('price'))
            content = {
                'name': ob.get_attribute('goodstitle'),
                'imgurl': ob.get_attribute('imgurl'),
                'price': ob.get_attribute('price')
            }
            goods_list.append(content)
        return goods_list

    def save_data(self, goods_list):
        for data in goods_list:
            str_data = json.dumps(data,ensure_ascii=False) + '\n'
            self.file.write(str_data)

    def run(self):
        while self.offset < 10:
            next_url = self.url.format(self.offset)
            obs = self.get_data(next_url)
            goods_list = self.analysis_data(obs)
            self.save_data(goods_list)
            self.offset += 1
        self.file.close()

if __name__ == '__main__':
    grap_lao = GrapLao()
    grap_lao.run()

