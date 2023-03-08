import winreg
import pickle

class RegisterItem:
    def __init__(self, name, data):
        self.is_init = False
        self.data = data
        self.name = name
        self.next = []
        self.last = []

    def __str__(self):
        last_ = [i.name for i in self.last]
        next_ = [i.name for i in self.next]
        return "{name:%s, last:%s, next:%s}" % (str(self.name), str(last_), str(next_))


REGISTER_VALUE_DICT = dict()
REGISTER_KEY_DICT = dict()
REGISTER_NAME_DICT = dict()

def str1(m:list):
    s = '["'
    for k in m:
        s += str(k)
        s += ', '
    return s + "]"


def str_(m: dict):
    if len(m) == 0:
        return "{}"
    s = '''{"'''
    for k in m:
        s += str(k)
        s += '''":"'''
        if type(m[k]) == list:
            s += str1(m[k])
        else:
            s += str(m[k])
        s += '''", '''
    return s[:-2] + " }"


def data_register(name, data):
    global REGISTER_VALUE_DICT
    global REGISTER_NAME_DICT
    global REGISTER_KEY_DICT
    if name in REGISTER_NAME_DICT:
        new_item = REGISTER_NAME_DICT[name]
        for d in data:
            if new_item.data.get(d) is None:
                new_item.data[d] = data[d]
            elif type(new_item.data.get(d)) == list:
                new_item.data[d].append(data[d])
            else:
                new_item.data[d] = [new_item.data[d], data[d]]
    else:
        new_item = RegisterItem(name, data)
        REGISTER_NAME_DICT[name] = new_item
    for d in data:
        if d != "":
            if d in REGISTER_NAME_DICT:
                new_item.next.append(REGISTER_NAME_DICT[d])
                REGISTER_NAME_DICT[d].last.append(new_item)
            if d in REGISTER_VALUE_DICT:
                for new_item in REGISTER_VALUE_DICT[d]:
                    new_item.next.append(new_item)
                    new_item.last.append(new_item)
            try:
                REGISTER_KEY_DICT[d].append(new_item)
            except:
                REGISTER_KEY_DICT[d] = [new_item]

        v = data[d]
        if v != "":
            if v in REGISTER_NAME_DICT:
                new_item.next.append(REGISTER_NAME_DICT[v])
                REGISTER_NAME_DICT[v].last.append(new_item)
            if v in REGISTER_KEY_DICT:
                for new_item in REGISTER_KEY_DICT[v]:
                    new_item.last.append(new_item)
                    new_item.next.append(new_item)
            try:
                REGISTER_VALUE_DICT[d].append(new_item)
            except:
                REGISTER_VALUE_DICT[d] = [new_item]


def register_item_get_data(register_key):
    index__ = 0
    data = {}
    while True:
        try:
            (key, value, format) = winreg.EnumValue(register_key, index__)
            data[key] = value
            index__ += 1
        except:
            return data


def read_straight(key_handle, key_name):
    if key_name is None:
        open_key = key_handle
    else:
        try:
            open_key = winreg.OpenKey(key_handle, key_name)
        except:
            return
    index_ = 0
    while True:
        data = register_item_get_data(open_key)
        if key_name is None:
            name = "HKLM"
        else:
            name = key_name.split('\\')[-1]
        data_register(name, data)
        try:
            new_key_name = winreg.EnumKey(open_key, index_)
            index_ += 1
            if key_name is None:
                read_straight(key_handle, new_key_name)
            else:
                read_straight(key_handle, key_name + "\\" + new_key_name)
        except:
            if open_key in [winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_USERS, winreg.HKEY_CURRENT_CONFIG]:
                return
            open_key.Close()
            return


def read_by_file():
    pass


if __name__ == '__main__':
    read_straight(winreg.HKEY_LOCAL_MACHINE, None)
    with open("HKLM_REGISTER_VALUE_DICT.txt", "wb") as writer:
        pickle.dump(REGISTER_VALUE_DICT, writer)
    with open("HKLM_REGISTER_KEY_DICT.txt", "wb") as writer:
        pickle.dump(REGISTER_KEY_DICT, writer)
    with open("HKLM_REGISTER_NAME_DICT.txt", "wb") as writer:
        pickle.dump(REGISTER_NAME_DICT, writer)

