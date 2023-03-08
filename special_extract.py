import winreg
import pickle
from bitlockder import run_cmd_no_stdin
from registry import register_item_get_data

CACHE_PARSER_CMD = "cache_parser.exe --csv %s --csvf %s"
EXE_GET_CMD = "get_exe.exe /stext %s"


def get_recent_use_cache(store_location="./", file_name="recent_use.csv"):
    run_cmd_no_stdin(CACHE_PARSER_CMD % (store_location, file_name))


def get_all_exe(file_name="exe_list.txt"):
    run_cmd_no_stdin(EXE_GET_CMD % file_name)


def shell_register_exe(handle=winreg.HKEY_CURRENT_USER):
    key = winreg.OpenKey(handle, 'SOFTWARE\\Classes\\Local Settings\\Software\\Microsoft\\Windows\\Shell\\MuiCache')
    raw_data = register_item_get_data(key)
    data = {}
    for path in raw_data:
        data[raw_data[path]] = path
    return data


if __name__ == '__main__':
    # get_recent_use_cache(store_location="H://tools//WinRegistryInformation")
    print(shell_register_exe())
