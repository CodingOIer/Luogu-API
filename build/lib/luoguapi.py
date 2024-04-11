import requests
import json
import urllib
import random
import time

lang = {
    "C++14 (GCC 9)": 0,
    "Pascal": 1,
    "C": 2,
    "C++98": 3,
    "C++11": 4,
    "Unknown1": 5,
    "Unknown2": 6,
    "Python 3": 7,
    "Java 8": 8,
    "Node.js LTS": 9,
    "Unknown4": 10,
    "C++14": 11,
    "C++17": 12,
    "Ruby": 13,
    "Go": 14,
    "Rust": 15,
    "PHP": 16,
    "C# Mono": 17,
    "Unknown5": 18,
    "Haskell": 19,
    "Unknown6": 20,
    "Kotlin/JVM": 21,
    "Unknown7": 22,
    "Perl": 23,
    "Unknown8": 24,
    "PyPy 3": 25,
    "Unknown9": 26,
    "C++20": 27,
    "C++14 (GCC 9) Copy": 28,
    "Unknown10": 29,
    "OCaml": 30,
    "Julia": 31,
    "Lua": 32,
    "Java 21": 33
}


def urlDecode(code: str):
    return urllib.parse.unquote(code)


def rmb(s: str, t: str):
    index = s.find(t)
    if index == -1:
        return s
    return s[index + len(t):]


def rma(s: str, t: str):
    index = s.find(t)
    if index == -1:
        return s
    return s[:index]


def rmd(s: str, l: str, r: str):
    return rma(rmb(s, l), r)


def ocr(img: list):
    return requests.post(
        "http://ocr.api.codingoier.work/ocr/file", files={'image': img}).text


class session:
    '''
    洛谷用户会话
    '''

    def __init__(self):
        self.uid = ''
        self.client = ''
        self.cookie = ''
        self.user = self.user(self)
        self.problem = self.problem(self)

    def getCsrfToken(self, url='https://www.luogu.com.cn'):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
            'x-luogu-type': 'content-only',
            'cookie': self.cookie,
            'x-requested-with': 'XMLHttpRequest',
        }
        res2 = requests.get(url, headers=headers)
        res2 = res2.text
        csrftoken = res2.split(
            "<meta name=\"csrf-token\" content=\"")[-1].split("\">")[0]
        return csrftoken

    def getHeaders(self, url='https://www.luogu.com.cn'):
        headers = {
            'referer': url,
            'cookie': self.cookie,
            'x-csrf-token': self.getCsrfToken(),
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
        }
        return headers

    class user:
        def __init__(self, session):
            self.session = session

        def makeCookie(self, length: int = 40):
            '''
            随机生成一个 cookie
            @arg length: 随机 cookie 长度
            @return 随机 cookie
            '''
            characters = '0123456789abcdef'
            result = ''.join(random.choice(characters)
                             for _ in range(length))
            return result

        def getCaptcha(self):
            '''
            获取验证码图片
            @return 根据当前 cookie 获取的二进制格式的验证码
            '''
            url = 'https://www.luogu.com.cn/lg4/captcha'
            response = requests.post(
                url=url, headers=self.session.getHeaders('https://luogu.com.cn/auth/login'))
            return response.content

        def loginCookie(self, _uid: str, __client_id: str):
            '''
            使用 _uid 和 __client_id 登录，不校验
            '''
            self.session.uid = _uid
            self.session.client = __client_id
            self.session.cookie = f'__client_id={__client_id};_uid={_uid}'

        def login(self, uid: str, passwd: str):
            '''
            尝试使用账号密码登录
            @arg uid: 用户 uid
            @arg passwd: 用户密码
            @return 如果登录成功返回 [True, username] ，登录失败（验证码错误自动重试）后 [False, <Username Or Password Wrong>]
            '''
            self.loginCookie('0', self.makeCookie())
            res = ocr(self.getCaptcha())
            url = 'https://www.luogu.com.cn/do-auth/password'
            response = requests.post(url=url, headers=self.session.getHeaders(
                'https://www.luogu.com.cn/auth/login'), json={
                "username": uid, "password": passwd, "captcha": res})
            if response.status_code == 200:
                temp = json.loads(response.text)
                self.loginCookie(uid, self.session.client)
                return [True, temp['username']]
            else:
                temp = json.loads(response.text)
                if (temp['errorType'] == 'LuoguWeb\\Spilopelia\\Exception\\CaptchaNotMatchException'):
                    return self.login(uid, passwd)
                else:
                    return [False, 'Username Or Password Wrong']

    class problem:
        def __init__(self, session):
            self.session = session

        def list(self, args: str = ''):
            '''
            获取指定题目列表
            @arg args: 自定义题目筛选参数
            @return 如果成功获取返回 [True, <题目列表 json 格式数据>], 失败返回原因 [False, <Invalid Arguments>]
            '''
            url = f'https://www.luogu.com.cn/problem/list?{args}'
            response = requests.get(
                url=url, headers=self.session.getHeaders(url))
            response = rmd(
                response.text, 'JSON.parse(decodeURIComponent("', '"));')
            response = urlDecode(response)
            response = json.loads(response)
            if response['code'] == 400:
                return [False, 'Invalid Arguments']
            else:
                return [True, response]

        def get(self, uid: str):
            '''
            获取指定题目
            @arg uid: 题目编号
            @return 如果成功获取返回 [True, <题目 json 格式数据>], 失败返回原因 [False, <Problem Not Found>]
            '''
            url = f'https://www.luogu.com.cn/problem/{uid}'
            response = requests.get(
                url=url, headers=self.session.getHeaders(url))
            if response.status_code == 404:
                return [False, 'Problem Not Found']
            response = rmd(
                response.text, 'JSON.parse(decodeURIComponent("', '"));')
            response = urlDecode(response)
            return [True, json.loads(response)]

        def submit(self, uid: str, code: str, lan: str = 'C++14', o2: int = 1):
            '''
            提交代码到指定题目
            @arg uid: 题目编号
            @arg code: 需要提交的代码
            @arg lan: 语言 (为完整 Luogu 界面复制语言)
            @arg o2: 是否开启 O2 优化 (非 C/C++ 语言无效)
            @return 如果成功题解返回 [True, rid], 失败返回原因 [False, <Unknown Language, Problem Not Found>]
            '''
            try:
                if lan[0] != 'C':
                    o2 = 0
                lan = lang[lan]
            except:
                return [False, 'Unknown Language']
            url = f'https://www.luogu.com.cn/fe/api/problem/submit/{uid}'
            h = self.session.getHeaders(
                f'https://www.luogu.com.cn/problem/{uid}')
            response = requests.post(url=url, headers=h, json={
                                     "code": code, "o2": o2, "lang": lan})
            if (response.status_code == 404):
                return [False, 'Problem Not Found']
            response = rmd(
                response.text, 'JSON.parse(decodeURIComponent("', '"));')
            response = urlDecode(response)
            rid = json.loads(response)['rid']
            return [True, rid]

        def solution(self, uid: str):
            '''
            获取指定题目的题解
            @arg uid: 题目编号
            @return 如果成功获取返回 [True, <题解 json 格式数据>], 失败返回原因 [False, <Problem Not Found>]
            '''
            url = f'https://www.luogu.com.cn/problem/solution/{uid}'
            response = requests.get(
                url=url, headers=self.session.getHeaders(url))
            if response.status_code == 404:
                return [False, 'Problem Not Found']
            response = rmd(
                response.text, 'JSON.parse(decodeURIComponent("', '"));')
            response = urlDecode(response)
            return [True, json.loads(response)]
