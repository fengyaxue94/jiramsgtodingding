list1 = ["这", "是", "一个", "测试"]
for index, item in enumerate(list1):
    print(index, item)


customers = ['链家', '智联', 'OPPO', '一汽', '三一', '上海电气', '中南', '中烟', '九阳', '保时捷', '大疆', '德邦', '智联', '歌尔声学', '河北烟草', '浙交投','猿辅导', '美团', '花生好车', '长城']

# for i in range(len(customers)):
#     customers[i] = 'project = YW AND issuetype = 业务需求 AND 关联客户 = '+str(customers[i])+' ORDER BY updated DESC'
# print(customers)

# jql = []
# for i,j in enumerate(customers):
#     customers[i] = 'project = YW AND issuetype = 业务需求 AND 关联客户 = ' + str(j) + ' ORDER BY updated DESC'
#     jql.append(customers[i])
#
# print(jql)


jql = ['链家', '智联', 'OPPO', '一汽', '三一', '上海电气', '中南', '中烟', '九阳', '保时捷', '大疆', '德邦', '智联', '歌尔声学', '河北烟草', '浙交投','猿辅导', '美团', '花生好车', '长城']
for i,j in enumerate(customers):
    jql[i] = 'project = YW AND issuetype = 业务需求 AND 关联客户 = ' + str(j) + ' ORDER BY updated DESC'
    #jql.append(customers[i])
print(jql)