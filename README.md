![1690949620661](https://github.com/resphinas/claude-on-wechat-master/assets/69687075/7a0bfcae-6d77-4b54-9203-5350dfdf3a03)


[![English badge](https://img.shields.io/badge/%E8%8B%B1%E6%96%87-English-blue)](./README_EN.md)

> claude近期以强大的对话和信息整合能力风靡全网，可以写代码、改论文、讲故事，几乎无所不能，这让人不禁有个大胆的想法，能否用他的对话模型把我们的微信打造成一个智能机器人，可以在与好友对话中给出意想不到的回应，而且再也不用担心女朋友影响我们 ~~打游戏~~ 工作了。

原项目网址： https://github.com/zhayujie/chatgpt-on-wechat
本项目将 openai 的 chatgpt 改为了 claude 



## 由于官方接入cloudware反爬，本项目已失效，不再更新！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！

### 1. 提取claude官方参数
https://blog.csdn.net/resphina/article/details/132034037?spm=1001.2014.3001.5501



### 2.运行环境

支持 Linux、MacOS、Windows 系统（可在Linux服务器上长期运行)，同时需安装 `Python`。
> 建议Python版本在 3.7.1~3.9.X 之间，推荐3.8版本，3.10及以上版本在 MacOS 可用，其他系统上不确定能否正常运行。



**(1) 克隆项目代码：**

```bash
git clone https://github.com/resphinas/claude-on-wechat-master
cd claude-on-wechat-master/
```

**(2) 安装核心依赖 (必选)：**
> 能够使用`itchat`创建机器人，并具有文字交流功能所需的最小依赖集合。
```bash
pip3 install -r requirements.txt
```

**(3) 拓展依赖 (可选，建议安装)：**

```bash
pip3 install -r requirements-optional.txt
```

> 如果某项依赖安装失败请注释掉对应的行再继续。





## 配置

配置文件的模板在根目录的`config-template.json`中，需复制该模板创建最终生效的 `config.json` 文件：


然后在`config.json`中填入配置，以下是对默认配置的说明，可根据需要进行自定义修改（请去掉注释）：

```bash
# config.json文件内容示例
改动后 只需填充
  org_uuid  组织uuid
  con_uuid  对话uuid
  cookie  claude聊天时的cookie
  group_name_white_list 微信群白名单列表
  single_chat_reply_prefix  私聊触发前缀
  group_chat_prefix  群聊触发前缀
  
这几个参数即可

```
**配置说明：**

**1.个人聊天**

+ 个人聊天中，需要以 "bot"或"@bot" 为开头的内容触发机器人，对应配置项 `single_chat_prefix` (如果不需要以前缀触发可以填写  `"single_chat_prefix": [""]`)
+ 机器人回复的内容会以 "[bot] " 作为前缀， 以区分真人，对应的配置项为 `single_chat_reply_prefix` (如果不需要前缀可以填写 `"single_chat_reply_prefix": ""`)

**2.群组聊天**

+ 群组聊天中，群名称需配置在 `group_name_white_list ` 中才能开启群聊自动回复。如果想对所有群聊生效，可以直接填写 `"group_name_white_list": ["ALL_GROUP"]`
+ 默认只要被人 @ 就会触发机器人自动回复；另外群聊天中只要检测到以 "@bot" 开头的内容，同样会自动回复（方便自己触发），这对应配置项 `group_chat_prefix`
+ 可选配置: `group_name_keyword_white_list`配置项支持模糊匹配群名称，`group_chat_keyword`配置项则支持模糊匹配群消息内容，用法与上述两个配置项相同。（Contributed by [evolay](https://github.com/evolay))
+ `group_chat_in_one_session`：使群聊共享一个会话上下文，配置 `["ALL_GROUP"]` 则作用于所有群聊


**本说明文档可能会未及时更新，当前所有可选的配置项均在该[`config.py`](https://github.com/zhayujie/chatgpt-on-wechat/blob/master/config.py)中列出。**

## 运行

### 0.必要测试
   claude_api.py 中填写自己的参数信息并且能够正常运行
   文件中部分代码如下
if __name__ == '__main__':
    org_uuid= 此处填写自己的uuid
    con_uuid= 此处填写自己的uuid
    cookie =  此处填写自己的cookie
    main(org_uuid,con_uuid,cookie)

确认运行正常且能接收到claude信息之后继续↓↓↓


### 1.本地运行

如果是开发机 **本地运行**，直接在项目根目录下执行：

```bash
python3 app.py
```
终端输出二维码后，使用微信进行扫码，当输出 "Start auto replying" 时表示自动回复程序已经成功运行了（注意：用于登录的微信需要在支付处已完成实名认证）。扫码登录后你的账号就成为机器人了，可以在微信手机端通过配置的关键词触发自动回复 (任意好友发送消息给你，或是自己发消息给好友)，参考[#142](https://github.com/zhayujie/chatgpt-on-wechat/issues/142)。


### 2.服务器部署

使用nohup命令在后台运行程序：

```bash
touch nohup.out                                   # 首次运行需要新建日志文件  
nohup python3 app.py & tail -f nohup.out          # 在后台运行程序并通过日志输出二维码
```
扫码登录后程序即可运行于服务器后台，此时可通过 `ctrl+c` 关闭日志，不会影响后台程序的运行。使用 `ps -ef | grep app.py | grep -v grep` 命令可查看运行于后台的进程，如果想要重新启动程序可以先 `kill` 掉对应的进程。日志关闭后如果想要再次打开只需输入 `tail -f nohup.out`。此外，`scripts` 目录下有一键运行、关闭程序的脚本供使用。

> **多账号支持：** 将项目复制多份，分别启动程序，用不同账号扫码登录即可实现同时运行。

> **特殊指令：** 用户向机器人发送 **#reset** 即可清空该用户的上下文记忆。

### 3.重要说明
使用中途如需更换claude conversation_uuid等，需要手动将 claude_flag.txt里的数字改为0



## 联系

欢迎提交PR、Issues，以及Star支持一下。程序运行遇到问题可以查看 
