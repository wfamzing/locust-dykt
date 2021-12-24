import json
from  locust.contrib.fasthttp import FastHttpUser
from locust import HttpUser, task, user
from locust.clients import HttpSession

header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        "content-type": "application/x-www-form-urlencoded",
        "authorization": "Bearer "
    }

class WebsiteTasks(FastHttpUser):
    host = 'https://dyktschool.zsyky.cn/'

    def on_start(self):
        #pass
        self.login()

    def login(self):
        h = {
            # "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
            # "content-type": "application/x-www-form-urlencoded",
            "authorization": "Basic dGVzdDp0ZXN0"
        }
        body = {
            "username": "20211115101345",
            "password": "VADzjMxbLCM=",
            "scope": "server",
            "grant_type": "password"
        }
        #self.session = HttpSession(self.host)
        r = self.client.post("auth/oauth/token", data=body, headers=h).text
        #print(r.text)
        #assert "access_token" in r #断言，判断接口返回是否成功
        r = json.loads(r)
        token = r['access_token']
        # header = {
        #     "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        #     "content-type": "application/x-www-form-urlencoded",
        #     "authorization": "Bearer "
        # }
        header["authorization"] = "Bearer " + token
        #return header


    @task(2)
    def index(self):
        #header = self.login()
        self.client.get("course/school/getHomePageInfo", headers=header)

    @task(1)
    def about(self):
        #header = self.login()
        self.client.get("course/rxcoursegeneralcategory/getInGeneralCategory",headers=header)