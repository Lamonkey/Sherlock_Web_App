
from requests_html import HTMLSession
def get_status_code(base_url,username):
    session = HTMLSession()
    r = session.get(base_url+username)
    return r

douban = "https://www.douban.com/people/"
username = "unkownuser"
print(get_status_code(douban,username))