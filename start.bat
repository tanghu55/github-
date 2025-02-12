@echo off
chcp 65001 > nul
title GitHub克隆工具
echo 正在启动GitHub克隆工具...

:: 创建日志目录
if not exist "logs" mkdir logs

:: 将所有输出重定向到日志文件
echo 启动时间: %date% %time% > logs\startup.log

:: 检查Python是否安装
echo 检查Python安装状态... >> logs\startup.log
python --version > nul 2>&1
if errorlevel 1 (
    echo 错误：未检测到Python，请确保已安装Python并添加到系统环境变量中
    echo 错误：未检测到Python >> logs\startup.log
    pause
    exit /b 1
)

:: 检查虚拟环境是否存在
echo 检查虚拟环境... >> logs\startup.log
if not exist "venv" (
    echo 正在创建虚拟环境...
    echo 创建虚拟环境... >> logs\startup.log
    python -m venv venv
    if errorlevel 1 (
        echo 创建虚拟环境失败！
        echo 创建虚拟环境失败 >> logs\startup.log
        pause
        exit /b 1
    )
    echo 虚拟环境创建完成
)

:: 激活虚拟环境
echo 激活虚拟环境... >> logs\startup.log
call venv\Scripts\activate
if errorlevel 1 (
    echo 激活虚拟环境失败！
    echo 激活虚拟环境失败 >> logs\startup.log
    pause
    exit /b 1
)

:: 确保pip是最新版本
python -m pip install --upgrade pip

:: 卸载已有的PyQt6（如果存在）
pip uninstall PyQt6 PyQt6-Qt6 PyQt6-sip -y

:: 重新安装PyQt6及其依赖
echo 正在安装PyQt6及其依赖...
pip install PyQt6==6.6.1 PyQt6-Qt6==6.6.1 PyQt6-sip==13.6.0

:: 检查安装是否成功
python -c "from PyQt6.QtWidgets import QApplication" 2>nul
if errorlevel 1 (
    echo PyQt6安装或导入失败！
    echo 尝试安装VC++运行时...
    powershell -Command "Invoke-WebRequest -Uri 'https://aka.ms/vs/17/release/vc_redist.x64.exe' -OutFile 'vc_redist.x64.exe'"
    vc_redist.x64.exe /quiet /norestart
    del vc_redist.x64.exe
    
    :: 再次尝试导入PyQt6
    python -c "from PyQt6.QtWidgets import QApplication" 2>nul
    if errorlevel 1 (
        echo PyQt6仍然无法正常工作，请确保系统已安装最新的Visual C++运行时
        pause
        exit /b 1
    )
)

:: 启动程序
echo 启动主程序... >> logs\startup.log
python github_clone_gui.py
if errorlevel 1 (
    echo 程序运行出错，请检查错误信息
    echo 程序运行错误 >> logs\startup.log
    pause
    exit /b 1
)

:: 运行结束后退出虚拟环境
echo 程序运行完成，退出虚拟环境 >> logs\startup.log
call venv\Scripts\deactivate

echo 如果看到此消息，请按任意键退出...
pause > nul 