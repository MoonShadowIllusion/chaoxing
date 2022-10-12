import json
from sys import _getframe as getframe
from typing import Optional
from Course import CourseSimple, Course, Knowledge, Card
import pyDes
import requests

debug = True


class LoginFailure(BaseException):
    def __str__(self) -> str:
        return "登陆失败"


class User:
    def __init__(self, username: str, password: str):

        front_func = getframe(1).f_code
        _1 = self.__class__.__name__
        _2 = self.getInstance.__name__
        if front_func.co_name != _2 or front_func.co_names[0] != _1:
            raise Exception(f"请使用 {_1}.{_2} 方法构造用户类")
        else:
            del _1, _2
            self.__session = requests.Session()
            self.__session.headers[
                "User-Agent"] = "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-N976N Build/QP1A.190711.020) (schild:1cbbbd018a6588746eae7fd5af30b357) (device:SM-N976N) Language/zh_CN com.chaoxing.mobile/ChaoXingStudy_3_6.0.4_android_phone_898_97 (@Kalimdor)_28113cfa3b7449f8b8b6c27b94335f23"
            _login_info = {
                "uname": username,
                "code": password
            }
            _login_info = json.dumps(_login_info)

            _login_info = bytearray(_login_info.encode())
            l = 8 - len(_login_info) % 8
            for i in range(l):
                _login_info.append(l)

            _key = "nmnua8WZ8YSgUUirbxxYgaZUCxBxGfAH"[:8]
            _login_info = pyDes.des(_key, mode=pyDes.ECB) \
                .encrypt(bytes(_login_info))
            login_info = ''.join(['%02X' % i for i in _login_info])

            form = {
                "logininfo": login_info,
                "loginType": "1",
                "roleSelect": "true"
            }
            url_1 = "https://passport2-api.chaoxing.com/v11/loginregister"
            params_1 = {
                "cx_xxt_passport": "json"
            }
            try:
                res1 = self.__session.post(url_1, params=params_1, data=form)
                self.__session.get(res1.json()['url'])
            except requests.exceptions.JSONDecodeError:
                raise LoginFailure

    __users: dict[str, 'User'] = {}

    @staticmethod
    def getInstance(username: str, password: str) -> Optional['User']:
        if username in User.__users:
            return User.__users[username]
        else:
            try:
                _ = User(username, password)
                User.__users[username] = _
                return User.__users[username]
            except User.LoginFailure:
                return None

    def getCourseList(self) -> tuple[CourseSimple]:
        url1 = "https://mooc1-api.chaoxing.com/mycourse/backclazzdata"
        params1 = {
            "view": "json",
            "mcode": ""
        }
        res1 = self.__session.get(url1, params=params1).json()
        return tuple(CourseSimple(i) for i in res1['channelList'])

    def getCourse(self, course_simple: CourseSimple):
        url = "https://mooc1-api.chaoxing.com/gas/clazz"
        params = {
            "id": course_simple.id,
            "personid": course_simple.personid,
            "fields": "id,bbsid,classscore,isstart,allowdownload,chatid,name,state,isfiled,visiblescore,begindate,coursesetting.fields(id,courseid,hiddencoursecover,coursefacecheck),course.fields(id,name,infocontent,objectid,app,bulletformat,mappingcourseid,imageurl,teacherfactor,jobcount,knowledge.fields(id,name,indexOrder,parentnodeid,status,layer,label,jobcount,begintime,endtime,attachment.fields(id,type,objectid,extension).type(video)))",
            "view": "json"
        }
        res = self.__session.get(url, params=params)
        return Course(res.json())

    def getKnowledgeCards(self, course: Course, know: Knowledge) -> tuple[Card]:
        # 获取章节下的任务
        url = 'https://mooc1-api.chaoxing.com/gas/knowledge'
        params = {
            "id": know.id,
            "courseid": course.id,
            "fields": "id,parentnodeid,indexorder,label,layer,name,begintime,createtime,lastmodifytime,status,jobUnfinishedCount,clickcount,openlock,card.fields(id,knowledgeid,title,knowledgeTitile,description,cardorder).contentcard(all)",
            "view": "json"
        }
        res = self.__session.get(url, params=params).json()
        _cards = res['data'][0]['card']['data']
        cards = tuple(Card(i) for i in _cards)
        return cards


if __name__ == "__main__":
    a = User.getInstance("", "")
    b = a.getCourseList()
    c = a.getCourse(b[1])
    d = a.getKnowledgeCards(c, c.knowledge[443986930])
    print(d)
