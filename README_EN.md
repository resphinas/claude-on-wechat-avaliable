# Introduction

Recently, Claude has become popular for its powerful dialogue and information integration capabilities. It can write code, edit papers, and tell stories, making people wonder whether we can use its dialogue model to turn our WeChat into an intelligent robot that can provide unexpected responses in conversations with friends. Now, we no longer have to worry about our girlfriend interrupting our work while we play games.

Original Project URL: https://github.com/zhayujie/chatgpt-on-wechat
This project modifies the openai's chatgpt to Claude.

## Preparation

### 1. Extracting Official Parameters for Claude
https://blog.csdn.net/resphina/article/details/132034037?spm=1001.2014.3001.5501

### 2. Operating Environment

Supports Linux, MacOS, and Windows systems (can be run on Linux servers for long-term use) and requires installation of `Python`.
> Python version between 3.7.1 and 3.9.X is recommended, with 3.8 being preferred. Version 3.10 and above should work on MacOS, but it's uncertain whether they can run smoothly on other systems.

**(1) Clone the Project Code:**

```bash
git clone https://github.com/resphinas/claude-on-wechat-master
cd claude-on-wechat-master/
```

**(2) Install Core Dependencies (Required):**
> Minimum set of dependencies needed to use `itchat` to create the bot and enable text interactions.

```bash
pip3 install -r requirements.txt
```

**(3) Install Optional Dependencies (Recommended):**

```bash
pip3 install -r requirements-optional.txt
```

> If any dependency installation fails, comment out the corresponding line and continue.

## Configuration

The template of the configuration file is in `config-template.json` at the root directory. Copy this template to create the final `config.json` file:

Then fill in the configuration in `config.json`. Below is an explanation of the default configuration, which can be customized as needed (please remove the comments):

```bash
# Example content of config.json
Just fill in the following parameters:
   org_uuid
  con_uuid
  cookie
  group_name_white_list
  single_chat_reply_prefix
  group_chat_prefix
  
```

**Configuration Explanation:**

**1. Individual Chat**

+ In individual chat, the bot needs to be triggered by messages starting with "bot" or "@bot", corresponding to the configuration item `single_chat_prefix` (If no prefix is required, you can set `"single_chat_prefix": [""]`).
+ The bot's reply will be prefixed with "[bot]" to distinguish from human responses. The configuration item for this is `single_chat_reply_prefix` (If no prefix is needed, you can set `"single_chat_reply_prefix": ""`).

**2. Group Chat**

+ In group chats, the group name needs to be configured in `group_name_white_list` for the auto-reply to work. If you want it to work for all group chats, you can directly set `"group_name_white_list": ["ALL_GROUP"]`.
+ By default, the bot will be triggered by being mentioned with "@". Additionally, if a message starts with "@bot", it will also trigger the bot's response (to easily trigger it yourself). This corresponds to the configuration item `group_chat_prefix`.
+ Optional Configuration: `group_name_keyword_white_list` supports fuzzy matching of group names, and `group_chat_keyword` supports fuzzy matching of group message contents. Their usage is the same as the above two configuration items. (Contributed by [evolay](https://github.com/evolay))
+ `group_chat_in_one_session`: Makes group chats share one session context. Setting `["ALL_GROUP"]` applies to all group chats.

**3. Speech Recognition**

+ Adding `"speech_recognition": true` will enable speech recognition, which uses the openai whisper model to convert speech to text and reply in text. This option is only available for private chat (note that since speech messages cannot match the prefix, once enabled, the bot will automatically reply to all voice messages and support voice-triggered drawing).
+ Adding `"group_speech_recognition": true` will enable speech recognition for group chats, using the openai whisper model to convert speech to text and reply in text. This option is only available for group chats (it will match `group_chat_prefix` and `group_chat_keyword`, and support voice-triggered drawing).
+ Adding `"voice_reply_voice": true` will enable voice-to-voice replies (both for private chat and group chat), but you need to configure the corresponding speech synthesis platform key. Due to itchat's protocol limitations, only voice mp3 files can be sent. If using WeChaty, the reply will be a WeChat voice message.

**Please note that this documentation may not be updated in a timely manner. All currently available optional configuration items are listed in this [`config.py`](https://github.com/zhayujie/chatgpt-on-wechat/blob/master/config.py).**

## Running

### 1. Local Run

If running **locally** on a development machine, simply execute in the project root directory:

```bash
python3 app.py
```
After the QR code is displayed in the terminal, use WeChat to scan it. When "Start auto replying" is output, it means the automatic reply program is running successfully (note that the WeChat account used for login needs to have completed real-name authentication at the payment stage). After scanning the code to log in, your account becomes a bot and can automatically reply to messages triggered by configured keywords in WeChat on the mobile phone (any friend sending you a message, or you sending a message to a friend), refer to [#142](https://github.com/zhayujie/chatgpt-on-wechat/issues/142).

### 2. Server Deployment

Use the nohup command to run the program in the background:

```bash
touch nohup.out                                   # Create a log file for the first run
nohup python3 app.py & tail -f nohup.out          # Run the program in the background and output the QR code in the log
```
After scanning the code to log in, the program can run in the background on the server. At this point, you can close the log with `ctrl+c` without affecting the operation of the background program. You can use the command `ps -ef | grep app.py | grep -v grep` to view the background processes. If you want to restart the program, you can first `kill` the corresponding process. If you want to reopen the log after closing it, just type `tail -f nohup.out`. Additionally, there are scripts in the `scripts` directory for one-click running and closing of the program.

> **Multi-Account Support:** Copy the project multiple times and start the program separately, using different accounts to scan the code for simultaneous operation.

> **Special Instructions:** Send **#reset** to the bot to clear the user's context memory.

## Contact

Welcome to submit PRs, issues, and give it a Star to show support. If you encounter any problems during program execution, you can check [the documentation](https://github.com/zhayujie/chatgpt-on-wechat/blob/master/docs/FAQ.md).
