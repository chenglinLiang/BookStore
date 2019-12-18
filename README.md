# BookStore
## It is a Website for BookStore online

python连接Mysql需要第三方库pymysql，连接sqlserver需要第三方库pymssql

在windows下，python3.5以上不能通过pip直接安装pymssql，需要安装编译好的whl文件

下载对应whl文件，使用pip直接安装
首先使用cmd进入whl文件所在目录,例如在D盘中(将whl复制到D盘)
~~~Bash
d:
~~~
~~~Bash
pip install pymssql-2.1.4.dev5-cp37-cp37m-win_amd64.whl
~~~
![image](https://github.com/yikegaocaisheng/BookStore/blob/master/readmeImage/1.PNG)

使用pycharm时，安装成功后仍需要进入setting->Project:LibraryStore->Project interpreter 点'+'安装,可直接安装成功
![image](https://github.com/yikegaocaisheng/BookStore/blob/master/readmeImage/2.PNG)

*sqlserver使用SQL server身份验证*

~~~Python
server = '***' #服务器名称
user = '***' #登录名
password = '***' #密码
database = '***' #数据库名

conn = pymssql.connect(server, user, password, database)
cursor = conn.cursor() #获取游标

# 直接写sql语句，建表等做出更改的最后需要提交(commit)
sql = '''create table User(
            username varchar(30) primary key,
            password varchar(20) not null
          )
'''
cursor.execute(sql)
conn.commit()

# 查询等需要取出结果(fetchall)
sql = '''select * from user
'''
cursor.execute(sql)
conn.commit()
~~~
带参数的sql语句及类的实现参照'db.py',同时有faker批量生成假数据的应用

