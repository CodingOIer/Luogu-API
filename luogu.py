import re
import requests
import json
import urllib

cookie = ''


def urlDecode(code: str):
    return urllib.parse.unquote(code)


def unicodeDecode(s):
    return s.encode().decode('unicode_escape')


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


def formatResult(res):
    pt = r'"__CLASS_NAME":"?([^"\\]*(?:\\.[^"\\]*)*)"?'
    ma = re.findall(pt, res)
    if ma:
        di = {match: match.replace("\\", "\\\\") for match in ma}
        for ol, ne in di.items():
            res = res.replace(ol, ne)
    return res


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


def getGetHeaders(url='https://www.luogu.com.cn'):
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
        response = requests.get(url=url, headers=getGetHeaders(url))
        response = rmd(
            response.text, 'JSON.parse(decodeURIComponent("', '"));')
        response = formatResult(unicodeDecode(urlDecode(response)))
        return json.loads(urlDecode(response))

    def get(uid: str):
        url = f'https://www.luogu.com.cn/problem/{uid}'
        response = requests.get(url=url, headers=getGetHeaders(url))
        response = rmd(
            response.text, 'JSON.parse(decodeURIComponent("', '"));')
        response = formatResult(unicodeDecode(urlDecode(response)))
        return json.loads(urlDecode(response))
