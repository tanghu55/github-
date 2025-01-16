# GitHub克隆工具

这是一个简单的命令行工具，用于克隆GitHub仓库。

## 使用要求

- Python 3.6+
- Git命令行工具

## 使用方法

基本用法：
```bash
python github_clone.py <仓库URL>
```

指定目标目录：
```bash
python github_clone.py <仓库URL> --dir <目标目录>
```

## 示例

克隆仓库到当前目录：
```bash
python github_clone.py https://github.com/用户名/仓库名.git
```

克隆仓库到指定目录：
```bash
python github_clone.py https://github.com/用户名/仓库名.git --dir D:/我的项目
```

## 注意事项

1. 确保已经安装了Git
2. 确保有足够的磁盘空间
3. 确保有正常的网络连接 