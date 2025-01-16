import os
import sys
import subprocess
import argparse

def clone_repository(url, target_dir=None):
    """
    克隆GitHub仓库
    :param url: GitHub仓库的URL
    :param target_dir: 目标目录（可选）
    """
    try:
        if target_dir:
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            os.chdir(target_dir)
        
        print(f"正在克隆仓库: {url}")
        subprocess.run(['git', 'clone', url], check=True)
        print("克隆完成！")
    except subprocess.CalledProcessError as e:
        print(f"克隆失败: {e}")
    except Exception as e:
        print(f"发生错误: {e}")

def main():
    parser = argparse.ArgumentParser(description='GitHub仓库克隆工具')
    parser.add_argument('url', help='GitHub仓库的URL')
    parser.add_argument('--dir', help='目标目录（可选）', default=None)
    
    args = parser.parse_args()
    clone_repository(args.url, args.dir)

if __name__ == '__main__':
    main() 