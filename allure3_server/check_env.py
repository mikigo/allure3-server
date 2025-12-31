import subprocess
import sys
import shutil
import os


def check_npm_installed():
    """检查 npm 是否已安装"""
    npm_path = shutil.which('npm')
    if npm_path:
        try:
            version_result = subprocess.run([npm_path, '--version'],
                                            capture_output=True,
                                            text=True)
            if version_result.returncode == 0:
                return True
        except (subprocess.SubprocessError, FileNotFoundError):
            pass

    return False


def check_node_installed():
    try:
        result = subprocess.run(['node', '--version'],
                                capture_output=True,
                                text=True)
        if result.returncode == 0:
            return True
    except (subprocess.SubprocessError, FileNotFoundError):
        pass

    return False


def prompt_npm_installation():
    print("\n" + "=" * 60)
    print("⚠️  npm 未安装或未正确配置")
    print("=" * 60)
    print("\npm 需要 Node.js 环境。请按以下步骤安装：")

    if sys.platform == "win32":
        print("\nWindows 用户：")
        print("1. 访问 https://nodejs.org/ 下载 Windows 安装程序")
        print("2. 运行安装程序，选择默认选项")
        print("3. 安装完成后，重启命令行窗口")

    elif sys.platform == "darwin":
        print("\nmacOS 用户：")
        print("1. 使用 Homebrew 安装：")
        print("   brew install node")
        print("2. 或者从 https://nodejs.org/ 下载 macOS 安装包")

    else:  # Linux
        print("\nLinux 用户：")
        print("1. Ubuntu/Debian:")
        print("   curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -")
        print("   sudo apt-get install -y nodejs")
        print("\n2. CentOS/RHEL/Fedora:")
        print("   curl -fsSL https://rpm.nodesource.com/setup_lts.x | sudo bash -")
        print("   sudo yum install -y nodejs")
        print("\n3. 或者使用包管理器：")
        print("   sudo apt install nodejs npm  # Ubuntu/Debian")
        print("   sudo yum install nodejs npm  # CentOS/RHEL")
        print("   sudo dnf install nodejs npm  # Fedora")

    print("\n安装完成后，请重新运行此程序。")
    print("=" * 60 + "\n")
    sys.exit(1)


def check_npm_env():
    # 先检查 Node.js
    if not check_node_installed():
        prompt_npm_installation()
    if not check_npm_installed():
        prompt_npm_installation()
    return True


if __name__ == "__main__":
    check_npm_env()