import requests
import json
import urllib
import random
import imageio
import time
from PIL import Image

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


class session:

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
            characters = '0123456789abcdef'
            result = ''.join(random.choice(characters)
                             for _ in range(length))
            print(result)
            return result

        def getCaptcha(self):
            url = 'https://www.luogu.com.cn/lg4/captcha'
            response = requests.post(
                url=url, headers=self.session.getHeaders('https://luogu.com.cn/auth/login'))
            stream = response.content
            img = imageio.imread(stream, format='PNG')
            imageio.imsave('output.png', img)
            pass

        def loginCookie(self, _uid: str, __client_id: str):
            self.session.uid = _uid
            self.session.client = __client_id
            self.session.cookie = f'__client_id={__client_id};_uid={_uid}'

        def login(self, uid: str, passwd: str):
            self.loginCookie('0', self.makeCookie())
            self.getCaptcha()
            img = Image.open('output.png')
            img.show()
            res = input('input captcha: ')
            url = 'https://www.luogu.com.cn/do-auth/password'
            h = self.session.getHeaders(
                'https://www.luogu.com.cn/auth/login')
            response = requests.post(url=url, headers=h, json={
                                     "username": uid, "password": passwd, "captcha": res})
            if response.status_code == 200:
                return [True, None]
            else:
                temp = json.dumps(response.text())
                return [False, temp['errorType']]

    class problem:
        def __init__(self, session):
            self.session = session

        def list(self, args: str = ''):
            url = f'https://www.luogu.com.cn/problem/list?{args}'
            response = requests.get(
                url=url, headers=self.session.getHeaders(url))
            response = rmd(
                response.text, 'JSON.parse(decodeURIComponent("', '"));')
            response = urlDecode(response)
            return json.loads(response)

        def get(self, uid: str):
            url = f'https://www.luogu.com.cn/problem/{uid}'
            response = requests.get(
                url=url, headers=self.session.getHeaders(url))
            response = rmd(
                response.text, 'JSON.parse(decodeURIComponent("', '"));')
            response = urlDecode(response)
            return json.loads(response)

        def submit(self, uid: str, code: str, lang: int = 0, o2: int = 1):
            url = f'https://www.luogu.com.cn/fe/api/problem/submit/{uid}'
            response = requests.post(url=url, headers=self.session.getHeaders(
                f'https://www.luogu.com.cn/problem/{uid}'), json={"code": code, "o2": o2, "lang": lang})
            return json.loads(response.text)
