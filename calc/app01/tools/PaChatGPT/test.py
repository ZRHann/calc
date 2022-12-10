import pymysql
db = pymysql.connect(host='localhost',
                                  user='root',
                                  password='zg801zrh160118.',
                                  database='ChatGPT_OL')
cursor = db.cursor()
sql = """INSERT INTO ChatGBT_OL(msg_json)
                 VALUES (1)"""
cursor.execute(sql)
