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
        #all_locusts_spawned.wait()
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

    #首页
    @task(3)
    class schoolindexTask(TaskSet):

        ''' 首页 '''
        menu_url = "admin/menu"  # 首页
        index_url = "course/school/getHomePageInfo"  # 首页接口
        getgetOrgScore = "course/school/getOrgScore"
        getCourseScore = "course/school/getCourseScore"

        # 获取首页
        @task(3)
        def get_index(self):
            all_locusts_spawned.wait()
            # 发起请求
            with self.client.get(self.index_url, headers=headers, name='首页get接口', catch_response=True) as response:
                # 将接口返回值中的josn提取出来，转为字典
                resp_dict = response.json()
                print(f'响应数据为{resp_dict}')
                # 断言响应状态码
                if response.status_code == 200:
                    # 请求成功
                    print(resp_dict)
                else:
                    response.failure(resp_dict['msg'])
            #all_locusts_spawned.wait()
            with self.client.get(self.menu_url, headers=headers, name='首页menu接口', catch_response=True) as response:
                # 将接口返回值中的josn提取出来，转为字典
                resp_dict = response.json()
                print(f'响应数据为{resp_dict}')
                # 断言响应状态码
                if response.status_code == 200:
                    # 请求成功
                    print(resp_dict)
                else:
                    response.failure(resp_dict['msg'])
            with self.client.get(self.getgetOrgScore, headers=headers, name='首页getgetOrgScore接口', catch_response=True) as response:
                # 将接口返回值中的josn提取出来，转为字典
                resp_dict = response.json()
                print(f'响应数据为{resp_dict}')
                # 断言响应状态码
                if response.status_code == 200:
                    # 请求成功
                    print(resp_dict)
                else:
                    response.failure(resp_dict['msg'])

            with self.client.get(self.getCourseScore, headers=headers, name='首页getCourseScore接口', catch_response=True) as response:
                # 将接口返回值中的josn提取出来，转为字典
                resp_dict = response.json()
                print(f'响应数据为{resp_dict}')
                # 断言响应状态码
                if response.status_code == 200:
                    # 请求成功
                    print(resp_dict)
                else:
                    response.failure(resp_dict['msg'])



    #课程资源库
    @task(2)
    class getOrgListForSchoolTask(TaskSet):

        ''' 课程资源库 '''
        getOrgListForSchool = "course/rxorgcoursemanage/getOrgListForSchool"
        getInGeneralCategory = "course/rxcoursegeneralcategory/getInGeneralCategory"
        page = "course/rxorgcoursemanage/page"
        getInSubCategory = "course/rxcoursesubclass/getInSubCategory?categoryId=1"
        organizationTeacherSelect = "course/orgTeacher/organizationTeacherSelect"

        @task(2)
        def get_OrgList(self):
            getdata = {"organizationCodes": [], "courseCategoryIds": [], "orderBys": [{"regCount": "DESC"}],
                       "pageNum": 1, "pageSize": 10}
            all_locusts_spawned.wait()
            # 发起请求
            with self.client.get(self.getOrgListForSchool, headers=headers, name='getOrgListForSchool接口', catch_response=True) as response:
                # 将接口返回值中的josn提取出来，转为字典
                resp_dict = response.json()
                print(f'响应数据为{resp_dict}')
                # 断言响应状态码
                if response.status_code == 200:
                    # 请求成功
                    print(resp_dict)
                else:
                    response.failure(resp_dict['msg'])
            with self.client.get(self.getInGeneralCategory, headers=headers, name='getInGeneralCategory接口',  catch_response=True) as response:
                # 将接口返回值中的josn提取出来，转为字典
                resp_dict = response.json()
                print(f'响应数据为{resp_dict}')
                # 断言响应状态码
                if response.status_code == 200:
                    # 请求成功
                    print(resp_dict)
                else:
                    response.failure(resp_dict['msg'])
            with self.client.post(self.page, headers=headers, name='page接口', json=getdata, catch_response=True) as response:
                # 将接口返回值中的josn提取出来，转为字典
                resp_dict = response.json()
                print(f'响应数据为{resp_dict}')
                # 断言响应状态码
                if response.status_code == 200:
                    # 请求成功
                    print(resp_dict)
                else:
                    response.failure(resp_dict['msg'])
            with self.client.get(self.getInSubCategory, headers=headers, name='getInSubCategory接口',
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
            with self.client.get(self.organizationTeacherSelect, headers=headers, name='organizationTeacherSelect接口',
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

#课程管理
    @task(2)
    class SchoolCourseTask(TaskSet):

        ''' 课程管理 '''
        getRxSchoolCourseStatistics = "course/rxschoolcourse/getRxSchoolCourseStatistics"
        rxschoolcourse_page = "course/rxschoolcourse/page?pageNum=1&pageSize=10"
        getInSubCategory = "course/rxcoursesubclass/getInSubCategory?categoryId=5"
        organizationTeacherSelect = "course/orgTeacher/organizationTeacherSelect"

        @task(2)
        def get_SchoolCourse(self):
            all_locusts_spawned.wait()
            # 发起请求
            with self.client.get(self.getRxSchoolCourseStatistics, headers=headers, name='getRxSchoolCourseStatistics接口', catch_response=True) as response:
                # 将接口返回值中的josn提取出来，转为字典
                resp_dict = response.json()
                print(f'响应数据为{resp_dict}')
                # 断言响应状态码
                if response.status_code == 200:
                    # 请求成功
                    print(resp_dict)
                else:
                    response.failure(resp_dict['msg'])
            with self.client.get(self.rxschoolcourse_page, headers=headers, name='rxschoolcourse_page', catch_response=True) as response:
                # 将接口返回值中的josn提取出来，转为字典
                resp_dict = response.json()
                print(f'响应数据为{resp_dict}')
                # 断言响应状态码
                if response.status_code == 200:
                    # 请求成功
                    print(resp_dict)
                else:
                    response.failure(resp_dict['msg'])
            with self.client.get(self.getInSubCategory, headers=headers, name='getInSubCategory接口',
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
            with self.client.get(self.organizationTeacherSelect, headers=headers, name='organizationTeacherSelect接口',
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

#报名信息
    @task(2)
    class StudentRegTask(TaskSet):

        ''' 报名信息 '''
        series = "course/afterClass/series"
        getRxSchoolStudentRegStatistics = "course/rxschoolstudentreg/getRxSchoolStudentRegStatistics"
        rxschoolstudentreg = "course/rxschoolstudentreg/page?pageNum=1&pageSize=10"

        @task(2)
        def get_StudentReg(self):
            all_locusts_spawned.wait()
            # 发起请求
            with self.client.get(self.series, headers=headers, name='series', catch_response=True) as response:
                # 将接口返回值中的josn提取出来，转为字典
                resp_dict = response.json()
                print(f'响应数据为{resp_dict}')
                # 断言响应状态码
                if response.status_code == 200:
                    # 请求成功
                    print(resp_dict)
                else:
                    response.failure(resp_dict['msg'])
            with self.client.get(self.getRxSchoolStudentRegStatistics, headers=headers, name='getRxSchoolStudentRegStatistics', catch_response=True) as response:
                # 将接口返回值中的josn提取出来，转为字典
                resp_dict = response.json()
                print(f'响应数据为{resp_dict}')
                # 断言响应状态码
                if response.status_code == 200:
                    # 请求成功
                    print(resp_dict)
                else:
                    response.failure(resp_dict['msg'])
            with self.client.get(self.rxschoolstudentreg, headers=headers, name='rxschoolstudentreg',
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

#班级管理
    @task(2)
    class ClassTask(TaskSet):

        ''' 班级管理 '''
        schoolCourseSelect = "course/rxschoolcourse/schoolCourseSelect"
        getRxSchoolClassStatistics = "course/schoolclass/getRxSchoolClassStatistics"
        schoolclass = "course/schoolclass/page?pageNum=1&pageSize=10"
        detail = "course/schoolclass/detail/1473231630742052866"
        organizationTeacherSelectForSchool_courseCode = "course/orgTeacher/organizationTeacherSelectForSchool?courseCode=KC00000012"
        organizationTeacherSelectForSchool = "course/orgTeacher/organizationTeacherSelectForSchool"
        schoolClassRoomSelect = "course/rxschoolclassroom/schoolClassRoomSelect"


        @task(2)
        def get_Class(self):
            all_locusts_spawned.wait()
            # 发起请求
            with self.client.get(self.schoolCourseSelect, headers=headers, name='schoolCourseSelect', catch_response=True) as response:
                # 将接口返回值中的josn提取出来，转为字典
                resp_dict = response.json()
                print(f'响应数据为{resp_dict}')
                # 断言响应状态码
                if response.status_code == 200:
                    # 请求成功
                    print(resp_dict)
                else:
                    response.failure(resp_dict['msg'])
            with self.client.get(self.getRxSchoolClassStatistics, headers=headers, name='getRxSchoolClassStatistics', catch_response=True) as response:
                # 将接口返回值中的josn提取出来，转为字典
                resp_dict = response.json()
                print(f'响应数据为{resp_dict}')
                # 断言响应状态码
                if response.status_code == 200:
                    # 请求成功
                    print(resp_dict)
                else:
                    response.failure(resp_dict['msg'])
            with self.client.get(self.schoolclass, headers=headers, name='schoolclass',
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
            with self.client.get(self.detail, headers=headers, name='detail',
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
            with self.client.get(self.organizationTeacherSelectForSchool_courseCode, headers=headers, name='organizationTeacherSelectForSchool_courseCode',
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
            with self.client.get(self.organizationTeacherSelectForSchool, headers=headers, name='organizationTeacherSelectForSchool',
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
            with self.client.get(self.schoolClassRoomSelect, headers=headers, name='schoolClassRoomSelect',
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

#课表管理
    @task(2)
    class CourseTableTask(TaskSet):

        ''' 班级管理 '''
        schoolCourseSelect = "course/rxschoolcourse/schoolCourseSelect"
        classSelect = "course/schoolClass/classSelect"
        organizationTeacherSelectForSchool = "course/orgTeacher/organizationTeacherSelectForSchool"
        schoolTeacherSelect = "course/rxschoolteacher/schoolTeacherSelect"
        schoolClassRoomSelect = "course/rxschoolclassroom/schoolClassRoomSelect"
        getOrgList = "course/rxorgcoursemanage/getOrgList"
        listCourseTable = "course/school/listCourseTable"


        @task(2)
        def get_CourseTable(self):
            all_locusts_spawned.wait()
            # 发起请求
            with self.client.get(self.schoolCourseSelect, headers=headers, name='schoolCourseSelect', catch_response=True) as response:
                # 将接口返回值中的josn提取出来，转为字典
                resp_dict = response.json()
                print(f'响应数据为{resp_dict}')
                # 断言响应状态码
                if response.status_code == 200:
                    # 请求成功
                    print(resp_dict)
                else:
                    response.failure(resp_dict['msg'])
            with self.client.get(self.classSelect, headers=headers, name='classSelect', catch_response=True) as response:
                # 将接口返回值中的josn提取出来，转为字典
                resp_dict = response.json()
                print(f'响应数据为{resp_dict}')
                # 断言响应状态码
                if response.status_code == 200:
                    # 请求成功
                    print(resp_dict)
                else:
                    response.failure(resp_dict['msg'])
            with self.client.get(self.organizationTeacherSelectForSchool, headers=headers, name='organizationTeacherSelectForSchool',
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
            with self.client.get(self.schoolTeacherSelect, headers=headers, name='schoolTeacherSelect',
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
            with self.client.get(self.schoolClassRoomSelect, headers=headers, name='schoolClassRoomSelect',
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
            with self.client.get(self.getOrgList, headers=headers, name='getOrgList',
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
            with self.client.get(self.listCourseTable, headers=headers, name='listCourseTable',
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

#订单管理
    @task(2)
    class orderTask(TaskSet):

        ''' 订单管理 '''
        getAllCourseOrderStatistics = "order/orderMain/getAllCourseOrderStatistics"
        orderMain = "order/orderMain/page?pageNum=1&pageSize=10"

        @task(2)
        def get_order(self):
            all_locusts_spawned.wait()
            # 发起请求
            with self.client.get(self.getAllCourseOrderStatistics, headers=headers, name='getAllCourseOrderStatistics', catch_response=True) as response:
                # 将接口返回值中的josn提取出来，转为字典
                resp_dict = response.json()
                print(f'响应数据为{resp_dict}')
                # 断言响应状态码
                if response.status_code == 200:
                    # 请求成功
                    print(resp_dict)
                else:
                    response.failure(resp_dict['msg'])
            with self.client.get(self.orderMain, headers=headers, name='orderMain', catch_response=True) as response:
                # 将接口返回值中的josn提取出来，转为字典
                resp_dict = response.json()
                print(f'响应数据为{resp_dict}')
                # 断言响应状态码
                if response.status_code == 200:
                    # 请求成功
                    print(resp_dict)
                else:
                    response.failure(resp_dict['msg'])
#老师管理
    @task(2)
    class TeacherTask(TaskSet):

        ''' 老师管理 '''
        getAllTeacherStatistics = "course/getAllTeacherStatistics"
        rxschoolteacher = "course/rxschoolteacher/page?pageNum=1&pageSize=10"
        rxschoolteacher_put = "course/rxschoolteacher"


        @task(2)
        def get_Teacher(self):
            teacher_data = {"id":"1473219291137433602",
                            "createdBy":"20211115101345",
                            "createdTime":"2021-12-21 17:10:25",
                            "modifiedBy":"",
                            "modifiedTime":"2021-12-21 17:10:24",
                            "remark":"",
                            "schoolCode":"20211115101345",
                            "sysUserCode":"ST202112210204",
                            "teacherCode":"7218",
                            "teacherName":"王小凡",
                            "sex":1,
                            "idCard":"430702197512239529",
                            "phone":"18932345678",
                            "teachSubject":"历史",
                            "userStatus":0}
            all_locusts_spawned.wait()
            # 发起请求
            with self.client.get(self.getAllTeacherStatistics, headers=headers, name='getAllTeacherStatistics', catch_response=True) as response:
                # 将接口返回值中的josn提取出来，转为字典
                resp_dict = response.json()
                print(f'响应数据为{resp_dict}')
                # 断言响应状态码
                if response.status_code == 200:
                    # 请求成功
                    print(resp_dict)
                else:
                    response.failure(resp_dict['msg'])
            with self.client.get(self.rxschoolteacher, headers=headers, name='rxschoolteacher', catch_response=True) as response:
                # 将接口返回值中的josn提取出来，转为字典
                resp_dict = response.json()
                print(f'响应数据为{resp_dict}')
                # 断言响应状态码
                if response.status_code == 200:
                    # 请求成功
                    print(resp_dict)
                else:
                    response.failure(resp_dict['msg'])
            with self.client.put(self.rxschoolteacher_put, headers=headers, name='rxschoolteacher_put', json=teacher_data,
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
    host = "https://school.dyketang.com/" #设置url
    #等待时间
    wait_time = between(1, 2)

# class StepLoadShaper(LoadTestShape):
#     '''
#         step_time -- 逐步加载时间长度
#         step_load -- 用户每一步增加的量
#         spawn_rate -- 用户在每一步的停止/启动的多少用户数
#         time_limit -- 时间限制压测的执行时长
#     '''
#
#     # 逐步负载策略每隔30秒新增启动10个用户
#     setp_time = 30
#     setp_load = 10
#     spawn_rate = 10
#     time_limit = 300
#
#     def tick(self):
#         run_time = self.get_run_time()
#
#         if run_time > self.time_limit:
#             return None
#         current_step = math.floor(run_time /self.setp_time) +1
#         return(current_step * self.setp_load,self.spawn_rate)

if __name__ == '__main__':
    os.system('locust -f school.py')
'''
运行：
    在终端中输入：locust -f 被执行的locust文件.py --host=http://被测服务器域名或ip端口地址
    也可以不指定host
命令执行成功，会提示服务端口，如：*：8089
此时，则可通过浏览器访问机器ip:8089,看到任务测试页面
'''