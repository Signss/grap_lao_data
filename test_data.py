from pymysql import *

conn = connect(host='localhost', port=3306, database='yilulao', user='root', password='mysql', charset='utf8')
# 获得Cursor对象
cs1 = conn.cursor()

name = '羽绒服'
imgurl = 'www.baidu.com'
price = '38.6'
data_str = "insert into test_goods(name,price, imgurl) values('%s','%s','%s')" % (name, price, imgurl)
print(data_str)
count = cs1.execute(data_str)
conn.commit()
cs1.close()