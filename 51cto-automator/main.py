import os
import pytest
import golVar
# import xlrd
from multiprocessing.pool import Pool
# case_id_data_path = os.path.dirname(os.path.abspath(__file__)) + '/case_id.xlsx'
#
# def case_data():
#     wb = xlrd.open_workbook(filename=case_id_data_path)
#     sheet1 = wb.sheet_by_index(0)
#     case_id = sheet1.col_values(0)
#     pool_id = sheet1.col_values(1)
#     case_id.pop(0)
#     pool_id.pop(0)
#     print('case_id', case_id)
#     print('pool_id', pool_id)
#     return case_id, pool_id
from lib.loggers import log


def execute_cmd(case_id, device_num):
    os.system('python3 -m pytest -s -v %s --alluredir report/allure_raw --clean-alluredir --cmdopt %d ' % (
        case_id, device_num))


# 多设备运行
def multi_device_operation():
    golVar.__init__()
    '''
        目前 case 分发逻辑：按照 case_pool 去分发测试任务，case_pool 列表中只有一个 case 文件，意味着该文件只能由一个设备测试，如需要
        2 台，甚至 3 台进行同步测试，则需将原 case 文件分为 3 份：TestCase1.py、TestCase1.py、TestCase3.py 放入 case_pool 列表中，
        每台设备跑对应文件的测试 case
    '''
    case_pool = ['./case/TestCase1.py']  # , './case/no_TestCase2.py'
    log.info(case_pool)
    # device_num = len(device_id_list)
    # which_case = case_data()
    p = Pool(len(case_pool))
    for i in range(len(case_pool)):
        p.apply_async(execute_cmd, args=(case_pool[i], i), )
    p.close()
    p.join()


if __name__ == '__main__':
    multi_device_operation()  # 多进程使用
    # pytest.main()  # 单台设备使用
    os.popen('allure generate report/allure_raw -o report/html --clean')
