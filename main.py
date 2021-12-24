from locust import TaskSet, between, task
from locust.contrib.fasthttp import FastHttpUser
import os

headers = {'authorization': 'Bearer'}

class MyTokenTask(TaskSet):
    # 接口请求路径
    login_url = "auth/oauth/token"
    index_url = "course/school/getHomePageInfo"


    # 学校端登录接口
    def on_start(self):
        print("用户初始化")
        # 请求头
        header = {"authorization": "Basic dGVzdDp0ZXN0"}
        # 请求头参数
        login_data = {
            "username": "20211115101345",
            "password": "VADzjMxbLCM=",
            "scope": "server",
            "grant_type": "password"
                      }
        print(f'登录请求参数为：{login_data}')
        # 发起请求
        with self.client.post(self.login_url, name='学校端登录post接口', data=login_data, headers=header) as response:
            # 获取接口返回的参数
            resp_dict = response.json()
            print(f'登录响应数据为{resp_dict}')
            # 提取登录接口返回参数中的token，并保存
        self.token = resp_dict['access_token']
        headers['authorization'] = 'Bearer ' + self.token
        print(self.token)

    def on_stop(self):
        print("用户结束")

    # 获取首页
    @task
    def get_index(self):
        # 发起请求
        with self.client.get(self.index_url, headers=headers, name='首页get接口', time=10, catch_response=True) as response:
            # 将接口返回值中的josn提取出来，转为字典
            resp_dict = response.json()
            print(f'响应数据为{resp_dict}')
            # 断言响应状态码
            if response.status_code == 200:
                # 请求成功
                print(resp_dict)
            else:
                response.failure(resp_dict['msg'])


class WebsiteUser(FastHttpUser):

    tasks = [MyTokenTask]
    # 请求域名
    host = "https://dyktschool.zsyky.cn/"
    #等待时间
    wait_time = between(0, 0)


if __name__ == '__main__':
    os.system('locust -f main.py')
'''
运行：
    在终端中输入：locust -f 被执行的locust文件.py --host=http://被测服务器域名或ip端口地址
    也可以不指定host
命令执行成功，会提示服务端口，如：*：8089
此时，则可通过浏览器访问机器ip:8089,看到任务测试页面
'''