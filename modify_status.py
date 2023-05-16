from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sqlite3
import time
import datetime

conn = sqlite3.connect("db.sqlite3")
conn.row_factory = sqlite3.Row
cursor=conn.cursor()


def batchUpdateJobStatus(status, ids):
  str = "("
  for id in ids:
    str = "{}{}{}".format(str, id, ",")
  str = str.strip(",")
  str = str + ")"
  update_time = datetime.datetime.now()

  sql = """update jobs set status = {}, apply_time = "{}" where id in {}""".format(status,  update_time, str )
  cursor.execute(sql)
  conn.commit()

driver = webdriver.Chrome()
try:
  driver.get("https://www.zhipin.com")
  # login
  element = WebDriverWait(driver,3000).until(
      EC.presence_of_all_elements_located((By.CLASS_NAME, "nav-figure"))
      )

  all_already_chat = []
  all_no_chat = []
  # 循环查询的职位列表
  for i in range(1,1000):
    data = cursor.execute('SELECT * FROM jobs where status = 1 limit 10')
    jobs = data.fetchall()
    if len(jobs) == 0:
      break

    result = [dict(row) for row in jobs]

    already_chat = []
    no_chat = []
    for job in result:
      url = job["detail_url"]
      # print(url)
      driver.get(url)
      WebDriverWait(driver,3000).until(
          EC.presence_of_all_elements_located((By.CLASS_NAME, "job-op"))
          )
      job_op = driver.find_element(By.CLASS_NAME, "job-op")
      start_chat_list = job_op.find_elements(By.CLASS_NAME,"btn-startchat")
      if len(start_chat_list) == 0:

        batchUpdateJobStatus(4, [job["id"]])
        print("job down")
        continue
      active_times = driver.find_elements(By.CLASS_NAME,"boss-active-time")
      if len(active_times) != 0:
        active_time = driver.find_element(By.CLASS_NAME,"boss-active-time").text
        if active_time != "刚刚活跃" and  active_time != "今日活跃"  :
          batchUpdateJobStatus(5, [job["id"]])
          print("job expire {}".format(active_time))
          time.sleep(4)
          continue

      start_chat = job_op.find_element(By.CLASS_NAME,"btn-startchat")
      if start_chat.text == "立即沟通":
        print("no chat")
        no_chat.append(job["id"])
      else:
        print("already chat")
        already_chat.append(job["id"])
      time.sleep(4)

    print("alread_chat list {}, len {}".format(already_chat, len(already_chat)))
    batchUpdateJobStatus(2, already_chat)
    print("no chat list {},len {} ".format(no_chat,len(no_chat)))
    batchUpdateJobStatus(3, no_chat)

  print("all_alread_chat list {}, len {}".format(all_already_chat, len(all_already_chat)))
  print("all no chat list {},len {} ".format(all_no_chat,len(all_no_chat)))


finally:
  driver.quit()
