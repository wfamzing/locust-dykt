import math

from locust import TaskSet, between, task, events, LoadTestShape
from locust.contrib.fasthttp import FastHttpUser
from gevent._semaphore import Semaphore
import os

all_locusts_spawned = Semaphore()
all_locusts_spawned.acquire()
def on_hatch_complete(**kwargs):
    all_locusts_spawned.release() #创建钩子方法

#events.hatch_complete += on_hatch_complete
events.spawning_complete.add_listener(on_hatch_complete)# 挂载到locust钩子函数（所有的Locust实例产生完成时触发）

headers = {'authorization': 'Bearer'}

#获取token
class MyTokenTask(TaskSet):
    # 接口请求路径
    login_url = "auth/oauth/token" #登录接口

    ''' 首页 '''
    menu_url = "admin/menu" #首页
    index_url = "course/edu/getLowerEduHomePageInfo" #首页接口
    getEduInfo = "course/rxorganization/getEduInfo"
    getEduType = "course/rxorganization/getEduType"
    getSellCategoryCount = "course/edu/getSellCategoryCount"
    statistics_edu = "course/rxorganization/statistics"
    png_36131648 = "static/img/gzmx.36131648.png"

    ''' 主体审核 '''
    todayStatistics = "course/rxorganization/todayStatistics"
    countryApprovePage = "course/rxorganization/countryApprovePage?pageNum=1&pageSize=10"
    inOrganizationDetail = "course/rxorganizationmain/inOrganizationDetail/1470204010895618049?id=1470204010895618049"

    # 学校端登录接口
    def on_start(self):
        print("用户初始化")
        # 请求头
        header = {"authorization": "Basic dGVzdDp0ZXN0"}
        # 请求头参数
        login_data = {
            "username": "370212",
            "password": "VADzjMxbLCM=",
            "scope": "server",
            "grant_type": "password"
                      }
        print(f'登录请求参数为：{login_data}')
        all_locusts_spawned.wait()
        # 发起请求
        with self.client.post(self.login_url, name='教委端登录post接口', data=login_data, headers=header) as response:
            # 获取接口返回的参数
            resp_dict = response.json()
            print(f'登录响应数据为{resp_dict}')
            # 提取登录接口返回参数中的token，并保存
        self.token = resp_dict['access_token']
        headers['authorization'] = 'Bearer ' + self.token
        print(self.token)

    def on_stop(self):
        print("用户结束")

    #首页
    @task(3)
    class eduindexTask(TaskSet):

        ''' 首页 '''
        menu_url = "admin/menu"  # 首页
        index_url = "course/edu/getLowerEduHomePageInfo"  # 首页接口
        getEduInfo = "course/rxorganization/getEduInfo"
        getEduType = "course/rxorganization/getEduType"
        getSellCategoryCount = "course/edu/getSellCategoryCount"
        statistics_edu = "course/rxorganization/statistics"
        png_36131648 = "static/img/gzmx.36131648.png"

        # 获取首页
        @task(3)
        def get_index(self):
            all_locusts_spawned.wait()
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

            with self.client.get(self.menu_url, headers=headers, name='首页menu接口', time=10, catch_response=True) as response:
                # 将接口返回值中的josn提取出来，转为字典
                resp_dict = response.json()
                print(f'响应数据为{resp_dict}')
                # 断言响应状态码
                if response.status_code == 200:
                    # 请求成功
                    print(resp_dict)
                else:
                    response.failure(resp_dict['msg'])

            with self.client.get(self.getEduInfo, headers=headers, name='首页getEduInfo接口', time=10, catch_response=True) as response:
                # 将接口返回值中的josn提取出来，转为字典
                resp_dict = response.json()
                print(f'响应数据为{resp_dict}')
                # 断言响应状态码
                if response.status_code == 200:
                    # 请求成功
                    print(resp_dict)
                else:
                    response.failure(resp_dict['msg'])

            with self.client.get(self.getEduType, headers=headers, name='首页getEduType接口', time=10, catch_response=True) as response:
                # 将接口返回值中的josn提取出来，转为字典
                resp_dict = response.json()
                print(f'响应数据为{resp_dict}')
                # 断言响应状态码
                if response.status_code == 200:
                    # 请求成功
                    print(resp_dict)
                else:
                    response.failure(resp_dict['msg'])

            with self.client.get(self.getSellCategoryCount, headers=headers, name='首页getSellCategoryCount接口', time=10, catch_response=True) as response:
                # 将接口返回值中的josn提取出来，转为字典
                resp_dict = response.json()
                print(f'响应数据为{resp_dict}')
                # 断言响应状态码
                if response.status_code == 200:
                    # 请求成功
                    print(resp_dict)
                else:
                    response.failure(resp_dict['msg'])

            with self.client.get(self.statistics_edu, headers=headers, name='首页statistics_edu接口', time=10, catch_response=True) as response:
                # 将接口返回值中的josn提取出来，转为字典
                resp_dict = response.json()
                print(f'响应数据为{resp_dict}')
                # 断言响应状态码
                if response.status_code == 200:
                    # 请求成功
                    print(resp_dict)
                else:
                    response.failure(resp_dict['msg'])

            with self.client.get(self.png_36131648, headers=headers, name='首页png接口', time=10, catch_response=True) as response:
                # 将接口返回值中的josn提取出来，转为字典
                #resp_dict = response.json()
                #print(f'响应数据为{resp_dict}')
                # 断言响应状态码
                if response.status_code == 200:
                    # 请求成功
                    print(resp_dict)
                else:
                    response.failure(resp_dict['msg'])


    #主体审核
    @task(2)
    class eduApproveTask(TaskSet):

        ''' 主体审核 '''
        todayStatistics = "course/rxorganization/todayStatistics"
        countryApprovePage = "course/rxorganization/countryApprovePage?pageNum=1&pageSize=10"
        inOrganizationDetail = "course/rxorganizationmain/inOrganizationDetail/1470204010895618049?id=1470204010895618049"

        @task(2)
        def get_orgApprove(self):
            all_locusts_spawned.wait()
            # 发起请求
            with self.client.get(self.todayStatistics, headers=headers, name='主体审核todayStatistics接口', time=10, catch_response=True) as response:
                # 将接口返回值中的josn提取出来，转为字典
                resp_dict = response.json()
                print(f'响应数据为{resp_dict}')
                # 断言响应状态码
                if response.status_code == 200:
                    # 请求成功
                    print(resp_dict)
                else:
                    response.failure(resp_dict['msg'])
            with self.client.get(self.countryApprovePage, headers=headers, name='主体审核countryApprovePage接口', time=10, catch_response=True) as response:
                # 将接口返回值中的josn提取出来，转为字典
                resp_dict = response.json()
                print(f'响应数据为{resp_dict}')
                # 断言响应状态码
                if response.status_code == 200:
                    # 请求成功
                    print(resp_dict)
                else:
                    response.failure(resp_dict['msg'])
            with self.client.get(self.inOrganizationDetail, headers=headers, name='主体审核inOrganizationDetail接口', time=10, catch_response=True) as response:
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
    host = "https://edu.dyketang.com/" #设置url
    #等待时间
    wait_time = between(0, 0)

class StepLoadShaper(LoadTestShape):
    '''
    逐步加载实例

    参数解析：
        step_time -- 逐步加载时间
        step_load -- 用户每一步增加的量
        spawn_rate -- 用户在每一步的停止/启动
        time_limit -- 时间限制

    '''
    setp_time = 30
    setp_load = 30
    spawn_rate = 30
    time_limit = 600

    def tick(self):
        run_time = self.get_run_time()

        if run_time > self.time_limit:
            return None

        current_step = math.floor(run_time /self.setp_time) +1

        return(current_step * self.setp_load,self.spawn_rate)

if __name__ == '__main__':
    os.system('locust -f edu.py')
'''
运行：
    在终端中输入：locust -f 被执行的locust文件.py --host=http://被测服务器域名或ip端口地址
    也可以不指定host
命令执行成功，会提示服务端口，如：*：8089
此时，则可通过浏览器访问机器ip:8089,看到任务测试页面
'''