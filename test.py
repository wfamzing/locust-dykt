import json
import math

from locust import TaskSet, between, task, events, LoadTestShape, HttpUser
from locust.contrib.fasthttp import FastHttpUser
from gevent._semaphore import Semaphore
import os

all_locusts_spawned = Semaphore()
all_locusts_spawned.acquire()


def on_hatch_complete(**kwargs):
    all_locusts_spawned.release()  # 创建钩子方法


# events.hatch_complete += on_hatch_complete
events.spawning_complete.add_listener(on_hatch_complete)  # 挂载到locust钩子函数（所有的Locust实例产生完成时触发）

headers = {'authorization': 'Bearer'}


# 获取token
class MyTokenTask(TaskSet):
    # 接口请求路径
    login_url = "auth/oauth/token"  # 登录接口

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
        # all_locusts_spawned.wait()
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

    # # 首页
    # @task(3)
    # class schoolindexTask(TaskSet):
    #
    #     ''' 首页 '''
    #     menu_url = "admin/menu"  # 首页
    #     index_url = "course/school/getHomePageInfo"  # 首页接口
    #     getgetOrgScore = "course/school/getOrgScore"
    #     getCourseScore = "course/school/getCourseScore"
    #
    #     # 获取首页
    #     @task(3)
    #     def get_index(self):
    #         all_locusts_spawned.wait()
    #         # 发起请求
    #         with self.client.get(self.index_url, headers=headers, name='首页get接口', time=10,
    #                              catch_response=True) as response:
    #             # 将接口返回值中的josn提取出来，转为字典
    #             resp_dict = response.json()
    #             print(f'响应数据为{resp_dict}')
    #             # 断言响应状态码
    #             if response.status_code == 200:
    #                 # 请求成功
    #                 print(resp_dict)
    #             else:
    #                 response.failure(resp_dict['msg'])
    #         with self.client.get(self.menu_url, headers=headers, name='首页menu接口', time=10,
    #                              catch_response=True) as response:
    #             # 将接口返回值中的josn提取出来，转为字典
    #             resp_dict = response.json()
    #             print(f'响应数据为{resp_dict}')
    #             # 断言响应状态码
    #             if response.status_code == 200:
    #                 # 请求成功
    #                 print(resp_dict)
    #             else:
    #                 response.failure(resp_dict['msg'])
    #         with self.client.get(self.getgetOrgScore, headers=headers, name='首页getgetOrgScore接口', time=10,
    #                              catch_response=True) as response:
    #             # 将接口返回值中的josn提取出来，转为字典
    #             resp_dict = response.json()
    #             print(f'响应数据为{resp_dict}')
    #             # 断言响应状态码
    #             if response.status_code == 200:
    #                 # 请求成功
    #                 print(resp_dict)
    #             else:
    #                 response.failure(resp_dict['msg'])
    #
    #         with self.client.get(self.getCourseScore, headers=headers, name='首页getCourseScore接口', time=10,
    #                              catch_response=True) as response:
    #             # 将接口返回值中的josn提取出来，转为字典
    #             resp_dict = response.json()
    #             print(f'响应数据为{resp_dict}')
    #             # 断言响应状态码
    #             if response.status_code == 200:
    #                 # 请求成功
    #                 print(resp_dict)
    #             else:
    #                 response.failure(resp_dict['msg'])

    # 课程资源库
    @task(3)
    class getOrgListForSchoolTask(TaskSet):

        ''' 课程资源库 '''
        getOrgListForSchool = "course/rxorgcoursemanage/getOrgListForSchool"
        getInGeneralCategory = "course/rxcoursegeneralcategory/getInGeneralCategory"
        page = "course/rxorgcoursemanage/page"
        getInSubCategory = "course/rxcoursesubclass/getInSubCategory?categoryId=1"
        organizationTeacherSelect = "course/orgTeacher/organizationTeacherSelect"

        @task(2)
        def get_OrgList(self):
            body = {
                "organizationCodes": [],
                "courseCategoryIds": [],
                "orderBys": [
                    {
                        "regCount": "DESC"
                    }
                ],
                "pageNum": 1,
                "pageSize": 10
            }
            all_locusts_spawned.wait()
            with self.client.post(self.page, headers=headers, name='page接口',json=body,
                                  catch_response=True) as response:
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
    host = "https://school.dyketang.com/"  # 设置url
    # 等待时间
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

        current_step = math.floor(run_time / self.setp_time) + 1

        return (current_step * self.setp_load, self.spawn_rate)


if __name__ == '__main__':
    os.system('locust -f test.py')
'''
运行：
    在终端中输入：locust -f 被执行的locust文件.py --host=http://被测服务器域名或ip端口地址
    也可以不指定host
命令执行成功，会提示服务端口，如：*：8089
此时，则可通过浏览器访问机器ip:8089,看到任务测试页面
'''
