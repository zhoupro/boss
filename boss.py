from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sqlite3
import datetime

conn = sqlite3.connect("db.sqlite3")
cursor=conn.cursor()

# status 1, 入库  2, 已投递 3, 未投递
#创建职位表
cursor.execute("""
CREATE TABLE if not exists jobs(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  job_name TEXT,
  company_name TEXT,
  salary TEXT,
  detail_url TEXT,
  uniq_url TEXT,
  status INTEGER,
  create_time timestamp,
  apply_time  timestamp
);
""")

cursor.execute("""CREATE INDEX if not exists idx_jobs_uniq_url_status ON jobs (uniq_url, status);
""")

conn.commit()


def insertRow(job_name,company_name,salary,detail_url):
  create_time = datetime.datetime.now()

  sqlite_insert_query = """INSERT INTO jobs
   (job_name,company_name , salary, detail_url, uniq_url, status, create_time)
                             VALUES
                            ("{}","{}","{}","{}","{}",{},"{}");"""

  uniq_url = detail_url.split("?")[0]
  sql = sqlite_insert_query.format(job_name,company_name,salary, detail_url, uniq_url, 1,create_time)
  cursor.execute(sql)
  conn.commit()

def rowExist(detail_url):
  uniq_url = detail_url.split("?")[0]
  sqlite_select_query = """SELECT * from jobs where uniq_url = "{}"
  """
  cursor.execute(sqlite_select_query.format(uniq_url))
  records = cursor.fetchall()
  if len(records) > 0 :
    return True
  return False


driver = webdriver.Chrome()
try:
  driver.get("https://www.zhipin.com")
  # login
  element = WebDriverWait(driver,3000).until(
      EC.presence_of_all_elements_located((By.CLASS_NAME, "nav-figure"))
      )

  # 循环查询的职位列表
  j = 1
  for i in range(1,3):
    url = "https://www.zhipin.com/web/geek/job?query=golang%E4%B8%BB%E7%A8%8B&city=101010100&salary=406&page={}"
    driver.get(url.format(i))
    WebDriverWait(driver,3000).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "job-card-wrapper"))
        )
    elements = driver.find_elements(By.CLASS_NAME, "job-card-wrapper")
    pageSize = len(elements)

    jobList = []

    for e in elements:
      curE = {}
      job_name = e.find_element(By.CLASS_NAME, "job-name")
      curE["job_name"] = job_name.text

      company_name = e.find_element(By.CLASS_NAME, "company-name")
      curE["company_name"] = company_name.text

      salary = e.find_element(By.CLASS_NAME, "salary")
      curE["salary"] = salary.text

      infoUrl = e.find_element(By.CLASS_NAME, "job-card-left")
      detail_url = infoUrl.get_attribute("href")
      curE["detail_url"] = detail_url
      jobList.append(curE)

    for job in jobList:
      if rowExist(job["detail_url"]) == False:
        print("Yes records")
        j = j + 1
        insertRow(job["job_name"],job["company_name"],job["salary"],job["detail_url"])
      else:
        print("No records")

      print("cur {}".format(i))
      print(job["detail_url"])
      print(job["job_name"])
      print(job["company_name"])
      print(job["salary"])
      print("--------------------")

  print("total insert {} records".format(j))

finally:
  driver.quit()
