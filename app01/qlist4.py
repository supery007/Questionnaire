#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:supery

q_list = [
    {'pid': '1', 'title': '你对教室网络情况打分', 'type': '1'},
    {'pid': '2', 'title': '对苑浩老师进行评价', 'type': '3'},
    {'pid': '3', 'title': 'Form难不难？', 'type': '2',
     'options':
         [
             {'id': '4', 'title': 'A.难', 'val': '8'},
             {'id': '5', 'title': 'B.真鸡儿不好用', 'val': '10'}
         ]
     },
    {'pid': '4', 'title': 'ModelForm难不难？', 'type': '2',
     'options':
         [
             {'id': '1', 'title': 'A.难', 'val': '7'},
             {'id': '2', 'title': 'B.真难', 'val': '9'},
             {'id': '3', 'title': 'C.真鸡儿难', 'val': '10'}
         ]
     },
    {'pid': '', 'title': '真鸡儿麻烦', 'type': '3'},
    {'pid': '', 'title': '开发好不好学', 'type': '2','options':
         [
             {'id': '1', 'title': 'A.一般', 'val': '5'},
             {'id': '2', 'title': 'B.难', 'val': '9'},
             {'id': '3', 'title': 'C.真JB难', 'val': '10'}
         ]
     }
]
for que in q_list:
    pid = que.get('pid')
    type = que.get('type')
    options = que.get('options')
    if not pid:
        if type == '2':
            for op in options:
                pass
                # 关联选项
                # print(op)
    else:
        # print(que)
        if type=='2':
            # print(que)
            for op in options:
                # print(op)
                pass
        else:
            print(que)
