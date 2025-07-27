"""
文章API测试模块
测试文章创建、获取、更新、删除等功能
"""

from .auth_helper import AuthenticatedAPITest
import json


class PostAPITest(AuthenticatedAPITest):
    """文章API测试类"""

    def __init__(self, base_url: str = "http://localhost:8000/api/v1", auto_cleanup: bool = True):
        super().__init__(base_url, auto_cleanup)
        self.created_user_ids = []  # 记录创建的用户ID
        self.created_post_ids = []  # 记录创建的文章ID用于清理

    def setup_test_user(self):
        """设置测试用户并登录获取JWT"""
        user_id = self.setup_authenticated_user("postauthor", "password123")
        if user_id:
            self.created_user_ids.append(user_id)
            return user_id
        return None

    def test_create_post(self):
        """测试创建文章"""
        self.print_step(1, "创建文章测试")

        if not self.created_user_ids:
            self.print_warning("没有可用的用户创建文章")
            return None

        user_id = self.created_user_ids[0]
        post_data = {
            "title": "我的第一篇文章",
            "content": "这是文章的内容，包含了一些有趣的信息。",
            "user_id": user_id,
        }

        response = self.make_request(
            "POST",
            "/post",
            data=post_data,
            expected_status=200,
            description="创建第一篇文章",
        )

        if response.status_code == 200:
            post_id = self.extract_id_from_response(response)
            if post_id:
                self.created_post_ids.append(post_id)
                self.print_info(f"创建文章ID: {post_id}")

        return response

    def test_create_multiple_posts(self):
        """测试创建多篇文章"""
        self.print_step(2, "创建多篇文章测试")

        if not self.created_user_ids:
            self.print_warning("没有可用的用户创建文章")
            return []

        user_id = self.created_user_ids[0]
        posts_data = [
            {
                "title": "技术分享：Go语言最佳实践",
                "content": "在这篇文章中，我将分享一些Go语言开发的最佳实践和经验。包括错误处理、并发编程、性能优化等方面的内容。",
                "user_id": user_id,
            },
            {
                "title": "深入理解HTTP协议",
                "content": "HTTP（超文本传输协议）是互联网上应用最为广泛的一种网络协议。\\n\\n1. HTTP的特点\\n- 简单快速\\n- 灵活\\n- 无连接\\n- 无状态\\n\\n2. HTTP请求方法\\n- GET、POST、PUT、DELETE等",
                "user_id": user_id,
            },
            {
                "title": "数据库设计原则",
                "content": "良好的数据库设计是应用程序成功的关键。本文分享数据库设计的基本原则和最佳实践。",
                "user_id": user_id,
            },
        ]

        responses = []
        for i, post_data in enumerate(posts_data, 1):
            print(f"\\n  📝 创建文章 {i}: {post_data['title']}")
            response = self.make_request(
                "POST",
                "/post",
                data=post_data,
                expected_status=200,
                description=f"创建文章: {post_data['title']}",
            )

            if response.status_code == 200:
                post_id = self.extract_id_from_response(response)
                if post_id:
                    self.created_post_ids.append(post_id)
                    self.print_info(f"创建文章ID: {post_id}")

            responses.append(response)

        return responses

    def test_create_invalid_post(self):
        """测试创建无效文章"""
        self.print_step(3, "创建无效文章测试")

        if not self.created_user_ids:
            self.print_warning("没有可用的用户创建文章")
            return None

        user_id = self.created_user_ids[0]

        # 测试空标题
        invalid_post = {"title": "", "content": "这篇文章没有标题", "user_id": user_id}

        response = self.make_request(
            "POST",
            "/post",
            data=invalid_post,
            expected_status=400,  # 期望失败
            description="创建空标题文章（应该失败）",
        )

        return response

    def test_get_post(self):
        """测试获取文章"""
        self.print_step(4, "获取文章测试")

        if not self.created_post_ids:
            self.print_warning("没有可用的文章进行测试")
            return None

        post_id = self.created_post_ids[0]
        response = self.make_request(
            "GET",
            f"/post/{post_id}",
            expected_status=200,
            description=f"获取文章 (ID: {post_id})",
        )

        return response

    def test_get_nonexistent_post(self):
        """测试获取不存在的文章"""
        self.print_step(5, "获取不存在的文章测试")

        response = self.make_request(
            "GET",
            "/post/99999",
            expected_status=500,  # 根据实际API调整
            description="获取不存在的文章",
        )

        return response

    def test_invalid_post_id(self):
        """测试无效的文章ID"""
        self.print_step(6, "无效文章ID测试")

        response = self.make_request(
            "GET", "/post/abc", expected_status=400, description="无效文章ID测试"
        )

        return response

    def test_update_post(self):
        """测试更新文章"""
        self.print_step(7, "更新文章测试")

        if not self.created_post_ids or not self.created_user_ids:
            self.print_warning("没有可用的文章或用户进行更新测试")
            return None

        post_id = self.created_post_ids[0]
        user_id = self.created_user_ids[0]

        update_data = {
            "id": post_id,
            "title": "我的第一篇文章（已更新）",
            "content": "这是更新后的文章内容，添加了更多详细信息和示例代码。\\n\\n更新内容包括：\\n1. 更详细的技术说明\\n2. 实际代码示例\\n3. 最佳实践建议",
            "user_id": user_id,
        }

        response = self.make_request(
            "PUT",
            "/post",
            data=update_data,
            expected_status=200,
            description="更新文章内容",
        )

        return response

    def test_verify_post_update(self):
        """验证文章更新"""
        self.print_step(8, "验证文章更新")

        if not self.created_post_ids:
            self.print_warning("没有可用的文章进行验证")
            return None

        post_id = self.created_post_ids[0]
        response = self.make_request(
            "GET",
            f"/post/{post_id}",
            expected_status=200,
            description="验证文章更新结果",
        )

        # 检查文章标题是否已更新
        try:
            data = response.json()
            title = data.get("data", {}).get("title", "")
            if "已更新" in title:
                self.print_success("文章更新验证成功")
            else:
                self.print_error("文章更新验证失败")
        except:
            self.print_error("无法验证文章更新结果")

        return response

    def test_create_long_content_post(self):
        """测试创建长内容文章"""
        self.print_step(9, "创建长内容文章测试")

        if not self.created_user_ids:
            self.print_warning("没有可用的用户创建文章")
            return None

        user_id = self.created_user_ids[0]
        long_content = """这是一篇包含大量内容的文章，用于测试系统对长文本的处理能力。

## 前言
在现代Web开发中，处理大量文本内容是一个常见需求。这篇文章将探讨各种文本处理技术和最佳实践。

## 主要内容

### 1. 文本存储
- 数据库设计考虑
- 字符编码处理
- 索引优化策略

### 2. 文本处理
- 内容格式化
- 搜索功能实现
- 性能优化技巧

### 3. 安全考虑
- XSS防护
- SQL注入预防
- 内容验证

## 技术实现

以下是一些关键的技术实现细节：

```go
func ProcessLongText(content string) error {
    // 文本长度验证
    if len(content) > MAX_CONTENT_LENGTH {
        return errors.New("content too long")
    }
    
    // 内容安全过滤
    sanitized := html.EscapeString(content)
    
    // 存储到数据库
    return saveToDatabase(sanitized)
}
```

## 结论
通过合理的架构设计和技术选择，我们可以有效地处理大量文本内容，确保系统的性能和安全性。

## 参考资料
1. Go语言官方文档
2. MySQL性能优化指南
3. Web安全最佳实践

---
*本文总字数: 约500字*"""

        post_data = {
            "title": "长内容文章测试",
            "content": long_content,
            "user_id": user_id,
        }

        response = self.make_request(
            "POST",
            "/post",
            data=post_data,
            expected_status=200,
            description="创建长内容文章",
        )

        if response.status_code == 200:
            post_id = self.extract_id_from_response(response)
            if post_id:
                self.created_post_ids.append(post_id)
                self.print_info(f"创建长内容文章ID: {post_id}")

        return response

    def test_delete_post(self):
        """测试删除文章"""
        self.print_step(10, "删除文章测试")

        if len(self.created_post_ids) < 2:
            # 创建一个临时文章用于删除
            if self.created_user_ids:
                temp_post = {
                    "title": "临时文章",
                    "content": "这篇文章将被删除",
                    "user_id": self.created_user_ids[0],
                }

                create_response = self.make_request(
                    "POST",
                    "/post",
                    data=temp_post,
                    expected_status=200,
                    description="创建临时文章用于删除测试",
                )

                if create_response.status_code == 200:
                    temp_post_id = self.extract_id_from_response(create_response)
                    if temp_post_id:
                        self.created_post_ids.append(temp_post_id)

        if not self.created_post_ids:
            self.print_warning("没有可用的文章进行删除测试")
            return None

        # 删除最后一个创建的文章
        post_id = self.created_post_ids[-1]
        response = self.make_request(
            "DELETE",
            f"/post/{post_id}",
            expected_status=200,
            description=f"删除文章 (ID: {post_id})",
        )

        if response.status_code == 200:
            self.created_post_ids.remove(post_id)

        return response

    def test_verify_deletion(self):
        """验证删除操作"""
        self.print_step(11, "验证删除操作")

        # 创建并删除一个临时文章
        if not self.created_user_ids:
            self.print_warning("没有可用的用户进行删除验证测试")
            return None

        temp_post = {
            "title": "删除验证测试文章",
            "content": "此文章用于验证删除操作",
            "user_id": self.created_user_ids[0],
        }

        # 创建临时文章
        create_response = self.make_request(
            "POST",
            "/post",
            data=temp_post,
            expected_status=200,
            description="创建用于删除验证的临时文章",
        )

        if create_response.status_code == 200:
            temp_post_id = self.extract_id_from_response(create_response)

            if temp_post_id:
                # 删除临时文章
                self.make_request(
                    "DELETE",
                    f"/post/{temp_post_id}",
                    expected_status=200,
                    description="删除临时文章",
                )

                # 尝试获取已删除的文章
                response = self.make_request(
                    "GET",
                    f"/post/{temp_post_id}",
                    expected_status=500,  # 期望获取失败
                    description="尝试获取已删除文章",
                )

                return response

        return None

    def test_edge_cases(self):
        """测试边界情况"""
        self.print_step(12, "边界情况测试")

        if not self.created_user_ids:
            self.print_warning("没有可用的用户进行边界测试")
            return

        user_id = self.created_user_ids[0]

        edge_cases = [
            {
                "name": "空标题",
                "data": {
                    "title": "",
                    "content": "有内容但没有标题",
                    "user_id": user_id,
                },
                "expected_status": 400,
            },
            {
                "name": "空内容",
                "data": {
                    "title": "有标题但没有内容",
                    "content": "",
                    "user_id": user_id,
                },
                "expected_status": 400,
            },
            {
                "name": "超长标题",
                "data": {
                    "title": "标" * 1000,
                    "content": "正常内容",
                    "user_id": user_id,
                },
                "expected_status": 400,
            },
            {
                "name": "不存在的用户ID",
                "data": {"title": "测试标题", "content": "测试内容", "user_id": 99999},
                "expected_status": 500,
            },
            {
                "name": "特殊字符标题",
                "data": {
                    "title": "特殊字符测试: @#$%^&*()_+{}|:<>?",
                    "content": "包含特殊字符的标题",
                    "user_id": user_id,
                },
                "expected_status": 200,
            },
        ]

        for case in edge_cases:
            print(f"\\n  🧪 测试案例: {case['name']}")
            response = self.make_request(
                "POST",
                "/post",
                data=case["data"],
                expected_status=case["expected_status"],
                description=case["name"],
            )

            # 如果创建成功，记录ID用于清理
            if response.status_code == 200:
                post_id = self.extract_id_from_response(response)
                if post_id:
                    self.created_post_ids.append(post_id)

    def cleanup(self):
        """清理测试数据"""
        self.print_step(13, "清理测试数据")

        # 清理文章
        for post_id in self.created_post_ids[:]:
            try:
                response = self.make_request(
                    "DELETE",
                    f"/post/{post_id}",
                    expected_status=200,
                    description=f"清理文章 ID: {post_id}",
                )
                if response.status_code == 200:
                    self.created_post_ids.remove(post_id)
            except Exception as e:
                self.print_error(f"清理文章 {post_id} 失败: {str(e)}")

        # 清理用户
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
        self.print_test_header("文章 API 删除测试")
        
        try:
            self.test_delete_post()
            self.test_verify_deletion()
            
            self.print_test_header("文章 API 删除测试完成")
            self.print_success("删除相关测试已执行完成")
            return True
            
        except Exception as e:
            self.print_error(f"删除测试过程中发生异常: {str(e)}")
            return False

    def run_test_suite(self, include_cleanup: bool = None):
        """运行完整的文章API测试套件"""
        self.print_test_header("文章 API 测试套件")

        # 确定是否运行清理
        run_cleanup = include_cleanup if include_cleanup is not None else self.auto_cleanup

        # 检查服务器状态
        if not self.check_server_status():
            self.print_error("服务器未运行！请先启动服务器: go run main.go")
            return False

        self.print_success("服务器运行正常")

        try:
            # 设置测试用户
            if not self.setup_test_user():
                self.print_error("无法创建测试用户")
                return False

            # 运行基础测试（不包括删除测试）
            self.test_create_post()
            self.test_create_multiple_posts()
            self.test_create_invalid_post()
            self.test_get_post()
            self.test_get_nonexistent_post()
            self.test_invalid_post_id()
            self.test_update_post()
            self.test_verify_post_update()
            self.test_create_long_content_post()
            self.test_edge_cases()

            self.print_test_header("文章 API 基础测试完成")
            self.print_success("基础测试已执行完成")
            
            if len(self.created_post_ids) > 0:
                self.print_info(f"本次测试创建了 {len(self.created_post_ids)} 篇文章，ID: {self.created_post_ids}")
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
    test = PostAPITest()
    test.run_test_suite()


if __name__ == "__main__":
    main()
