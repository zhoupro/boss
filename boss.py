
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


driver = webdriver.Chrome()
driver.get("https://www.zhipin.com")


try:
  # login
  element = WebDriverWait(driver,3000).until(
      EC.presence_of_all_elements_located((By.CLASS_NAME, "nav-figure"))
      )

  # 循环查询的职位列表
  for i in range(1,8):
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
      print("cur {}".format(i))
      print(job["detail_url"])
      print(job["job_name"])
      print(job["company_name"])
      print(job["salary"])
      print("--------------------")

finally:
  driver.quit()
