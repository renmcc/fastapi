import sys
import os
from pathlib import Path

project_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, project_dir)

from fastapi.testclient import TestClient
from run import app
"""Testing 测试用例"""

client = TestClient(app)  # pip install pytest


def test_run_bg_task():
    """
    函数名用test_开头是pytest的规范，注意不是async def
    """
    response = client.post(url="/chapter08/background_task?framework=FastAPI")
    assert response.status_code == 200
    assert response.json() == {"message": "任务已在后台运行"}


