

_global_dict = {}


def __init__():  # 初始化
    global _global_dict


def set_value(key, value):
    """ 定义一个全局变量 """
    _global_dict[key] = value


def get_value(key, defValue='relative_layout_en'):
    try:
        return _global_dict[key]
    except KeyError:
        return defValue
