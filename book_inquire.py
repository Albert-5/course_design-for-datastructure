from font_color import *
from prettytable import PrettyTable
import pymysql
import time
import getpass
import datetime

'''
# 一下是连接mysql的测试
db = pymysql.connect('localhost','Local','123456','Book_Inquire')
# 使用cursor（）方法创建一个游标对象
cursor = db.cursor()
'''

# 定义图书类
class Book(object):
    def __init__(self,bnum,name,author,press,Pub_time,price):
        self.bnum = bnum
        self.name = name
        self.author = author
        self.press = press
        self.Pub_time = Pub_time
        self.price = price
    def __str__(self):
        return '<Book:%s>' % self.name


# 定义游客或者学生信息
class student(object):
   name = None
   sno = None
   sex = None
   tel = None
   classes = None



# 定义图书管理信息系统
class BookManage(object):
    # books = []
    def init(self):
        # self.books.append(Book(123,'数据库','yuanmengchao','中南民族大学出版社',2019,100))
        print(OKGREEN+'图书信息初始化成功......'+END)

    # 定义连接数据库函数
    def connect(self):
        print('正在连接到数据库，请稍后...')
        try:
            db = pymysql.connect('localhost', 'root', '123456', 'book_inquire', charset='utf8') # 连接到mysql数据库，参数
            time.sleep(1)
            print(OKGREEN+'已成功连接到数据库！'+END)
            return db
        except:
            print(ERRORRED+'数据库连接失败，请重试~'+END)


