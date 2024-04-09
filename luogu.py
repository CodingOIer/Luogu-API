import requests
import json
import urllib

cookie = ''

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


def updateCookie(_uid: str, __client_id: str):
    global cookie
    cookie = f'__client_id={__client_id};_uid={_uid}'


def getCsrfToken(url='https://www.luogu.com.cn'):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
        'x-luogu-type': 'content-only',
        'cookie': cookie,
        'x-requested-with': 'XMLHttpRequest',
    }
    res2 = requests.get(url, headers=headers)
    res2 = res2.text
    csrftoken = res2.split(
        "<meta name=\"csrf-token\" content=\"")[-1].split("\">")[0]
    return csrftoken


def getHeaders(url='https://www.luogu.com.cn'):
    headers = {
        'referer': url,
        'cookie': cookie,
        'x-csrf-token': getCsrfToken(),
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
    }
    return headers


class problem:
    def list(args: str = ''):
        url = f'https://www.luogu.com.cn/problem/list?{args}'
        response = requests.get(url=url, headers=getHeaders(url))
        response = rmd(
            response.text, 'JSON.parse(decodeURIComponent("', '"));')
        response = urlDecode(response)
        return json.loads(response)

    def get(uid: str):
        url = f'https://www.luogu.com.cn/problem/{uid}'
        response = requests.get(url=url, headers=getHeaders(url))
        response = rmd(
            response.text, 'JSON.parse(decodeURIComponent("', '"));')
        response = urlDecode(response)
        return json.loads(response)

    def submit(uid: str, code: str, lang: int = 0, o2: int = 1):
        url = f'https://www.luogu.com.cn/fe/api/problem/submit/{uid}'
        response = requests.post(url=url, headers=getHeaders(
            f'https://www.luogu.com.cn/problem/{uid}'), json={"code": code, "o2": o2, "lang": lang})
        return json.loads(response.text)
