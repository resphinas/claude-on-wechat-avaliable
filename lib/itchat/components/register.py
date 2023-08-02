import datetime
import logging, traceback, sys, threading
import time
from lib import itchat


try:
    import Queue
except ImportError:
    import queue as Queue

from ..log import set_logging
from ..utils import test_connect
from ..storage import templates

logger = logging.getLogger('itchat')





def run_at_noon():
    now = datetime.datetime.now()
    [a,b,c,d] = open("noon_test_time.txt","r").read().split()
    a = int(a)
    b = int(b)
    c = int(c)
    d = int(d)
    if now.hour == 9 and d==1:
        with open("noon_test_time.txt", "w", encoding="utf-8") as file:
            file.write(f"{a} {b} {c} 0")
        return 0
    if now.hour == a :
        if d ==0:
            with open("noon_test_time.txt","w",encoding="utf-8") as file:
                file.write(f"{a} {b} {c} 1")

            return 1

        else:
            return 0
    else:
        return 0


def run_at_minute():
    now = datetime.datetime.now()
    if  now.minute % 30 ==0 and now.second >30 and now.second <35 :
        return 1
    else:
        return 0

def load_register(core):
    core.auto_login       = auto_login
    core.configured_reply = configured_reply
    core.msg_register     = msg_register
    core.run              = run

def auto_login(self, hotReload=False, statusStorageDir='itchat.pkl',
        enableCmdQR=False, picDir=None, qrCallback=None,
        loginCallback=None, exitCallback=None):
    if not test_connect():
        logger.info("You can't get access to internet or wechat domain, so exit.")
        sys.exit()
    self.useHotReload = hotReload
    self.hotReloadDir = statusStorageDir
    if hotReload:
        rval=self.load_login_status(statusStorageDir,
                loginCallback=loginCallback, exitCallback=exitCallback)
        if rval:
            return
        logger.error('Hot reload failed, logging in normally, error={}'.format(rval))
        self.logout()
        self.login(enableCmdQR=enableCmdQR, picDir=picDir, qrCallback=qrCallback,
            loginCallback=loginCallback, exitCallback=exitCallback)
        self.dump_login_status(statusStorageDir)
    else:
        self.login(enableCmdQR=enableCmdQR, picDir=picDir, qrCallback=qrCallback,
            loginCallback=loginCallback, exitCallback=exitCallback)


import pickle

# 将字典保存到文件
def save_dict_to_file(dict_data, file_path):
    with open(file_path, "wb") as file:
        pickle.dump(dict_data, file)

# 从文件中读取字典
def load_dict_from_file(file_path):
    with open(file_path, "rb") as file:
        dict_data = pickle.load(file)
    return dict_data

def configured_reply(self,time_flag,diy_msg):
    ''' determine the type of message and reply if its method is defined
        however, I use a strange way to determine whether a msg is from massive platform
        I haven't found a better solution here
        The main problem I'm worrying about is the mismatching of new friends added on phone
        If you have any good idea, pleeeease report an issue. I will be more than grateful.
    '''


    try:
        msg = self.msgList.get(timeout=1)
    except Queue.Empty:
        pass
    else:
        if isinstance(msg['User'], templates.User):
            replyFn = self.functionDict['FriendChat'].get(msg['Type'])
        elif isinstance(msg['User'], templates.MassivePlatform):
            replyFn = self.functionDict['MpChat'].get(msg['Type'])

        elif isinstance(msg['User'], templates.Chatroom):

            try:
                save_dict_to_file(self.functionDict['GroupChat'], "function_dict.pkl")
                save_dict_to_file(msg, "function_dict1.pkl")
            except:
                pass




            #原始代码
            replyFn = self.functionDict['GroupChat'].get(msg['Type'])
        if replyFn is None:
            r = None
        else:
            try:
                r = replyFn(msg)
                if r is not None:

                    #原始代码
                    self.send(r, msg.get('FromUserName'))
            except:
                logger.warning(traceback.format_exc())

def msg_register(self, msgType, isFriendChat=False, isGroupChat=False, isMpChat=False):
    ''' a decorator constructor
        return a specific decorator based on information given '''
    if not (isinstance(msgType, list) or isinstance(msgType, tuple)):
        msgType = [msgType]
    def _msg_register(fn):
        for _msgType in msgType:
            if isFriendChat:
                self.functionDict['FriendChat'][_msgType] = fn
            if isGroupChat:
                self.functionDict['GroupChat'][_msgType] = fn
            if isMpChat:
                self.functionDict['MpChat'][_msgType] = fn
            if not any((isFriendChat, isGroupChat, isMpChat)):
                self.functionDict['FriendChat'][_msgType] = fn
        return fn
    return _msg_register






def run(self, debug=False, blockThread=True):
    logger.info('Start auto replying.')
    if debug:
        set_logging(loggingLevel=logging.DEBUG)
    def reply_fn():
        try:
            self.last_time =int(time.time())
            while self.alive:
                logging.info("time not equal")
                # print("test")
                current_time = int(time.time())

                self.configured_reply(False,None)
        except KeyboardInterrupt:
            if self.useHotReload:
                self.dump_login_status()
            self.alive = False
            logger.debug('itchat received an ^C and exit.')
            logger.info('Bye~')
    if blockThread:
        reply_fn()
    else:
        replyThread = threading.Thread(target=reply_fn)
        replyThread.setDaemon(True)
        replyThread.start()
