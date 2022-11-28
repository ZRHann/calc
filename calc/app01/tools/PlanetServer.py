#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socket
import threading  # 导入线程模块
import json

'''
msg: 
{
    type: "login" / "Login Failed"
    username: ""
    players: [
        {
            username: "", 
            x : 0, 
            y : 0, 
        }, 
        
        {
            username: "", 
            x : 0, 
            y : 0, 
        }, 
    ]
}



PLAYERS: 
{
    "user1" : {
        "link": link, 
        "x": x, 
        "y": y, 
    }, 
    
    "user2" : {
        "link": link, 
        "x": x, 
        "y": y, 
    }
}
'''

PLAYERS = {}


def link_handler(link, client):
    """
    该函数为线程需要执行的函数，负责具体的服务器和客户端之间的通信工作
    :param link: 当前线程处理的连接
    :param client: 客户端ip和端口信息，一个二元元组
    :return: None
    """
    print("服务器开始接收来自[%s:%s]的请求...." % (client[0], client[1]))
    while True:  # 利用一个死循环，保持和客户端的通信状态
        data = json.loads(link.recv(1024).decode())
        if data['type'] == "exit":
            print("结束与[%s:%s]的通信..." % (client[0], client[1]))
            break
        print("来自[%s:%s]的客户端发送：%s" % (client[0], client[1], data))
        if data['type'] == "login":
            msg1 = {
                "type": "",
                "username": data["username"],
                "players": []
            }
            if PLAYERS.get(data["username"]):  # 发送登录失败
                msg1["type"] = "Login Failed"
                link.sendall(json.dumps(msg1).encode())
            else:  # 如果登录成功
                PLAYERS[data['username']] = {  # 向PLAYERS添加新玩家
                    "link": link,
                    "x": data["players"][0]["x"],
                    "y": data["players"][0]["y"],
                }
                msg1["type"] = "update"  # 广播更新玩家位置的指令
                for users in PLAYERS.keys():
                    msg1["players"].append({
                        "username": users,
                        "x": PLAYERS[users]["x"],
                        "y": PLAYERS[users]["y"]
                    })
                print('Server广播：', msg1)
                broadcast(json.dumps(msg1))

        elif data['type'] == "update":
            msg1 = {
                "type": "",
                "username": data["username"],
                "players": []
            }
            if not PLAYERS.get(data["username"]):  # 发送没有用户
                msg1["type"] = "Player Not Found"
                link.sendall(json.dumps(msg1).encode())
            else:  # 如果登录成功
                PLAYERS[data['username']] = {  # 向PLAYERS更新玩家
                    "link": link,
                    "x": data["players"][0]["x"],
                    "y": data["players"][0]["y"],
                }
                msg1["type"] = "update"  # 广播更新玩家位置的指令
                for users in PLAYERS.keys():
                    msg1["players"].append({
                        "username": users,
                        "x": PLAYERS[users]["x"],
                        "y": PLAYERS[users]["y"]
                    })
                print('Server广播：', msg1)
                broadcast(json.dumps(msg1))
    link.close()


def broadcast(msg):  # 传入string
    for username, v in PLAYERS.items():
        v["link"].sendall((msg+">>>>>>").encode())


if __name__ == "__main__":
    ip_port = ('172.24.93.205', 2829)
    sk = socket.socket()  # 创建套接字
    sk.bind(ip_port)  # 绑定服务地址
    sk.listen(5)  # 监听连接请求

    print('启动socket服务，等待客户端连接...')

    while True:  # 一个死循环，不断的接受客户端发来的连接请求
        conn, address = sk.accept()  # 等待连接，此处自动阻塞
        # 每当有新的连接过来，自动创建一个新的线程，
        # 并将连接对象和访问者的ip信息作为参数传递给线程的执行函数
        t = threading.Thread(target=link_handler, args=(conn, address))
        t.start()
