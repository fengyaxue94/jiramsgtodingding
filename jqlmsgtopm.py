import json
import base64
import hashlib
import hmac
import time
import urllib

import self as self
from jira import JIRA
import requests
# 按照项目维度提醒每个PM关于项目issue的统计信息：方案todo的有多少，产品todo的多少，产品待排期处理的有多少
class JiraParse:
    # 初始化，获取jira的服务器地址信息，登录名、密码
    def __init__(self, name, password, server, project, max_results):
        jira = JIRA(server='http://jira.sunyur.com/', basic_auth=('fengyaxue.fyx', 'feng123456$'))
        self.name = name
        self.password = password
        self.server = server
        self.project = project
        # customer代表不同的租户：链家、智联、OPPO、一汽、三一、上海电气、中南、中烟、九阳、保时捷、大疆、德邦、智联、歌尔声学、河北烟草、浙交投、猿辅导、美团、花生好车、长城
        customers = ['链家','智联','OPPO','一汽','三一','上海电气','中南','中烟','九阳','保时捷','大疆','德邦','歌尔声学','河北烟草','浙交投','猿辅导','美团','花生好车','长城','迈瑞']
        # 根据租户不同查询各个项目的需求处理状态统计情况
        # 定义各个查询语句变量
        # 查询每个项目的所有业务反馈需求数量
        self.issue_lianjia_all_jql = 'project = YW AND issuetype = 业务需求 AND 关联客户 = 链家 ORDER BY updated DESC'
        self.issue_zhilian_all_jql = 'project = YW AND issuetype = 业务需求 AND 关联客户 = 链家 ORDER BY updated DESC'
        self.issue_oppo_all_jql = 'project = YW AND issuetype = 业务需求 AND 关联客户 = 链家 ORDER BY updated DESC'
        self.issue_yiqi_all_jql = 'project = YW AND issuetype = 业务需求 AND 关联客户 = 链家 ORDER BY updated DESC'
        self.issue_sanyi_all_jql = 'project = YW AND issuetype = 业务需求 AND 关联客户 = 链家 ORDER BY updated DESC'
        self.issue_shanghaidianqi_all_jql = 'project = YW AND issuetype = 业务需求 AND 关联客户 = 链家 ORDER BY updated DESC'
        self.issue_zhongnan_all_jql = 'project = YW AND issuetype = 业务需求 AND 关联客户 = 链家 ORDER BY updated DESC'
        self.issue_zhongyan_all_jql = 'project = YW AND issuetype = 业务需求 AND 关联客户 = 链家 ORDER BY updated DESC'
        self.issue_jiuyang_all_jql = 'project = YW AND issuetype = 业务需求 AND 关联客户 = 链家 ORDER BY updated DESC'
        self.issue_baoshijie_all_jql = 'project = YW AND issuetype = 业务需求 AND 关联客户 = 链家 ORDER BY updated DESC'
        self.issue_dajiang_all_jql = 'project = YW AND issuetype = 业务需求 AND 关联客户 = 链家 ORDER BY updated DESC'
        self.issue_debang_all_jql = 'project = YW AND issuetype = 业务需求 AND 关联客户 = 链家 ORDER BY updated DESC'
        self.issue_geershengxue_all_jql = 'project = YW AND issuetype = 业务需求 AND 关联客户 = 链家 ORDER BY updated DESC'
        # 查询每个项目中状态=方案todo的业务需求数量
        self.issuecustomer_schemetodo_jql  = ['链家','智联','OPPO','一汽','三一','上海电气','中南','中烟','九阳','保时捷','大疆','德邦','智联','歌尔声学','河北烟草','浙交投','猿辅导','美团','花生好车','长城']
        # 查询每个项目中状态=产品todo的业务需求数量
        self.issuecustomer_producttodo_jql = ['链家','智联','OPPO','一汽','三一','上海电气','中南','中烟','九阳','保时捷','大疆','德邦','智联','歌尔声学','河北烟草','浙交投','猿辅导','美团','花生好车','长城']
        # 查询每个项目中状态=待排期的业务需求数量
        self.issuecustomer_waittinglist_jql = ['链家','智联','OPPO','一汽','三一','上海电气','中南','中烟','九阳','保时捷','大疆','德邦','智联','歌尔声学','河北烟草','浙交投','猿辅导','美团','花生好车','长城']
        # 查询每个项目中状态=已排期的业务需求数量
        self.issuecustomer_scheduledlist_jql = ['链家','智联','OPPO','一汽','三一','上海电气','中南','中烟','九阳','保时捷','大疆','德邦','智联','歌尔声学','河北烟草','浙交投','猿辅导','美团','花生好车','长城']
        # 通过for循环赋值查询获取各个业务状态下的每个项目的issue查询结果
        for i,j in enumerate(customers):
            self.issuecustomer_all_jql[i] = 'project = YW AND issuetype = 业务需求 AND 关联客户 = '+str(j)+' ORDER BY updated DESC'
            # 获取各个项目业务状态=方案todo的需求情况
            self.issuecustomer_schemetodo_jql[i] ='project = YW AND issuetype = 业务需求 AND status = "方案 todo" AND 关联客户 = ' + str(j) + ' ORDER BY updated DESC'
            # 获取各个项目业务状态=产品todo的需求情况
            self.issuecustomer_producttodo_jql[i] = 'project = YW AND issuetype = 业务需求 AND status = "产品 todo" AND 关联客户 = ' + str(j) + ' ORDER BY updated DESC'
            # 获取各个项目业务状态=待排期的需求情况
            self.issuecustomer_waittinglist_jql[i] ='project = YW AND issuetype = 业务需求 AND status = 待排期 AND 关联客户 = ' + str(j) + ' ORDER BY updated DESC'
            # 获取各个项目业务状态=已排期的需求情况
            self.issuecustomer_scheduledlist_jql[i]  = 'project = YW AND issuetype = 业务需求 AND status = 已排期 AND 关联客户 = ' + str(j) + ' ORDER BY updated DESC'
        print(self.issuecustomer_producttodo_jql)
        print(self.issuecustomer_scheduledlist_jql)
        self.max_results = max_results
        self.jira_object = JIRA(server=self.server, basic_auth=(self.name, self.password),options={'verify': False})
    # 查询issues方法，并返回查询到的issues
    def search_issues(self, jql):
        issues = self.jira_object.search_issues(jql_str=jql, maxResults=self.max_results)
        return issues
    # 获取jql语句查询到的issues
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
            now_time = datetime.datetime.now()
            today = now_time.strftime('%Y-%m-%d')
            tomorrow = (now_time + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
            """
            issue_dict = dict()
            # 1、self.get_issues(self.solved_jql.format(project=self.project, today=today, tomorrow=tomorrow),issue_dict)
            # 2、self.get_issues(self.created_jql.format(project=self.project, today=today, tomorrow=tomorrow),issue_dict)
            # 3、self.get_issues(self.closed_jql.format(project=self.project, today=today, tomorrow=tomorrow),issue_dict)
            # 查询每个项目的所有业务反馈需求
            sum_customer_all = self.get_issues(self.issuecustomer_all_jql, issue_dict)
            # 查询每个项目中状态=方案todo的业务需求
            sum_customer_schemetodo = self.get_issues(self.issuecustomer_schemetodo_jql, issue_dict)
            # 查询每个项目中状态=产品todo的业务需求
            sum_customer_producttodo = self.get_issues(self.issuecustomer_producttodo_jql, issue_dict)
            # 查询每个项目中状态=待排期的业务需求
            sum_customer_waittinglist = self.get_issues(self.issuecustomer_waittinglist_jql, issue_dict)
            # 查询每个项目中状态=已排期的业务需求
            sum_customer_scheduledlist = self.get_issues(self.issuecustomer_scheduledlist_jql, issue_dict)
            issue_str = '租户''所有已反馈业务需求： {customer_all} 个issue.\n' \
                        '状态=方案todo的业务需求：{customer_schemetodo} 个issue.\n \状态=产品todo的业务需求： {producttodo} 个issue.\n' \
                        '状态=待排期的业务需求： {customer_waittinglist} 个issue.\n' \
                        '状态=已排期的业务需求： {customer_scheduledlist} 个issue.\n''\n'.format(customer_all= sum_customer_all, customer_schemetodo=sum_customer_schemetodo,
                                                                           producttodo=sum_customer_producttodo, customer_waittinglist= sum_customer_waittinglist,
                                                                           customer_scheduledlist=sum_customer_scheduledlist)
            # str1 = '优先级为 {priority} 的Bug共有 {number}个。'
            # for each in bug_dict:
            #     bug_str += str1.format(priority=each, number=bug_dict[each])
            # bug_str += '\n\n'
            print(issue_str)
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
                "17638163986"
            ]
        }
    }
    res = requests.post(dingurls, headers=headers, json=msgs)
