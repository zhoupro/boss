# boss 直聘爬虫
## 功能
- [X] 爬取列表职位信息
- [X] 爬取数据写入sqlite3数据库
- [X] 过滤已拉取职位
- [ ] 为数据标记是否已投递
- [ ] 自动投递

## 安装
```bash
pip3 install selenium
```

## 使用
```bash
python3 boss.py| tee out.txt
```
## sqlite3 客户端
ubuntu 系统下，按张sqlite3 客户端

```bash
sudo add-apt-repository -y ppa:linuxgndu/sqlitebrowser
sudo apt-get install sqlitebrowser
sqlite3 db.sqlite3


```
## 注意
使用测试号爬职位链接。用正式号打开职位链接投递。
