import os
import pytest
from pytest_mini.constant import Constant

test_cases = ["test_home.py"]  # 执行的脚本

main_list = [
    '-s', '-v',
    *test_cases,
    '--durations=0', '--clean-alluredir',
    '--alluredir', f'{Constant().REPORT_PATH}/allure_results'
]
pytest.main(main_list)
if not os.getenv("BUILD_URL"):
    os.system(f"{Constant.ALLURE_TOOL} serve {Constant().REPORT_PATH}/allure_results")  # 本地执行
