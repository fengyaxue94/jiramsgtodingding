import json
import base64
import hashlib
import hmac
import time
import urllib
from jira import JIRA
import datetime
import dingdingmsg
import requests
# 按照领域维度提醒每个领域主pd关于该领域的统计结果信息：产品todo多少，产品待排期，产品已排期分别多少

class JiraParse:
    # 初始化，获取jira的服务器地址信息，登录名、密码
    def __init__(self, name, password, server, project, max_results):
        jira = JIRA(server='http://jira.sunyur.com/', basic_auth=('fengyaxue.fyx', 'feng123456$'))
        self.name = name
        self.password = password
        self.server = server
        self.project = project
        # 查询所有未关闭，未交付解决的业务需求
        self.issuenoslove_jql = 'project = YW AND issuetype = 业务需求 AND status in (草稿, 已排期, 待排期, "方案 todo", "产品 todo")'
        # 查询所有已关闭的需求
        self.closed_jql = 'project = YW AND issuetype = 业务需求 AND status in (关闭, 已交付)'
        # 查询业务需求项目中7天内，产品未排期处理的任务
        self.untreated_jql = 'project = YW AND issuetype = 业务需求 AND status in (待排期, "产品 todo") AND  updated <= -7d ORDER BY updated DESC'
        #'project = {project} AND issuetype = 业务需求 AND resolved >= {today} AND resolved <= {tomorrow}'
        # 1天内新创建的问题
        # self.created_jql = 'project = YW AND issuetype = 业务需求 AND created >= {today}  AND created <= {tomorrow}'
        # 7天内，未排期处理的P0级需求
        self.urgent7_jql = 'project = YW AND issuetype = 业务需求 AND status in (草稿, 待排期, "产品 todo") AND priority = 紧急 AND created >= -7d'
        # 15天内，未排期处理的P1级需求
        self.high15_jql = 'project = YW AND status in (草稿, 待排期, "产品 todo") AND priority = 高  AND issuetype = 业务需求 AND created >= -15d'
        self.max_results = max_results
        self.jira_object = JIRA(server=self.server, basic_auth=(self.name, self.password), options={'verify': False})

    def search_issues(self, jql):
        issues = self.jira_object.search_issues(
            jql_str=jql, maxResults=self.max_results)
        return issues

    def get_issues(self, jql, _dict):
        """
        :param jql:  需要查询的sql
        :param _dict:  放入_dict中，
        :return:  返回该sql计数 sum_issue
        """
        sum_issue = 0
        temp = self.search_issues(jql)
        for each in temp:
            sum_issue += 1
            temp1 = str(each.fields.priority)
            if _dict.get(temp1):
                _dict[temp1] += 1
            else:
                _dict[temp1] = 1

        return sum_issue

    def all_issues(self):
        """
        issue_dict 不确定以后需要不需要，先统计出来放着。
        :return:
        """
        now_time = datetime.datetime.now()
        today = now_time.strftime('%Y-%m-%d')
        tomorrow = (now_time + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        # sum_solved = 0
        # sum_created = 0
        # sum_closed = 0
        issue_dict = dict()
        # 1、self.get_issues(self.solved_jql.format(project=self.project, today=today, tomorrow=tomorrow),issue_dict)
        # 2、self.get_issues(self.created_jql.format(project=self.project, today=today, tomorrow=tomorrow),issue_dict)
        # 3、self.get_issues(self.closed_jql.format(project=self.project, today=today, tomorrow=tomorrow),issue_dict)
        # 查询所有未关闭，未交付解决的业务需求
        sum_issuenoslove = self.get_issues(self.issuenoslove_jql,issue_dict)
        # 查询所有已关闭的需求
        sum_closed = self.get_issues(self.closed_jql,issue_dict)
        # 查询业务需求项目中7天内，产品未排期处理的任务
        sum_untreated = self.get_issues(self.untreated_jql,issue_dict)
        # 'project = {project} AND issuetype = 业务需求 AND resolved >= {today} AND resolved <= {tomorrow}'
        # 1天内新创建的问题
        #sum_created = self.get_issues(self.created_jql,issue_dict)
        # 7天内，未排期处理的P0级需求
        sum_urgent7 = self.get_issues(self.urgent7_jql,issue_dict)
        # 15天内，未排期处理的P1级需求
        sum_high15 = self.get_issues(self.high15_jql,issue_dict)
        # 今日新创建需求： {created} 个issue.\n

        issue_str = '所有已关闭需求： {closed} 个issue.\n' \
                   '7天内产品未排期处理需求：{untreated} 个issue.\n7天内未排期处理的P0级需求： {urgent7} 个issue.\n'\
                   '15天内未排期处理的P1级需求： {high15} 个issue.\n'\
                  '所有未关闭，未交付需求： {issuenoslove} 个issue.\n''\n'.format(closed=sum_closed,untreated=sum_untreated,urgent7=sum_urgent7,high15=sum_high15,issuenoslove=sum_issuenoslove)
        # str1 = '优先级为 {priority} 的Bug共有 {number}个。'
        # for each in bug_dict:
        #     bug_str += str1.format(priority=each, number=bug_dict[each])
        # bug_str += '\n\n'
        return issue_str
# 机器人设置中webhook后的access_token
TOKEN = "e7f4961810af7e5e293ef9aac0f3cf81549925d8b76b4363654ba1b9e88c6db2"
# 安全设置中的秘钥
SECRET = "SECd21b3ec435f9ebbb2c50da01dbf3bfbaa77a6fabebb3eb48e854cbe1f71a564e"
headers = {'Content-Type': 'application/json;charset=utf-8'}

def get_url():
    # 钉钉官方要求，请求的url中必须携带三个参数，access_token， timestamp，sign(签名是由secret加密而来)
    timestamp = str(round(time.time() * 1000))
    #secret = 'this is secret'
    secret_enc = SECRET.encode('utf-8')
    string_to_sign ='{}\n{}'.format(timestamp, SECRET)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    # 完整的url
    api_url = "https://oapi.dingtalk.com/robot/send?access_token={}&timestamp={}&sign={}".format(TOKEN, timestamp, sign)
    return api_url





if __name__ == '__main__':
    name = 'fengyaxue.fyx'
    password = 'feng123456$'
    server = r'http://jira.sunyur.com/'
    project = 'YW'
    max_results = 1000
    atMobiles1 = ['17638163986','13120095528','18221010405']
    j = JiraParse(server=server, name=name, password=password, project=project, max_results=max_results)
    msgtext = j.all_issues()
    dingurls = get_url()
    msgs = {
        "msgtype": "text",
        "text": {
            "content": msgtext

        },
        "at": {
            "atMobiles": [
                "13120095528",
                "18221010405"
            ]
        }
    }
    res = requests.post(dingurls, headers=headers, json=msgs)
