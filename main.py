from _G import handle_exception, log_error, log_info, log_warning
import os
import re
import requests
import json

Session = requests.Session()

RE_VALID_URI = r"(?!\.)([a-zA-Z0-9]|\.)+"
RE_VALID_URI_CHAR = r"([a-zA-Z0-9]|\.)"

def init():
    global Session
    Session = requests.Session()
    Session.headers['Authorization'] = os.getenv('NOTION_API_TOKEN')
    Session.headers['Notion-Version'] = os.getenv('NOTION_API_VERSION')
    Session.headers['Content-Type'] = 'application/json'

def stringify_url(ss):
    uri = re.search(RE_VALID_URI, ss)
    if not uri:
        return ''
    uri = uri.group()
    ret = ''
    for ch in uri:
        if re.match(RE_VALID_URI_CHAR, ch):
            ret += ch
    while ret[-1] == '.':
        ret = ret[:-1]
    return ret

TEXT_KEYS = (
    'plain_text', 'name'
)

def get_db(id, data={}):
    global Session
    res = Session.post(
        f"https://api.notion.com/v1/databases/{id}/query",
        json.dumps(data)
    )
    ret = {}
    try:
        ret = res.json()
    except Exception as err:
        handle_exception(err)
    return ret

def get_page(id):
    global Session
    res = Session.get(f"https://api.notion.com/v1/pages/{id}")
    ret = {}
    try:
        ret = res.json()
    except Exception as err:
        handle_exception(err)
    return ret

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
    elif _type == 'date':
        da = obj['date']
        if not da:
            return ''
        if da['start'] and da['end']:
            return f"{da['start']} ~ {da['end']}"
        return da['start'] or da['end']
    elif _type == 'relation':
        ret = ''
        for rel in obj[_type]:
            try:
                page = get_page(rel['id'])
                ret += get_obj_text(page['properties']['Name']) + '\n'
            except Exception as err:
                handle_exception(err)
        return ret

    if _type in obj:
        return get_obj_text(obj[_type])
    return str(obj)

def main():
    pass

if __name__ == '__main__':
    init()
    main()