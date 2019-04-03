import pymysql

# 打开数据库连接
db = pymysql.connect("localhost", "root", "wodeshujuku", "test")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
cursor.execute("DROP TABLE IF EXISTS PythonTest")

# 建表
sql = """CREATE TABLE PythonTest (
          `id` int(11) NOT NULL AUTO_INCREMENT,
          `msg` varchar(20) NOT NULL,
          `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
          PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8"""
cursor.execute(sql)

# 插入数据
sql = """INSERT INTO PythonTest(msg)
         VALUES ('信息1'),('信息2'),('信息3'),('信息4')"""
try:
    # 执行sql语句
    cursor.execute(sql)
    # 提交到数据库执行
    db.commit()
except:
    # 如果发生错误则回滚
    db.rollback()

# SQL 更新语句
sql = "UPDATE PythonTest SET msg= '更新信息4' WHERE id = 4"
try:
    # 执行SQL语句
    cursor.execute(sql)
    # 提交到数据库执行
    db.commit()
except:
    # 发生错误时回滚
    db.rollback()

# SQL 删除语句
sql = "DELETE FROM PythonTest WHERE id = 2"
try:
    # 执行SQL语句
    cursor.execute(sql)
    # 提交修改
    db.commit()
except:
    # 发生错误时回滚
    db.rollback()

# SQL 查询语句
sql = "SELECT * FROM PythonTest"
try:
    # 执行SQL语句
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()
    for row in results:
        id = row[0]
        msg = row[1]
        # 打印结果
        print("id=%d,msg=%s" % (id, msg))
except:
    print("Error: unable to fetch data")

db.close()
