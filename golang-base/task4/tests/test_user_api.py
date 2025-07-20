"""
用户API测试模块
测试用户注册、登录、获取、更新、删除等功能
"""

from .base_test import BaseAPITest
import json


class UserAPITest(BaseAPITest):
    """用户API测试类"""

    def __init__(self, base_url: str = "http://localhost:8000/api/v1", auto_cleanup: bool = True):
        super().__init__(base_url, auto_cleanup)
        self.created_user_ids = []  # 记录创建的用户ID用于清理

    def test_user_registration(self):
        """测试用户注册"""
        self.print_step(1, "用户注册测试")

        # 测试正常注册
        user_data = {
            "username": "testuser",
            "password": "testpass123",
            "email": "test@example.com",
        }

        response = self.make_request(
            "POST",
            "/register",
            data=user_data,
            expected_status=200,
            description="正常用户注册",
        )

        if response.status_code == 200:
            user_id = self.extract_id_from_response(response)
            if user_id:
                self.created_user_ids.append(user_id)
                self.print_info(f"创建用户ID: {user_id}")

        return response

    def test_duplicate_registration(self):
        """测试重复用户注册"""
        self.print_step(2, "重复用户注册测试（应该失败）")

        user_data = {
            "username": "testuser",
            "password": "testpass123",
            "email": "test@example.com",
        }

        response = self.make_request(
            "POST",
            "/register",
            data=user_data,
            expected_status=400,  # 期望失败
            description="重复用户注册",
        )

        return response

    def test_multiple_user_registration(self):
        """测试多用户注册"""
        self.print_step(3, "注册多个用户")

        users = [
            {"username": "alice", "password": "alice123", "email": "alice@example.com"},
            {"username": "bob", "password": "bob123", "email": "bob@example.com"},
            {
                "username": "charlie",
                "password": "charlie123",
                "email": "charlie@example.com",
            },
        ]

        responses = []
        for i, user_data in enumerate(users, 1):
            print(f"\n  📝 注册用户 {i}: {user_data['username']}")
            response = self.make_request(
                "POST",
                "/register",
                data=user_data,
                expected_status=200,
                description=f"注册用户 {user_data['username']}",
            )

            if response.status_code == 200:
                user_id = self.extract_id_from_response(response)
                if user_id:
                    self.created_user_ids.append(user_id)
                    self.print_info(f"创建用户ID: {user_id}")

            responses.append(response)

        return responses

    def test_get_user(self):
        """测试获取用户信息"""
        self.print_step(4, "获取用户信息测试")

        if not self.created_user_ids:
            self.print_warning("没有可用的用户ID进行测试")
            return None

        user_id = self.created_user_ids[0]
        response = self.make_request(
            "GET",
            f"/user/{user_id}",
            expected_status=200,
            description=f"获取用户信息 (ID: {user_id})",
        )

        return response

    def test_get_nonexistent_user(self):
        """测试获取不存在的用户"""
        self.print_step(5, "获取不存在的用户测试")

        response = self.make_request(
            "GET",
            "/user/99999",
            expected_status=500,  # 根据你的API实际返回状态码调整
            description="获取不存在的用户",
        )

        return response

    def test_invalid_user_id(self):
        """测试无效的用户ID"""
        self.print_step(6, "无效用户ID测试")

        response = self.make_request(
            "GET", "/user/abc", expected_status=400, description="无效用户ID测试"
        )

        return response

    def test_user_login(self):
        """测试用户登录"""
        self.print_step(7, "用户登录测试")

        if not self.created_user_ids:
            self.print_warning("没有可用的用户进行登录测试")
            return None

        user_id = self.created_user_ids[0]
        login_data = {"id": user_id, "password": "testpass123"}

        response = self.make_request(
            "POST",
            "/login",
            data=login_data,
            expected_status=200,
            description="用户登录",
        )

        return response

    def test_wrong_password_login(self):
        """测试错误密码登录"""
        self.print_step(8, "错误密码登录测试")

        if not self.created_user_ids:
            self.print_warning("没有可用的用户进行登录测试")
            return None

        user_id = self.created_user_ids[0]
        login_data = {"id": user_id, "password": "wrongpassword"}

        response = self.make_request(
            "POST",
            "/login",
            data=login_data,
            expected_status=401,
            description="错误密码登录",
        )

        return response

    def test_update_user(self):
        """测试更新用户信息"""
        self.print_step(9, "更新用户信息测试")

        if not self.created_user_ids:
            self.print_warning("没有可用的用户进行更新测试")
            return None

        user_id = self.created_user_ids[0]
        update_data = {
            "id": user_id,
            "username": "updated_testuser",
            "password": "newpassword123",
            "email": "updated@example.com",
        }

        response = self.make_request(
            "PUT",
            "/user",
            data=update_data,
            expected_status=200,
            description="更新用户信息",
        )

        return response

    def test_verify_update(self):
        """验证用户更新"""
        self.print_step(10, "验证用户更新")

        if not self.created_user_ids:
            self.print_warning("没有可用的用户进行验证")
            return None

        user_id = self.created_user_ids[0]
        response = self.make_request(
            "GET",
            f"/user/{user_id}",
            expected_status=200,
            description="验证用户更新结果",
        )

        # 检查用户名是否已更新
        try:
            data = response.json()
            if data.get("data", {}).get("username") == "updated_testuser":
                self.print_success("用户信息更新验证成功")
            else:
                self.print_error("用户信息更新验证失败")
        except:
            self.print_error("无法验证用户更新结果")

        return response

    def test_delete_user(self):
        """测试删除用户"""
        self.print_step(11, "删除用户测试")

        if len(self.created_user_ids) < 2:
            self.print_warning("需要至少2个用户进行删除测试")
            return None

        # 删除最后一个创建的用户
        user_id = self.created_user_ids[-1]
        response = self.make_request(
            "DELETE",
            f"/user/{user_id}",
            expected_status=200,
            description=f"删除用户 (ID: {user_id})",
        )

        if response.status_code == 200:
            self.created_user_ids.remove(user_id)

        return response

    def test_verify_deletion(self):
        """验证删除操作"""
        self.print_step(12, "验证删除操作")

        # 这里需要一个已删除的用户ID，我们可以创建一个临时用户然后删除
        temp_user = {
            "username": "temp_user",
            "password": "temp123",
            "email": "temp@example.com",
        }

        # 创建临时用户
        create_response = self.make_request(
            "POST",
            "/register",
            data=temp_user,
            expected_status=200,
            description="创建临时用户用于删除测试",
        )

        if create_response.status_code == 200:
            temp_user_id = self.extract_id_from_response(create_response)

            # 删除临时用户
            self.make_request(
                "DELETE",
                f"/user/{temp_user_id}",
                expected_status=200,
                description="删除临时用户",
            )

            # 尝试获取已删除的用户
            response = self.make_request(
                "GET",
                f"/user/{temp_user_id}",
                expected_status=500,  # 期望获取失败
                description="尝试获取已删除用户",
            )

            return response

        return None

    def test_edge_cases(self):
        """测试边界情况"""
        self.print_step(13, "边界情况测试")

        edge_cases = [
            {
                "name": "空用户名",
                "data": {
                    "username": "",
                    "password": "test123",
                    "email": "test@example.com",
                },
                "expected_status": 400,
            },
            {
                "name": "空密码",
                "data": {
                    "username": "testuser",
                    "password": "",
                    "email": "test@example.com",
                },
                "expected_status": 400,
            },
            {
                "name": "无效邮箱格式",
                "data": {
                    "username": "testuser",
                    "password": "test123",
                    "email": "invalid-email",
                },
                "expected_status": 400,
            },
            {
                "name": "超长用户名",
                "data": {
                    "username": "a" * 1000,
                    "password": "test123",
                    "email": "test@example.com",
                },
                "expected_status": 400,
            },
        ]

        for case in edge_cases:
            print(f"\n  🧪 测试案例: {case['name']}")
            self.make_request(
                "POST",
                "/register",
                data=case["data"],
                expected_status=case["expected_status"],
                description=case["name"],
            )

    def cleanup(self):
        """清理测试数据"""
        self.print_step(14, "清理测试数据")

        for user_id in self.created_user_ids[:]:
            try:
                response = self.make_request(
                    "DELETE",
                    f"/user/{user_id}",
                    expected_status=200,
                    description=f"清理用户 ID: {user_id}",
                )
                if response.status_code == 200:
                    self.created_user_ids.remove(user_id)
            except Exception as e:
                self.print_error(f"清理用户 {user_id} 失败: {str(e)}")
    
    def run_cleanup_tests(self):
        """运行删除相关测试"""
        self.print_test_header("用户 API 删除测试")
        
        try:
            self.test_delete_user()
            self.test_verify_deletion()
            
            self.print_test_header("用户 API 删除测试完成")
            self.print_success("删除相关测试已执行完成")
            return True
            
        except Exception as e:
            self.print_error(f"删除测试过程中发生异常: {str(e)}")
            return False

    def run_test_suite(self, include_cleanup: bool = None):
        """运行完整的用户API测试套件"""
        self.print_test_header("用户 API 测试套件")

        # 确定是否运行清理
        run_cleanup = include_cleanup if include_cleanup is not None else self.auto_cleanup

        # 检查服务器状态
        if not self.check_server_status():
            self.print_error("服务器未运行！请先启动服务器: go run main.go")
            return False

        self.print_success("服务器运行正常")

        try:
            # 运行基础测试（不包括删除测试）
            self.test_user_registration()
            self.test_duplicate_registration()
            self.test_multiple_user_registration()
            self.test_get_user()
            self.test_get_nonexistent_user()
            self.test_invalid_user_id()
            self.test_user_login()
            self.test_wrong_password_login()
            self.test_update_user()
            self.test_verify_update()
            self.test_edge_cases()

            self.print_test_header("用户 API 基础测试完成")
            self.print_success("基础测试已执行完成")
            
            if len(self.created_user_ids) > 0:
                self.print_info(f"本次测试创建了 {len(self.created_user_ids)} 个用户，ID: {self.created_user_ids}")
                if not run_cleanup:
                    self.print_warning("测试数据未自动清理，如需清理请运行删除测试选项")

            return True

        except Exception as e:
            self.print_error(f"测试过程中发生异常: {str(e)}")
            return False

        finally:
            # 根据设置决定是否清理测试数据
            if run_cleanup:
                self.cleanup()


def main():
    """主函数"""
    test = UserAPITest()
    test.run_test_suite()


if __name__ == "__main__":
    main()
