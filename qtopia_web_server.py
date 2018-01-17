from socket import *
import multiprocessing
import re

import mini_WEB

class WEB_Server(object):
    def __init__(self):
        """初始化服务器"""
        # 创建一个服务器套接字
        self.server_soc = socket(AF_INET, SOCK_STREAM)
        # 使得套接字关闭后，端口可以立即释放，立即连接
        self.server_soc.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        # 绑定服务器套接字的ip地址和端口，转为监听状态
        self.server_soc.bind(('', 1314))
        self.server_soc.listen(128)

    def handle_request(self, client_soc):
        # 接收客户端传来的请求
        recv_data = client_soc.recv(1024).decode("utf-8")
        print("客户端文件接收成功：\r\n", recv_data)
        if recv_data:
            # 提取出请求的文件路径
            first_line = recv_data.splitlines()[0]
            content_path = re.match(r'[^/]+(/[^ ]*)', first_line).group(1)

            # 响应请求
            if content_path == '/':
                content_path = "/index.html"
            # 如果搜索的内容路径为.py文件，动态返回，否则静态返回
            if content_path.endswith(".py"):
                # 返回动态数据
                # 空字典
                params_server = dict()
                # 添加一个地址
                params_server['url'] = content_path
                body = mini_WEB.application(params_server, self.set_head_params)
                # 这个是返回一个头数据以后才能拼接
                head = "HTTP/1.1 %s\r\n" % self.stauts
                # 拼接头部
                for temp in self.params:
                    head += "%s:%s\r\n" % (temp[0], temp[1])
                # 拼接响应内容
                content = head + "\r\n" + body
                client_soc.send(content.encode('utf-8'))
            else:
                #返回静态数据
                try:
                    # 获取到文件内容
                    with open('html' + content_path, 'rb') as file:  # 本地文件夹直接找名字，不需要在之前加‘/’
                        content = file.read()
                except:
                    # 文件不存在
                    responce_head = "HTTP/1.1 404 NOT FOUND\r\n"
                    responce_head += 'Content-Type: text/html;charset=utf-8\r\n'
                    responce_head += "\r\n"
                    responce_body = "没有找到内容"
                    client_soc.send(responce_head.encode("utf-8"))
                    client_soc.send(responce_body.encode("utf-8"))
                else:
                    # 返回网页给浏览器
                    responce_head = "HTTP/1.1 200 OK\r\n"
                    responce_head += "\r\n"
                    responce_body = content
                    client_soc.send(responce_head.encode("utf-8"))
                    client_soc.send(responce_body)

        # 关闭子进程p1的客服套接字（主进程中客服套接字的硬链接）
        client_soc.close()

    def run_server(self):
        while True:
            # 等待客户端连接
            print("等待客户端连接")
            client_soc, client_addr = self.server_soc.accept()
            print("客户端连接成功 %s" % client_addr[0])

            # 与客户端进行通信
            # 创建子进程并启动
            p = multiprocessing.Process(target=self.handle_request, args=(client_soc,))
            p.start()
            # 关闭主进程的客服套接字
            client_soc.close()  # 进程是互相独立的，需要也在主进程中关闭套接字

        # # 关闭套接字
        # server_soc.close()

    def set_head_params(self,stauts,params):
        self.stauts = stauts
        self.params = params

def main():
    """服务器主逻辑"""
    # 创建服务器对象
    web_server = WEB_Server()
    # 开启服务器
    web_server.run_server()


if __name__ == '__main__':
    main()
