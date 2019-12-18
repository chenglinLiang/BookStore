# BookStore
##It is a web site for BookStore online

python连接Mysql需要第三方库pymysql，连接sqlserver需要第三方库pymssql

在windows下，python3.5以上不能通过pip直接安装pymssql，需要安装编译好的whl文件

下载对应whl文件，使用pip直接安装
'''Bash
pip install pymssql-2.1.4.dev5-cp37-cp37m-win_amd64.whl
'''

使用pycharm时，安装成功后仍需要进入setting->Project:LibraryStore->Project interpreter 点'+'安装,可直接安装成功
