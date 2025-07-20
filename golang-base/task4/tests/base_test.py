"""
基础测试类，提供通用的测试工具和配置
"""

import requests
import json
from typing import Dict, Any, Optional
from colorama import Fore, Style, init

# 初始化colorama
init(autoreset=True)


class BaseAPITest:
    """API测试基类"""

    def __init__(self, base_url: str = "http://localhost:8000/api/v1", auto_cleanup: bool = True):
        self.base_url = base_url
        self.auto_cleanup = auto_cleanup  # 控制是否自动清理测试数据
        self.session = requests.Session()
        self.session.headers.update(
            {"Content-Type": "application/json", "Accept": "application/json"}
        )

    def print_test_header(self, title: str):
        """打印测试标题"""
        print(f"\n{Fore.CYAN}{'=' * 60}")
        print(f"{Fore.CYAN}{title:^60}")
        print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")

    def print_step(self, step_num: int, description: str):
        """打印测试步骤"""
        print(f"\n{Fore.YELLOW}📋 步骤{step_num}: {description}{Style.RESET_ALL}")

    def print_success(self, message: str):
        """打印成功消息"""
        print(f"{Fore.GREEN}✅ {message}{Style.RESET_ALL}")

    def print_error(self, message: str):
        """打印错误消息"""
        print(f"{Fore.RED}❌ {message}{Style.RESET_ALL}")

    def print_warning(self, message: str):
        """打印警告消息"""
        print(f"{Fore.YELLOW}⚠️  {message}{Style.RESET_ALL}")

    def print_info(self, message: str):
        """打印信息消息"""
        print(f"{Fore.BLUE}ℹ️  {message}{Style.RESET_ALL}")

    def make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[Any, Any]] = None,
        expected_status: int = 200,
        description: str = "",
    ) -> requests.Response:
        """
        发送HTTP请求并处理响应

        Args:
            method: HTTP方法 (GET, POST, PUT, DELETE)
            endpoint: API端点
            data: 请求数据
            expected_status: 期望的状态码
            description: 请求描述

        Returns:
            requests.Response对象
        """
        url = f"{self.base_url}{endpoint}"

        try:
            if method.upper() == "GET":
                response = self.session.get(url)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data)
            elif method.upper() == "PUT":
                response = self.session.put(url, json=data)
            elif method.upper() == "DELETE":
                response = self.session.delete(url)
            else:
                raise ValueError(f"不支持的HTTP方法: {method}")

            # 打印请求信息
            print(f"🌐 {method.upper()} {url}")
            if data:
                print(f"📤 请求数据: {json.dumps(data, ensure_ascii=False, indent=2)}")

            # 打印响应信息
            print(f"📈 状态码: {response.status_code}")

            # 尝试解析JSON响应
            try:
                response_data = response.json()
                print(
                    f"📥 响应数据: {json.dumps(response_data, ensure_ascii=False, indent=2)}"
                )
            except json.JSONDecodeError:
                print(f"📥 响应数据: {response.text}")

            # 检查状态码
            if response.status_code == expected_status:
                if description:
                    self.print_success(f"{description} - 成功")
                else:
                    self.print_success("请求成功")
            else:
                if description:
                    self.print_error(
                        f"{description} - 失败 (期望状态码: {expected_status}, 实际: {response.status_code})"
                    )
                else:
                    self.print_error(
                        f"请求失败 (期望状态码: {expected_status}, 实际: {response.status_code})"
                    )

            return response

        except requests.exceptions.RequestException as e:
            self.print_error(f"请求异常: {str(e)}")
            raise

    def check_server_status(self) -> bool:
        """检查服务器是否运行"""
        try:
            response = self.session.get(f"{self.base_url}/user/1", timeout=5)
            return True
        except requests.exceptions.RequestException:
            return False

    def extract_id_from_response(self, response: requests.Response) -> Optional[int]:
        """从响应中提取ID"""
        try:
            data = response.json()
            if "data" in data:
                # 尝试多种可能的ID字段名
                for id_field in ["id", "ID", "Id"]:
                    if id_field in data["data"]:
                        return data["data"][id_field]
        except (json.JSONDecodeError, KeyError):
            pass
        return None

    def assert_response_success(self, response: requests.Response, message: str = ""):
        """断言响应成功"""
        try:
            data = response.json()
            if data.get("code") == 0:  # 假设0表示成功
                self.print_success(message or "响应成功")
                return True
            else:
                self.print_error(
                    f"{message or '响应失败'}: {data.get('msg', '未知错误')}"
                )
                return False
        except json.JSONDecodeError:
            self.print_error(f"{message or '响应失败'}: 无法解析JSON响应")
            return False

    def run_cleanup_tests(self):
        """运行清理测试 - 子类可以选择实现"""
        pass
    
    def run_test_suite(self, include_cleanup: bool = None):
        """运行测试套件 - 子类需要实现
        
        Args:
            include_cleanup: 是否包含清理测试，None表示使用默认设置
        """
        raise NotImplementedError("子类需要实现run_test_suite方法")
