import subprocess
from bitlockder import run_cmd_no_stdin, run_cmd_use_stdin

COMMON_UNLOCK = "cipher /d %s"  # file path
IMPORT_CRET: str = "echo %s|certutil -importpfx -user %s"  # password + pfx-cert path


def off_readonly(file_path: str):
    # 管理员权限
    import os
    import stat
    os.chmod(file_path, stat.S_IWRITE)