# 定义登录函数
    def loginn(self,db):
        cursor = db.cursor()
        uname = str(input('请输入用户名：'))
        psw = str(input('请输入密码：'))
        res = cursor.execute("select name from users where name=%s", (uname))
        if res == 1:
            re = cursor.execute("select * from users where name=%s", (uname))
            upwd = cursor.fetchmany()[0][1]
            if psw == upwd:
                print(OKGREEN + '登录成功！'+END)
                # db.close()
                time.sleep(1)
                return uname
            else:
                print(ERRORRED + "用户名或密码错误" + END)
                time.sleep(1)
                db.rollback()


    # 定义函数--添加管理员
    def add_admin(self,db):
        name = input('输入新的用户名：')
        pwd = input('请输入新用户名的密码：')
        sex = input('请输入管理员性别：')
        sno = input('请输入管理员学号：')
        classes = input('请输入管理员班级：')
        tel = input('请输入电话号码：')
        role = input('请确定用户角色：')
        # db = pymysql.connect(host='localhost', port='3306', user='root', passwd='123456', db='book_inquire',
        #                      charset='utf8')
        cursor = db.cursor()
        r = cursor.execute('select name from users where name = %s', (name))
        if r == 0:
            cursor.execute('insert into users values(%s,%s,%s,%s,%s,%s,%s)', (name, pwd,sno,sex,tel,classes,role))
            print(OKGREEN + '添加用户 ' + name + ' 成功' + END)
            db.commit()
            # cursor.close()
            # db.close()
            time.sleep(1)
        else:
            print(ERRORRED + '用户已存在' + END)
            db.close()
            time.sleep(1)


    # 定义删除管理员函数
    def del_admin(self,db):
        name = input('请输入要删除的成员姓名：')
        cursor = db.cursor()
        r = cursor.execute('select name from users where name = %s',(name))
        if r != 0:
            cursor.execute('delete from users where name=%s',(name))
            print(OKGREEN+'删除成功！'+END)
            db.commit()
        else:
            print(WARNING+'您要删除的成员不存在'+END)

    # 定义查找图书函数
    def bookfind(self,db):
        cursor = db.cursor()
        name = input('请输入要查询的图书名称：')
        sql = "select * from book"
        try:
            cursor.execute(sql)
            books = cursor.fetchall()
            index = 0
            li = []
            for row in books:
                if row[1] == name:
                    li.append(row)
                table = PrettyTable()
                table.field_names = [' ', 'ISBN号', '图书名', '作者', '出版社', '出版时间', '价格', '库存']
                for index, book in enumerate(li):
                    table.add_row([index+1, book[0], book[1], book[2], book[3], book[4], book[5], book[6]])
            print(table)
            # return table
        except:
            db.rollback()


    # 定义查找图书存在性
    def book(self,db,book_name,bnum):
        cursor = db.cursor()
        sql = "select * from book"
        try:
            cursor.execute(sql)
            books = cursor.fetchall()
            flag = 0
            for row in books:
                if row[0] == bnum and row[1] == book_name:
                    flag += 1
                else:
                    continue
            if flag:
                return flag
        except:
            db.rollback()



    # 定义添加图书信息函数
    def bookadd(self,db):
        print("正在检验数据库中图书.....")
        cursor = db.cursor()

        name = input('请输入图书名称：')
        bnum = input('请输入图书号：')
        # 取出图书库存信息
        total = cursor.execute('select * from book where name=%s',(name))
        if self.book(db,name,bnum):
            # 如果要添加的图书信息已经存在，则库存加1
            cursor.execute('update book set total=total+1 where name=%s',(name))
            print(WARNING+ '库存已更新！'+END)
        else:
            # v1.0 添加图书信息
            # bnum = input('请输入图书ISBN编号：')
            # author = input('请输入作者：')
            # press = input('请输入出版社信息：')
            # Pub_time = input('请输入出版时间：')
            # price = input('请输入图书价格信息：')
            # self.books.append(Book(bnum,name,author,press,Pub_time,price))
            # print(OKGREEN+'*****图书信息录入成功！******'+END)

            # v2.0 添加图书信息
            print(OKGREEN+'未在数据库中找到该书籍！请按以下提示添加图书信息~~~'+END)
            # total = 0
            cursor = db.cursor()
            # num = "\"" + input('请输入图书号：') + "\","
            num = "\"" + bnum + "\","
            name = "\"" + name + "\","
            # name = "\"" + input('请输入图书名：') + "\","
            author = "\"" + input('请输入图书作者：') + "\","
            press = "\"" + input('请输入图书出版社：') + "\","
            Pub_time = "\"" + input('请输入图书出版时间：') + "\","
            price = "\"" + input('请输入图书价格：') + "\","
            total = "\"" + input('请输入图书库存(当前应设定为1)：') + "\""  # 其实为1
            # total = "\""+str(1)+"\""
            sql = "INSERT INTO book VALUES (" + num + name + author + press + Pub_time + price + total+")"
            # sql2 = 'update book set total=total+1 where name={}'.format(name)
            try:
                cursor.execute(sql)
                # cursor.execute(sql2)
                print(OKGREEN + '图书添加成功！' + END)
                db.commit()

            except:
                print(ERRORRED + '数据添加失败！'+END)
                db.rollback()
    # 定义删除图书信息函数
    def bookdel(self,db):
        nam = input("请输入待删除的图书名：")
        bnum = input('请输入待删除的图书号：')
        nam = "\'" + nam + "\'"
        cursor = db.cursor()
        curr_total = cursor.execute('select total from book where bnum= %s',(bnum))
        curr_total = cursor.fetchall()[0][0]
        # print(curr_total)
        if curr_total != '0':                  # 首先判断要删除的书籍是否存在，如果存在则进行以下操作，否则返回未找到信息
            # sql = "delete from book where name=%s" % nam
            # try:
            #cursor.execute('update book set total=total-1 where bnum=%s', (bnum))
            cursor.execute('delete from book where bnum=%s',(bnum))
            db.commit()
            print(OKGREEN+ '图书删除成功' + END)
            # except Exception:
            #     db.rollback()

        else:
            if self.book(db,nam,bnum):                  # 首先判断要删除的书籍是否存在，如果存在则进行以下操作，否则返回未找到信息
                # sql = 'update book set total -= 1 where name=%s' %nam
                try:
                    cursor.execute("delete from book where name=%s",(nam))
                    db.commit()
                    print(OKGREEN+ '删除数据成功' + END)
                except Exception:
                    db.rollback()
            else:
                print(WARNING + "数据库中未查找到该图书信息" + END)




    # 输出所有图书的信息
    def bookshow(self,db):
        print('图书信息一览表'.center(74,'*'))
        #-----连接数据库，读取数据-----
        cursor = db.cursor()
        # 按字典返回
        # cursor = db.cursor(pymysql.cursors.DictCursor)

        sql = "SELECT * FROM book"
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                table = PrettyTable()
                table.field_names = [' ', 'ISBN号', '图书名', '作者', '出版社', '出版时间', '价格','库存']
                for index, book in enumerate(results):
                    table.add_row([index + 1, book[0], book[1], book[2], book[3], book[4], book[5], book[6]])
            print(table)
        except:
                import traceback
                traceback.print_exc()

                print("Error: unable to fetch data")
        # table = PrettyTable()
        # table.field_names = [' ','ISBN号','图书名','作者','出版社','出版时间','价格']
        # for index,book in enumerate(self.books):
        #     table.add_row([index+1,book.bnum,book.name,book.author,book.press,book.Pub_time,book.price])
        # print(table)


    # 定义菜单栏
    def menu(self,role):
        print('图书信息查询系统'.center(74,'*'))
        print(('当前时间：'+str(datetime.date.today())).center(78,'*'))
        if role != 'student':
            parameters = """
            
                ---------------欢迎使用图书信息查询系统---------------
    
                    1.录入图书信息                              
                    2.查询图书信息
                    3.删除图书信息                              
                    4.图书信息通览
                    5.添加成员信息
                    6.删除成员信息                            
                    7.退出查询系统                               
                 -----------------------------------------------------
            """
            choice = input(parameters)
            return choice
        else:
            parameters = """
            
                ---------------欢迎使用图书信息查询系统---------------                             
                    1.查询图书信息                             
                    2.图书信息通览                           
                    3.退出查询系统                               
                ------------------------------------------------------
            """

            choice = input(parameters)
            if choice == '3':
                choice = '7'
            if choice == '2':
                choice = '4'
            if choice == '1':
                choice = '2'
            return choice
    # 定义用户角色
    def get_role(self,name):
        db = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='book_inquire',
                            charset='utf8')
        cursor = db.cursor()
        cursor.execute("select role from users where name ='{}'".format(name))
        role = cursor.fetchall()[0][0]
        return role


