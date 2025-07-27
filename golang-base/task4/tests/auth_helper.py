"""
JWT认证助手模块
为所有测试提供统一的认证支持
"""

from .base_test import BaseAPITest


class AuthenticatedAPITest(BaseAPITest):
    """带认证的API测试基类"""

    def __init__(self, base_url: str = "http://localhost:8000/api/v1", auto_cleanup: bool = True):
        super().__init__(base_url, auto_cleanup)
        self.test_user_id = None
        self.test_user_password = "testpass123"

    def setup_authenticated_user(self, username: str = "authuser", password: str = None):
        """创建测试用户并登录获取JWT token"""
        if password is None:
            password = self.test_user_password

        self.print_step(0, f"设置认证用户: {username}")

        # 创建用户
        user_data = {
            "username": username,
            "password": password,
            "email": f"{username}@example.com",
        }

        response = self.make_request(
            "POST",
            "/register",
            data=user_data,
            expected_status=200,
            description=f"创建认证用户 {username}",
            require_auth=False,
        )

        if response.status_code == 200:
            user_id = self.extract_id_from_response(response)
            if user_id:
                self.test_user_id = user_id
                self.print_info(f"创建认证用户ID: {user_id}")

                # 登录获取token
                login_data = {"id": user_id, "password": password}
                login_response = self.make_request(
                    "POST",
                    "/login",
                    data=login_data,
                    expected_status=200,
                    description="登录获取JWT token",
                    require_auth=False,
                )

                if login_response.status_code == 200:
                    try:
                        data = login_response.json()
                        token = data.get("data", {}).get("token")
                        if token:
                            self.set_jwt_token(token)
                            self.print_success("认证设置完成，已获取JWT token")
                            return user_id
                        else:
                            self.print_error("登录响应中未找到token")
                    except:
                        self.print_error("无法解析登录响应")

        self.print_error("认证用户设置失败")
        return None

    def cleanup_test_user(self):
        """清理测试用户"""
        if self.test_user_id:
            try:
                self.make_request(
                    "DELETE",
                    f"/user/{self.test_user_id}",
                    expected_status=200,
                    description=f"清理认证用户 {self.test_user_id}",
                )
            except:
                pass  # 忽略清理错误