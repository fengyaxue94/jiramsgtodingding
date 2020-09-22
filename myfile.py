# 查询每个项目中状态=方案todo的业务需求数量
self.issuecustomer_schemetodo_jql = 'project = YW AND issuetype = 业务需求 AND status = "方案 todo" AND 关联客户 = ' + str(
    j) + ' ORDER BY updated DESC'

# 查询每个项目中状态=产品todo的业务需求数量
self.issuecustomer_producttodo_jql = 'project = YW AND issuetype = 业务需求 AND status = "产品 todo" AND 关联客户 = ' + str(
    j) + ' ORDER BY updated DESC'

# 查询每个项目中状态=待排期的业务需求数量
self.issuecustomer_waittinglist_jql = 'project = YW AND issuetype = 业务需求 AND status = 待排期 AND 关联客户 = ' + str(
    j) + ' ORDER BY updated DESC'

# 查询每个项目中状态=已排期的业务需求数量
self.issuecustomer_scheduledlist_jql = 'project = YW AND issuetype = 业务需求 AND status = 已排期 AND 关联客户 = ' + str(
    j) + ' ORDER BY updated DESC'

# self.issuecustomer_all_jql
# self.issuecustomer_schemetodo_jql.append('project = YW AND issuetype = 业务需求 AND status = "方案 todo" AND 关联客户 = '+customers[customer]+' ORDER BY updated DESC')
# self.issuecustomer_producttodo_jql.append('project = YW AND issuetype = 业务需求 AND status = "产品 todo" AND 关联客户 = '+customers[customer]+' ORDER BY updated DESC')
# self.issuecustomer_all_jql.append('project = YW AND issuetype = 业务需求 AND 关联客户 = '+customers[customer]+' ORDER BY updated DESC')
# self.issuecustomer_waittinglist_jql.append( 'project = YW AND issuetype = 业务需求 AND status = 待排期 AND 关联客户 = '+customers[customer]+' ORDER BY updated DESC')
# self.issuecustomer_scheduledlist_jql.append('project = YW AND issuetype = 业务需求 AND status = 已排期 AND 关联客户 = '+customers[customer]+' ORDER BY updated DESC')