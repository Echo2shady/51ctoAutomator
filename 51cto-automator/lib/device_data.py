#!usr/bin/env python
# -*- coding:utf-8 -*-
# user nanme: Mr.zhang
# data time : 2021/12/29   2:55 下午
# project   : device_data.py
# IDE       : PyCharm
# email     :17600960626@163.com


import os
import platform
import re

'''
初始化设备信息
存放adb等获取设备的信息使用
'''

# 获取分辨率
def get_vm_size(device_id_list, screen_size_list):
    cmd = os.popen('adb -s %s shell wm size' % device_id_list)
    vm_size = cmd.read()
    cmd.close()
    print(vm_size, type(vm_size))
    vm_size_list = re.findall(r'(\d+)', vm_size)
    width = vm_size_list[0]
    screen_size_list.append(width)
    height = vm_size_list[1]
    screen_size_list.append(height)
    return screen_size_list


# 查询端口号是否可用
def keep_port_available(port_id):
    which_system = platform.system().lower()
    print('which_system: %s' % which_system)
    if 'darwin'in which_system:
        cmd = os.popen('lsof -i tcp:%d' % port_id)
        port_available = cmd.read()
        cmd.close()
        pid = re.findall(r'(\s\d+\s)', port_available)
        port_available_last = ''.join(pid).strip()
        try:
            os.system('kill %s' % port_available_last)
        except Exception as e:
            e
            pass

    else:
        cmd = os.popen('netstat -aon | findstr "%d" ' % port_id)
        port_available = cmd.read()
        cmd.close()
        pid = re.findall(r'(\s\d+\s)', port_available)
        port_available_last = ''.join(pid).strip()
        try:
            os.system('taskkill /F /PID %s' % port_available_last)
        except Exception as e:
            pass


# 查询系统版本号
def get_platform_version(device_id):
    cmd = os.popen('adb -s %s shell getprop ro.build.version.release' % device_id)
    platform_version = cmd.read()
    cmd.close()
    return platform_version.replace('\n', '')

# 连接的设备device id
def start_devices():
    """
    :return: 返回list（连接的设备device id）
    """
    cmd = os.popen('adb devices')
    device_info = cmd.read()
    cmd.close()
    device_id_list = re.findall(r'(.*?)\t', device_info)
    return device_id_list

# 启动 appium 服务监听端口号
def start_appium(port_id, device):
    """
    :param port_id: 启动 appium 服务监听端口号
    :param device: 设备device id
    :return:
    """
    os.system(
        'node /Applications/Appium.app/Contents/Resources/app/node_modules/appium/build/lib/main.js'
        ' --port %s -U %s --session-override' % (
            str(port_id), device))
    '''
    appium 使用方式
    result = os.system('appium -p %s -bp %s -U %s --session-override' % (
            str(port_id), device))
    '''
    # Log_info().getlog('start-service').debug(result)
    print("%s,%s,%s" % (str(port_id), device))