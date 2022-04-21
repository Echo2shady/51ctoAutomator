import os

import yaml


def get_path_data(path):  # '/layout/candidate_layout'
    """
    :param path: 文件相对路径
    :return: 测试数据
    """
    script_path_up = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = script_path_up + path
    test_case_data = yaml.safe_load(open(data_path, 'r'))
    return test_case_data


def get_path(path):  # '/layout/candidate_layout'
    """
    :param path: 文件相对路径
    :return: 文件绝对路径
    """
    script_path_up = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = script_path_up + path
    return data_path