# 定义main函数
#主函数 v2.0
def main():
    BM = BookManage()
    #初始化信息
    BM.init()
    db = BM.connect()
    # 进行登录操作
    count = 0
    print('请先登录'.center(70,'#'))
    # while count < 3:
    #     user = BM.loginn(db)
    #     if type(user) == str:
    #         role = get_role(user)
    #
    #     else:
    #         count += 1
    # if count == 3:
    #     print(ERRORRED+'不知道密码就不要再猜了哦~'+END)
    user = BM.loginn(db)
    # if type(user) == str:
    role = BM.get_role(user)
    while True:
        print(OKGREEN+'当前登录用户：{}'.format(user)+END)
        print(OKGREEN+'身份：{}'.format(role)+END)
        flag = BM.menu(role)
        if flag == '1':
            BM.bookadd(db)
        elif flag == '2':
            BM.bookfind(db)
        elif flag == '3':
            BM.bookdel(db)
        elif flag == '4':
            BM.bookshow(db)
        elif flag == '5':
            BM.add_admin(db)
        elif flag == '6':
            BM.del_admin(db)
        elif flag == '7':
            db.close()
            exit(0)
        else:
            print(ERRORRED +'选择不存在，请重新输入！'+END)


# 主函数v1.0
# 定义主函数
# def main():
#     BM = BookManage()
#     # 初始化信息
#     BM.init()
#     db = BM.connect()
#     parameters = """
#              ---------------欢迎使用图书信息查询系统---------------
#
#                1.录入图书信息
#                2.查询图书信息
#                3.删除图书信息
#                4.图书信息通览
#                5.添加管理员
#                6.退出查询系统
#
#
#              -----------------------------------------------------
#             """
#
#     while True:
#         flag = input(parameters)
#         if flag == '1':
#             BM.bookadd(db)
#         elif flag == '2':
#             BM.bookfind(db)
#         elif flag == '3':
#             BM.bookdel(db)
#         elif flag == '4':
#             BM.bookshow(db)
#         elif flag == '5':
#             db.close()
#             exit(0)
#         else:
#             print(ERRORRED +'选择不存在，请重新输入！'+END)


if __name__ == '__main__':
    main()



