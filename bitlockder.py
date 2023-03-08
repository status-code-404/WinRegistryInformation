import subprocess
import time
import os

DECRYPT_PASSWORD = "manage-bde -unlock %s -password"
DECRYPT_SAFE_KEY = "manage-bde -unlock %s -RecoveryPassword %s"
OFF_ENCRYPT = "manage-bde -protectors -disable %s"
STATUS = "manage-bde -status"
NEED_PARAM = [DECRYPT_PASSWORD]


def decrypt_by_password(volumn: str, password: str):
    return run_cmd_use_stdin(DECRYPT_PASSWORD % volumn, password)


def decrypt_by_key(volumn: str, key: str):
    return run_cmd_no_stdin(DECRYPT_SAFE_KEY % (volumn, key))


# todo: 我这个地方的代码如果跑password就告诉我找不到句柄，也不知道为啥也不知道咋修，是真的佛了
def run_cmd_use_stdin(cmd, *args):
    process = subprocess.Popen(cmd.split(" "), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               env=os.environ, shell=True)
    print(cmd)
    print(args)
    for arg in args:
        text = process.stdout.read().decode("gb2312")
        print(text.strip())
        process.stdin.write(str.encode("gb2312") + b"\n")
        process.stdin.flush()
        print(arg)
    print("Done")


def run_cmd_no_stdin(cmd):
    print(cmd)
    result = subprocess.run(cmd.split(" "), capture_output=True, text=True, timeout=5)
    return result.stdout


def get_status():
    status_str = run_cmd_no_stdin(STATUS)
    status_all = dict()
    for line in status_str.split("\n"):
        if len(line) == 0:
            continue
        if line[0] == "卷":
            now_volumn = line[1:3]
            status_all[now_volumn] = dict()
        if "锁定状态" in line:
            status_all[now_volumn]["locked"] = False if "已解锁" in line else True
        # 其他属性后面可以再加
    return status_all


if __name__ == '__main__':
    # decrypt_by_key("E:", "623601-045122-449944-117700-000913-584023-033011-372229")
    print(get_status())
