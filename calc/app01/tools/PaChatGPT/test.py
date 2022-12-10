import pymysql
db = pymysql.connect(host='localhost',
                                  user='root',
                                  password='zg801zrh160118.',
                                  database='ChatGPT_OL')
cursor = db.cursor()
sql = """INSERT INTO conversation_log(msg_json) VALUES ()"""
cursor.execute(sql)
