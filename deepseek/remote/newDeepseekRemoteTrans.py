import paramiko

def ssh_connect_and_execute(host, port, username, password, command):
    # 创建 SSH 客户端对象
    ssh = paramiko.SSHClient()
    
    # 自动添加服务器的 SSH 密钥到 known_hosts
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # 连接到服务器
        ssh.connect(host, port=port, username=username, password=password)
        
        # 执行命令
        stdin, stdout, stderr = ssh.exec_command(command)
        
        # 获取命令执行的输出
        output = stdout.read().decode()
        error = stderr.read().decode()
        
        
        if error:
            print(f"错误信息: {error}")
    
    except Exception as e:
        print(f"连接或执行命令时出错: {e}")
    finally:
        # 关闭 SSH 连接
        ssh.close()
        
        return output
        
        



def ssh_connect_and_upload_file(host, port, username, password, local_filepath, remote_filepath):
    # 创建 SSH 客户端对象
    ssh = paramiko.SSHClient()

    # 自动添加服务器的 SSH 密钥到 known_hosts
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # 连接到服务器
        ssh.connect(host, port=port, username=username, password=password)
        
        # 使用 SFTP 上传文件
        sftp = ssh.open_sftp()

        # 上传文件
        sftp.put(local_filepath, remote_filepath)
        print(f"文件  成功上传到 {remote_filepath}")
        
        # 关闭 SFTP 会话
        sftp.close()
    
    except Exception as e:
        print(f"连接或上传文件时出错: {e}")
    finally:
        # 关闭 SSH 连接
        ssh.close()


def make_file(con_tent_):
    
    with open("./ciallo.txt","w",encoding="utf-8") as file :
        file.write("请将下面医学相关的英语翻译成中文，要求术语准确，数据无误，深入理解原文的语境和医学逻辑，避免因误解导致的翻译错误，语言流畅，逻辑清晰，风格一致。不要使用markdown格式，直接以文本的形式回答 。 不要说任何多余的话，只需要告诉我翻译的结果。不要说任何多余的话，只需要告诉我翻译的结果。 \n")
        file.writelines(con_tent_)


def trans_deepseek_remote(source) :
    
    make_file(source)


    # 使用示例
    host = 'region-9.autodl.pro'        # 目标服务器地址
    port = 17758                       # SSH 端口（默认是 22）
    username = 'root'      # SSH 登录用户名
    password = 'hwjKhBFWMbNX'      # SSH 登录密码
    command = 'bash -l /root/deepseek/chuli/部署.sh'               # 你要执行的命令


    local_filepath = './ciallo.txt'  # 本地文件路径
    remote_filepath = '/root/deepseek/inference/ciallo2.txt'  # 远程服务器上的文件路径



    ssh_connect_and_upload_file(host, port, username, password, local_filepath, remote_filepath)
    output = ssh_connect_and_execute(host, port, username, password, command)
    
    # print("the output :")
    # print(output)
    # print("end")
    
    parts = output.split('</think>', 1)
    if len(parts) > 1:
        result_ans = parts[1]
    else:
        result_ans = output
        
    
    parts_ = result_ans.split('</lcx_out_mark>', 1)
    if len(parts_) > 1:
        result_ans_ = parts_[0]
    else:
        result_ans_ = result_ans
    
    
    return result_ans_.lstrip("\n")


# afterS = trans_deepseek_remote(" Predicted to enable ATP binding activity and ATP hydrolysis activity. Predicted to be involved in mitochondrion organization. Located in mitochondrion. ")

# print("the ans is")
# print(afterS)

# with open("./zako.txt","w",encoding="utf-8") as file :
#     file.write(afterS)