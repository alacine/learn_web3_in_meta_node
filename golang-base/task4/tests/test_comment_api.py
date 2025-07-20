"""
评论API测试模块
测试评论创建、获取、更新、删除等功能
"""

from .base_test import BaseAPITest
import json


class CommentAPITest(BaseAPITest):
    """评论API测试类"""

    def __init__(self, base_url: str = "http://localhost:8000/api/v1", auto_cleanup: bool = True):
        super().__init__(base_url, auto_cleanup)
        self.created_user_ids = []  # 记录创建的用户ID
        self.created_post_ids = []  # 记录创建的文章ID
        self.created_comment_ids = []  # 记录创建的评论ID用于清理

    def setup_test_data(self):
        """设置测试数据（用户和文章）"""
        self.print_step(0, "准备测试数据")

        # 创建测试用户
        print("\\n  👤 创建评论者用户")
        user_data = {
            "username": "commenter",
            "password": "password123",
            "email": "commenter@example.com",
        }

        user_response = self.make_request(
            "POST",
            "/register",
            data=user_data,
            expected_status=200,
            description="创建评论者用户",
        )

        if user_response.status_code == 200:
            user_id = self.extract_id_from_response(user_response)
            if user_id:
                self.created_user_ids.append(user_id)
                self.print_info(f"创建用户ID: {user_id}")

        # 创建测试文章
        if self.created_user_ids:
            print("\\n  📄 创建可评论的文章")
            post_data = {
                "title": "可评论的文章",
                "content": "这是一篇可以被评论的文章内容，欢迎大家积极评论和讨论。",
                "user_id": self.created_user_ids[0],
            }

            post_response = self.make_request(
                "POST",
                "/post",
                data=post_data,
                expected_status=200,
                description="创建测试文章",
            )

            if post_response.status_code == 200:
                post_id = self.extract_id_from_response(post_response)
                if post_id:
                    self.created_post_ids.append(post_id)
                    self.print_info(f"创建文章ID: {post_id}")

        return len(self.created_user_ids) > 0 and len(self.created_post_ids) > 0

    def test_create_comment(self):
        """测试创建评论"""
        self.print_step(1, "创建评论测试")

        if not self.created_user_ids or not self.created_post_ids:
            self.print_warning("缺少测试数据（用户或文章）")
            return None

        comment_data = {
            "content": "这是第一条评论，内容很棒！",
            "user_id": self.created_user_ids[0],
            "post_id": self.created_post_ids[0],
        }

        response = self.make_request(
            "POST",
            "/comment",
            data=comment_data,
            expected_status=200,
            description="创建第一条评论",
        )

        if response.status_code == 200:
            comment_id = self.extract_id_from_response(response)
            if comment_id:
                self.created_comment_ids.append(comment_id)
                self.print_info(f"创建评论ID: {comment_id}")

        return response

    def test_create_multiple_comments(self):
        """测试创建多条评论"""
        self.print_step(2, "创建多条评论测试")

        if not self.created_user_ids or not self.created_post_ids:
            self.print_warning("缺少测试数据")
            return []

        user_id = self.created_user_ids[0]
        post_id = self.created_post_ids[0]

        comments_data = [
            {
                "content": "我也来评论一下，感谢分享！",
                "user_id": user_id,
                "post_id": post_id,
            },
            {
                "content": "这篇文章写得很详细，学到了很多东西。",
                "user_id": user_id,
                "post_id": post_id,
            },
            {
                "content": "期待作者分享更多这样的高质量内容！👍",
                "user_id": user_id,
                "post_id": post_id,
            },
        ]

        responses = []
        for i, comment_data in enumerate(comments_data, 1):
            print(f"\\n  💬 创建评论 {i}")
            response = self.make_request(
                "POST",
                "/comment",
                data=comment_data,
                expected_status=200,
                description=f"创建评论 {i}",
            )

            if response.status_code == 200:
                comment_id = self.extract_id_from_response(response)
                if comment_id:
                    self.created_comment_ids.append(comment_id)
                    self.print_info(f"创建评论ID: {comment_id}")

            responses.append(response)

        return responses

    def test_create_long_comment(self):
        """测试创建长评论"""
        self.print_step(3, "创建长评论测试")

        if not self.created_user_ids or not self.created_post_ids:
            self.print_warning("缺少测试数据")
            return None

        long_content = """这是一条比较长的评论，我想详细说明一下我的观点：

首先，这篇文章的主题很有趣，作者从多个角度分析了问题，展现了深厚的技术功底。

其次，文章的结构清晰，逻辑性强，读起来很流畅。特别是以下几个方面：
1. 问题分析很到位
2. 解决方案具有实用性
3. 代码示例清晰易懂
4. 总结部分点题很好

最后，希望作者能够继续分享这样的高质量内容。作为读者，我从中学到了很多实用的技术知识和经验。

期待下一篇文章！🚀

---
评论者：热心读者
时间：刚刚"""

        comment_data = {
            "content": long_content,
            "user_id": self.created_user_ids[0],
            "post_id": self.created_post_ids[0],
        }

        response = self.make_request(
            "POST",
            "/comment",
            data=comment_data,
            expected_status=200,
            description="创建长评论",
        )

        if response.status_code == 200:
            comment_id = self.extract_id_from_response(response)
            if comment_id:
                self.created_comment_ids.append(comment_id)
                self.print_info(f"创建长评论ID: {comment_id}")

        return response

    def test_create_invalid_comment(self):
        """测试创建无效评论"""
        self.print_step(4, "创建无效评论测试")

        if not self.created_user_ids or not self.created_post_ids:
            self.print_warning("缺少测试数据")
            return None

        # 测试空内容评论
        invalid_comment = {
            "content": "",
            "user_id": self.created_user_ids[0],
            "post_id": self.created_post_ids[0],
        }

        response = self.make_request(
            "POST",
            "/comment",
            data=invalid_comment,
            expected_status=400,  # 期望失败
            description="创建空内容评论（应该失败）",
        )

        return response

    def test_get_comment(self):
        """测试获取评论"""
        self.print_step(5, "获取评论测试")

        if not self.created_comment_ids:
            self.print_warning("没有可用的评论进行测试")
            return None

        comment_id = self.created_comment_ids[0]
        response = self.make_request(
            "GET",
            f"/comment/{comment_id}",
            expected_status=200,
            description=f"获取评论 (ID: {comment_id})",
        )

        return response

    def test_get_nonexistent_comment(self):
        """测试获取不存在的评论"""
        self.print_step(6, "获取不存在的评论测试")

        response = self.make_request(
            "GET",
            "/comment/99999",
            expected_status=500,  # 根据实际API调整
            description="获取不存在的评论",
        )

        return response

    def test_invalid_comment_id(self):
        """测试无效的评论ID"""
        self.print_step(7, "无效评论ID测试")

        response = self.make_request(
            "GET", "/comment/abc", expected_status=400, description="无效评论ID测试"
        )

        return response

    def test_update_comment(self):
        """测试更新评论"""
        self.print_step(8, "更新评论测试")

        if (
            not self.created_comment_ids
            or not self.created_user_ids
            or not self.created_post_ids
        ):
            self.print_warning("缺少测试数据")
            return None

        comment_id = self.created_comment_ids[0]
        update_data = {
            "id": comment_id,
            "content": "这是更新后的评论内容，添加了更多细节和想法。原来的评论已经被修改，现在包含了更完整的观点。",
            "user_id": self.created_user_ids[0],
            "post_id": self.created_post_ids[0],
        }

        response = self.make_request(
            "PUT",
            "/comment",
            data=update_data,
            expected_status=200,
            description="更新评论内容",
        )

        return response

    def test_verify_comment_update(self):
        """验证评论更新"""
        self.print_step(9, "验证评论更新")

        if not self.created_comment_ids:
            self.print_warning("没有可用的评论进行验证")
            return None

        comment_id = self.created_comment_ids[0]
        response = self.make_request(
            "GET",
            f"/comment/{comment_id}",
            expected_status=200,
            description="验证评论更新结果",
        )

        # 检查评论内容是否已更新
        try:
            data = response.json()
            content = data.get("data", {}).get("content", "")
            if "更新后的评论内容" in content:
                self.print_success("评论更新验证成功")
            else:
                self.print_error("评论更新验证失败")
        except:
            self.print_error("无法验证评论更新结果")

        return response

    def test_special_characters_comment(self):
        """测试包含特殊字符的评论"""
        self.print_step(10, "特殊字符评论测试")

        if not self.created_user_ids or not self.created_post_ids:
            self.print_warning("缺少测试数据")
            return None

        special_content = """这条评论包含各种特殊字符和多语言内容：

英文: Hello World! @#$%^&*()_+{}|:"<>?[]\\;',./ 
中文: 你好世界！《》【】，。；：''""？！
日文: こんにちは世界！
韩文: 안녕하세요 세계!
表情: 😀😃😄😁😆😅🤣😂🙂🙃😉😊😇
符号: ★☆♦♠♣♥♡♢♧♤✓✗✘✚✪✧✦✤✥✣✢

代码示例:
```go
func main() {
    fmt.Println("Hello, 世界!")
}
```

HTML标签测试: <script>alert('test')</script> <b>加粗</b> <i>斜体</i>

特殊Unicode: ℃ ℉ ™ © ® ℅ № ℓ ℮ ⅛ ⅜ ⅝ ⅞"""

        comment_data = {
            "content": special_content,
            "user_id": self.created_user_ids[0],
            "post_id": self.created_post_ids[0],
        }

        response = self.make_request(
            "POST",
            "/comment",
            data=comment_data,
            expected_status=200,
            description="创建包含特殊字符的评论",
        )

        if response.status_code == 200:
            comment_id = self.extract_id_from_response(response)
            if comment_id:
                self.created_comment_ids.append(comment_id)
                self.print_info(f"创建特殊字符评论ID: {comment_id}")

        return response

    def test_comment_on_nonexistent_post(self):
        """测试对不存在文章的评论"""
        self.print_step(11, "对不存在文章评论测试")

        if not self.created_user_ids:
            self.print_warning("缺少用户数据")
            return None

        comment_data = {
            "content": "这是对不存在文章的评论",
            "user_id": self.created_user_ids[0],
            "post_id": 99999,  # 不存在的文章ID
        }

        response = self.make_request(
            "POST",
            "/comment",
            data=comment_data,
            expected_status=500,  # 期望失败
            description="对不存在文章的评论",
        )

        return response

    def test_delete_comment(self):
        """测试删除评论"""
        self.print_step(12, "删除评论测试")

        if len(self.created_comment_ids) < 2:
            # 创建一个临时评论用于删除
            if self.created_user_ids and self.created_post_ids:
                temp_comment = {
                    "content": "这条评论将被删除",
                    "user_id": self.created_user_ids[0],
                    "post_id": self.created_post_ids[0],
                }

                create_response = self.make_request(
                    "POST",
                    "/comment",
                    data=temp_comment,
                    expected_status=200,
                    description="创建临时评论用于删除测试",
                )

                if create_response.status_code == 200:
                    temp_comment_id = self.extract_id_from_response(create_response)
                    if temp_comment_id:
                        self.created_comment_ids.append(temp_comment_id)

        if not self.created_comment_ids:
            self.print_warning("没有可用的评论进行删除测试")
            return None

        # 删除最后一个创建的评论
        comment_id = self.created_comment_ids[-1]
        response = self.make_request(
            "DELETE",
            f"/comment/{comment_id}",
            expected_status=200,
            description=f"删除评论 (ID: {comment_id})",
        )

        if response.status_code == 200:
            self.created_comment_ids.remove(comment_id)

        return response

    def test_verify_deletion(self):
        """验证删除操作"""
        self.print_step(13, "验证删除操作")

        # 创建并删除一个临时评论
        if not self.created_user_ids or not self.created_post_ids:
            self.print_warning("缺少测试数据")
            return None

        temp_comment = {
            "content": "删除验证测试评论",
            "user_id": self.created_user_ids[0],
            "post_id": self.created_post_ids[0],
        }

        # 创建临时评论
        create_response = self.make_request(
            "POST",
            "/comment",
            data=temp_comment,
            expected_status=200,
            description="创建用于删除验证的临时评论",
        )

        if create_response.status_code == 200:
            temp_comment_id = self.extract_id_from_response(create_response)

            if temp_comment_id:
                # 删除临时评论
                self.make_request(
                    "DELETE",
                    f"/comment/{temp_comment_id}",
                    expected_status=200,
                    description="删除临时评论",
                )

                # 尝试获取已删除的评论
                response = self.make_request(
                    "GET",
                    f"/comment/{temp_comment_id}",
                    expected_status=500,  # 期望获取失败
                    description="尝试获取已删除评论",
                )

                return response

        return None

    def test_edge_cases(self):
        """测试边界情况"""
        self.print_step(14, "边界情况测试")

        if not self.created_user_ids or not self.created_post_ids:
            self.print_warning("缺少测试数据")
            return

        user_id = self.created_user_ids[0]
        post_id = self.created_post_ids[0]

        edge_cases = [
            {
                "name": "空评论内容",
                "data": {"content": "", "user_id": user_id, "post_id": post_id},
                "expected_status": 400,
            },
            {
                "name": "只有空格的评论",
                "data": {"content": "   ", "user_id": user_id, "post_id": post_id},
                "expected_status": 400,
            },
            {
                "name": "超长评论",
                "data": {
                    "content": "很" * 10000,
                    "user_id": user_id,
                    "post_id": post_id,
                },
                "expected_status": 400,
            },
            {
                "name": "不存在的用户ID",
                "data": {"content": "测试评论", "user_id": 99999, "post_id": post_id},
                "expected_status": 500,
            },
            {
                "name": "不存在的文章ID",
                "data": {"content": "测试评论", "user_id": user_id, "post_id": 99999},
                "expected_status": 500,
            },
            {
                "name": "单字符评论",
                "data": {"content": "好", "user_id": user_id, "post_id": post_id},
                "expected_status": 200,
            },
        ]

        for case in edge_cases:
            print(f"\\n  🧪 测试案例: {case['name']}")
            response = self.make_request(
                "POST",
                "/comment",
                data=case["data"],
                expected_status=case["expected_status"],
                description=case["name"],
            )

            # 如果创建成功，记录ID用于清理
            if response.status_code == 200:
                comment_id = self.extract_id_from_response(response)
                if comment_id:
                    self.created_comment_ids.append(comment_id)

    def cleanup(self):
        """清理测试数据"""
        self.print_step(15, "清理测试数据")

        # 清理评论
        for comment_id in self.created_comment_ids[:]:
            try:
                response = self.make_request(
                    "DELETE",
                    f"/comment/{comment_id}",
                    expected_status=200,
                    description=f"清理评论 ID: {comment_id}",
                )
                if response.status_code == 200:
                    self.created_comment_ids.remove(comment_id)
            except Exception as e:
                self.print_error(f"清理评论 {comment_id} 失败: {str(e)}")

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
        self.print_test_header("评论 API 删除测试")
        
        try:
            self.test_delete_comment()
            self.test_verify_deletion()
            
            self.print_test_header("评论 API 删除测试完成")
            self.print_success("删除相关测试已执行完成")
            return True
            
        except Exception as e:
            self.print_error(f"删除测试过程中发生异常: {str(e)}")
            return False

    def run_test_suite(self, include_cleanup: bool = None):
        """运行完整的评论API测试套件"""
        self.print_test_header("评论 API 测试套件")

        # 确定是否运行清理
        run_cleanup = include_cleanup if include_cleanup is not None else self.auto_cleanup

        # 检查服务器状态
        if not self.check_server_status():
            self.print_error("服务器未运行！请先启动服务器: go run main.go")
            return False

        self.print_success("服务器运行正常")

        try:
            # 设置测试数据
            if not self.setup_test_data():
                self.print_error("无法创建测试数据")
                return False

            # 运行基础测试（不包括删除测试）
            self.test_create_comment()
            self.test_create_multiple_comments()
            self.test_create_long_comment()
            self.test_create_invalid_comment()
            self.test_get_comment()
            self.test_get_nonexistent_comment()
            self.test_invalid_comment_id()
            self.test_update_comment()
            self.test_verify_comment_update()
            self.test_special_characters_comment()
            self.test_comment_on_nonexistent_post()
            self.test_edge_cases()

            self.print_test_header("评论 API 基础测试完成")
            self.print_success("基础测试已执行完成")
            
            if len(self.created_comment_ids) > 0:
                self.print_info(f"本次测试创建了 {len(self.created_comment_ids)} 条评论，ID: {self.created_comment_ids}")
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
    test = CommentAPITest()
    test.run_test_suite()


if __name__ == "__main__":
    main()
