import pymysql  # mysql 连接数据库
# import pymssql      #sql server 连接数据库
from faker import Faker


# 3 db = BookStore()
class BookStore:
    # MySQL连接数据库
    def __init__(self):
        self.conn = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='13831347435',
            db='bookstore',
            port=3306,
            charset='utf8'
        )
        self.curosr = self.conn.cursor()

    # sqlserver连接数据库
    '''
    def __init__(self):
        self.conn = pymssql.connect(
            '(local)',   服务器名称
            '****',      登录名
            '****',      密码
            '****'       所连接数据库
        )
        self.curosr = self.conn.cursor()
    '''

    def create(self):
        sql_1 = '''create table User(
                    username varchar(20) primary key ,
                    password varchar(20) not null
                )
                '''
        sql_2 = '''create table Book(
                    bookname varchar(30) not null ,
                    writer varchar(30) not null ,
                    ISBN varchar(20) primary key ,
                    publish varchar(50) not null ,
                    price float not null ,
                    discount float ,
                    contents text ,
                    inventory int not null
                )
                '''
        sql_3 = '''create table Orders(
                      id varchar(30) primary key ,
                      stats tinyint not null ,
                      pay tinyint not null ,
                      book varchar(20) not null ,
                      buyer varchar(20) not null ,
                      foreign key (book) references Book(ISBN),
                      foreign key (buyer) references User(username)
                    )
                '''
        sql_4 = '''create table Buy(
                      username varchar(20) ,
                      ISBN varchar(30) ,
                      primary key (username, ISBN) ,
                      foreign key (username) references User(username) ,
                      foreign key (ISBN) references Book(ISBN)
                    )
                '''
        sql_5 = '''create table Browsing(
                      username varchar(20) ,
                      ISBN varchar(30) ,
                      primary key (username, ISBN) ,
                      foreign key (username) references User(username) ,
                      foreign key (ISBN) references Book(ISBN)
                    )
                '''
        sql_6 = '''create table Comment(
                      comt varchar(100) ,
                      username varchar(20) ,
                      primary key (Comt, username) ,
                      foreign key (username) references User(username)
                    )
                '''
        sql_7 = '''create table Complain(
                      Comn varchar(100) ,
                      username varchar(20) ,
                      primary key (Comn, username) ,
                      foreign key (username) references User(username)
                    )
                '''
        sql_8 = '''create table Logistics(
                      id varchar(20) primary key ,
                      send tinyint not null ,
                      take tinyint not null ,
                      place1 varchar(40) ,
                      place2 varchar(40) ,
                      place3 varchar(40) ,
                      place4 varchar(40) ,
                      place5 varchar(40) ,
                      place6 varchar(40) ,
                      place7 varchar(40) ,
                      place8 varchar(40) ,
                      place9 varchar(40) ,
                      place10 varchar(40) ,
                      foreign key (id) references orders(id)
                    )
                '''
        sqls = [sql_1, sql_2, sql_3, sql_4, sql_5, sql_6, sql_7, sql_8]
        for sql in sqls:
            self.curosr.execute(sql)
        self.conn.commit()

    def faker(self):
        f = Faker(locale="zh_CN")  #实例
        count = 0
        for i in range(1000):
            # user
            username = f.name()
            password = f.password(length=15)
            # book
            bookname = f.word()
            writer = f.name()
            ISBN = f.numerify()
            publish = f.company()
            price = f.random_int(max=100)
            discount = f.random_digit()
            contents = f.text()
            inventory = f.random_int(min=100, max=999)
            # orders
            id = f.pystr()
            stats = 1
            pay = 1
            # logistics
            send = 1
            take = 0
            place1 = f.address()
            place2 = f.city_suffix()
            place3 = f.district()
            place4 = f.province()
            place5 = f.province()
            place6 = f.district()
            place7 = f.city_suffix()
            place8 = f.address()
            # comment
            comm = f.text()
            # complain
            comp = f.text()

            sql_user = '''insert into
                            user(username, password) VALUES (%s,%s)
            '''

            sql_book = '''insert into
                            book(bookname, writer, ISBN, publish, price, discount, contents, inventory)
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            '''

            sql_orders = '''insert into
                              orders(id, stats, pay, book, buyer) 
                              VALUES (%s,%s,%s,%s,%s) 
            '''
            sql_logistics = '''insert into
                                logistics(id, send, take, place1, place2, place3, place4, place5, place6, place7, place8) 
                                values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            '''
            sql_browsing = '''insert into
                                browsing(username, ISBN) VALUES (%s,%s)
            '''
            sql_buy = '''insert into
                            buy(username, id) VALUES (%s,%s)
            '''
            sql_comment = '''insert into
                                comment(comm, username) VALUES (%s,%s)
            '''
            sql_complain = '''insert into
                                complain(comp, username) VALUES (%s,%s)
            '''
            try:
                self.curosr.execute(sql_user, (username, password))
                self.curosr.execute(sql_book, (bookname, writer, ISBN, publish, price, discount, contents, inventory))
                self.curosr.execute(sql_orders, (id, stats, pay, ISBN, username))
                self.curosr.execute(sql_logistics,
                                    (id, send, take, place1, place2, place3, place4, place5, place6, place7, place8))
                self.curosr.execute(sql_browsing, (username, ISBN))
                self.curosr.execute(sql_buy, (username, id))
                self.curosr.execute(sql_comment, (comm, username))
                self.curosr.execute(sql_complain, (comp, username))
                self.conn.commit()
                count = count + 1
            except pymysql.err.IntegrityError:
                pass
        print('成功', count, '次')

    def selectBook(self, keyword):
        sql = '''select bookname,price,writer,publish from books
                    where bookname like %s or writer like %s or ISBN like %s or publish like %s
                '''
        self.curosr.execute(sql, ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%'))
        results = list(self.curosr.fetchall())
        return results

    def showBook(self):
        sql = '''select bookname,price,writer,publish,ISBN
                    from books
             '''
        self.curosr.execute(sql)
        results = list(self.curosr.fetchall())
        return results

    def selectComment(self):
        sql = '''select username,comm
                    from comment
        '''
        self.curosr.execute(sql)
        results = list(self.curosr.fetchall())
        return results

    def insert_user(self, username, password):
        sql = '''insert into
                    user(username, password) values (%s,%s)
        '''
        self.curosr.execute(sql, (username, password))
        self.conn.commit()

    def select_user(self, username):
        sql = '''select username
                  from user
                  where username=%s
        '''
        self.curosr.execute(sql, username)
        result = list(self.curosr.fetchall())
        print(result)
        return result

    def verfiy_user(self, username, password):
        sql = '''select username
                    from user
                    where username=%s and password=%s
        '''
        self.curosr.execute(sql, (username, password))
        result = self.curosr.fetchall()
        return result

    def selectOrder(self, username):
        sql = '''select id, bookname,stats, price, send, take, place1, place2, place3,place4,place5,place6,place7,place8,place9 from root
                    where username=%s
        '''
        self.curosr.execute(sql, username)
        results = self.curosr.fetchall()
        return results

    def select_logistics(self, username):
        sql = '''select * from logistics
                    where id in(
                    select id from orders
                    where buyer=%s
                    )
        '''
        self.curosr.execute(sql, username)
        results = list(self.curosr.fetchall())
        return results

    def selectISBN(self, ISBN):
        sql = '''select bookname, price, writer, publish
                from books
                where ISBN=%s
        '''
        self.curosr.execute(sql, ISBN)
        results = self.curosr.fetchall()
        return results[0]

    def selectUser(self, username):
        sql = '''select username from user
                    where username=%s
        '''
        self.curosr.execute(sql, username)
        username = self.curosr.fetchall()
        return username[0][0]

    def insertOrder(self, ISBN, username, telephone, address, note):
        f = Faker("zh_CN")
        sql = '''insert into
                    orders(id, stats, pay, book, buyer, telephone, address, note) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        '''
        try:
            id = f.pystr()
            stats = 1
            pay = 1
            self.curosr.execute(sql, (id, stats, pay, ISBN, username, telephone, address, note))
            self.conn.commit()
            self.insertLogistics(id)
        except pymysql.err.IntegrityError:
            self.conn.rollback()

    def insertLogistics(self, id):
        sql = '''insert into logistics(id, send, take)
                    values (%s,%s,%s)
        '''
        self.curosr.execute(sql, (id, 1, 0))
        self.conn.commit()

    def selectRoot(self):
        sql = '''select * from root
        '''
        self.curosr.execute(sql)
        results = self.curosr.fetchall()
        return results

    def selectBookUser(self):
        sql = '''select * from book
        '''
        self.curosr.execute(sql)
        results = self.curosr.fetchall()
        return results

    def selectComplain(self):
        sql = '''select username, comp from complain
        '''
        self.curosr.execute(sql)
        results = self.curosr.fetchall()
        return results

    # def selectCommentRoot(self):
    #     sql = '''select username, comm from comment
    #     '''
    #     self.curosr.execute(sql)
    #     results = self.curosr.fetchall()
    #     return results

    def selectLogistics(self):
        sql = '''select * from fast
        '''
        self.curosr.execute(sql)
        results = self.curosr.fetchall()
        return results

    # def delUser(self, username):
    #     sql = '''set foreign_key_checks = 0
    #     '''
    #     self.curosr.execute(sql)
    #     sql = '''delete from user
    #                 where username=%s
    #     '''
    #     self.curosr.execute(sql, username)
    #     self.conn.commit()

    def __del__(self):
        self.curosr.close()
        self.conn.close()

# if __name__ == '__main__':
#     db = BookStore()
#     BookStore.
