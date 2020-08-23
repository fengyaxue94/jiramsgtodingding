import string

customers = ['链家', '智联', 'OPPO', '一汽', '三一', '上海电气', '中南', '中烟', '九阳', '保时捷', '大疆', '德邦', '智联', '歌尔声学', '河北烟草', '浙交投','猿辅导', '美团', '花生好车', '长城']
for customer in range(len(customers)):
    # 查询每个项目的所有业务反馈需求数量
    test= '我是'+customers[customer]+'项目'

    #stest.append('我是'+customers[customer]+'项目')
    test.split(",")
    print(test)