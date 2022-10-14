import _G
import os
import re
import requests

Session = requests.Session()

RE_VALID_URI_CHAR = r"([a-zA-Z0-9]|\.)"

def init():
    global Session
    Session = requests.Session()
    Session.headers['Authorization'] = os.getenv('NOTION_API_TOKEN')
    Session.headers['Notion-Version'] = os.get_env('NOTION_API_VERSION')
    Session.headers['Content-Type'] = 'application/json'

def stringify(ss):
    ret = ''
    for ch in ss:
        if re.match(RE_VALID_URI_CHAR, ch):
            if ch == '.':
                continue
            ret += ch
    while ret[-1] == '.':
        ret = ret[:-1]
    return ret

TEXT_KEYS = (
    'plain_text', 'name'
)

def get_db(id):
    global Session
    return Session.get(f"https://api.notion.com/v1/databases/{id}/query")

def get_page(id):
    global Session
    return Session.get(f"https://api.notion.com/v1/pages/{id}")

def get_obj_text(obj):
    if obj != 0 and not obj:
        return ''
    elif type(obj) != dict:
        return str(obj)
    
    for t in TEXT_KEYS:
        if t in obj:
            return str(obj[t])
    
    if 'type' not in obj:
        return str(obj)
    
    _type = obj['type']
    if _type in ['title', 'array']:
        ret = ''
        for attr in obj[_type]:
            ret += get_obj_text(attr)
        return ret
    elif _type == 'relation':
        ret = ''
        for rel in obj[_type]:
            page = get_page(rel['id'])
            ret += get_obj_text(page['properties']['Name']) + '\n'
        return ret

    if _type in obj:
        return get_obj_text[_type]
    return str(obj)

def main():
    pass

if __name__ == '__main__':
    init()
    main()