# boss 直聘爬虫
## 功能
- [X] 爬取列表职位信息
- [X] 爬取数据写入sqlite3数据库
- [X] 过滤已拉取职位
- [X] 过滤已下架职位
- [X] 为数据标记是否已投递
- [X] 标记过期职位
- [ ] 自动投递

## 安装
```bash
pip3 install selenium
```

## 表结构
保存职位信息表
| 列           | 类型     | 备注                                   |
|--------------|----------|----------------------------------------|
| id           | int      | 主键                                   |
| job_name     | text     | 工作名                                 |
| company_name | text     | 公司名                                 |
| salary       | text     | 薪资                                   |
| detail_url   | text     | 沟通链接                               |
| uniq_url     | text     | 岗位唯一值                             |
| create_time  | datetime | 获取职位时间                           |
| status       | int      | 岗位状态，1：入库，2：已沟通 3: 待沟通 |

## status
  - 1
      入库
  - 2
      已投递
  - 3
      待投递
  - 4
      职位下架
  - 5
      职位超时不登录
  - 6
      不投递
  - 7
      待定


## 使用
- 获取职位
```bash
python3 joblist.py| tee out.txt
```
- 标记已投递建立
```bash
python3 modify_status.py
```
- 查看未投递职位  
  使用 sqlitebrowser 打开数据库，筛选状态为3的工作。决定是否沟通。并修改岗位的状态为已投递，即status修改为2。

## sqlite3 客户端
ubuntu 系统下，按张sqlite3 客户端

```bash

sudo add-apt-repository -y ppa:linuxgndu/sqlitebrowser
sudo apt-get install sqlitebrowser
sqlite3 db.sqlite3

```
## 注意
使用测试号爬职位链接。用正式号打开职位链接投递。
