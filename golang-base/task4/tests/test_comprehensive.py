"""
综合测试模块
模拟完整的博客系统工作流程，包括用户互动场景
"""

from .base_test import BaseAPITest
import json
import time


class ComprehensiveAPITest(BaseAPITest):
    """综合API测试类"""

    def __init__(self, base_url: str = "http://localhost:8000/api/v1", auto_cleanup: bool = True):
        super().__init__(base_url, auto_cleanup)
        self.test_users = []  # 存储测试用户信息
        self.test_posts = []  # 存储测试文章信息
        self.test_comments = []  # 存储测试评论信息

    def create_test_users(self):
        """创建测试用户"""
        self.print_step(1, "创建测试用户")

        users_data = [
            {
                "username": "alice",
                "password": "alice123",
                "email": "alice@example.com",
                "role": "博客作者",
            },
            {
                "username": "bob",
                "password": "bob123",
                "email": "bob@example.com",
                "role": "活跃读者",
            },
            {
                "username": "charlie",
                "password": "charlie123",
                "email": "charlie@example.com",
                "role": "偶尔评论者",
            },
        ]

        for user_data in users_data:
            print(f"\\n  👤 创建用户: {user_data['username']} ({user_data['role']})")

            response = self.make_request(
                "POST",
                "/register",
                data={
                    "username": user_data["username"],
                    "password": user_data["password"],
                    "email": user_data["email"],
                },
                expected_status=200,
                description=f"注册用户 {user_data['username']}",
            )

            if response.status_code == 200:
                user_id = self.extract_id_from_response(response)
                if user_id:
                    user_info = {
                        "id": user_id,
                        "username": user_data["username"],
                        "password": user_data["password"],
                        "email": user_data["email"],
                        "role": user_data["role"],
                    }
                    self.test_users.append(user_info)
                    self.print_success(
                        f"用户 {user_data['username']} 创建成功 (ID: {user_id})"
                    )

        return len(self.test_users) >= 3

    def test_user_authentication(self):
        """测试用户认证流程"""
        self.print_step(2, "用户认证流程测试")

        for user in self.test_users:
            print(f"\\n  🔐 测试用户 {user['username']} 登录")

            # 正确密码登录
            login_response = self.make_request(
                "POST",
                "/login",
                data={"id": user["id"], "password": user["password"]},
                expected_status=200,
                description=f"用户 {user['username']} 正确登录",
            )

            # 错误密码登录
            wrong_response = self.make_request(
                "POST",
                "/login",
                data={"id": user["id"], "password": "wrongpassword"},
                expected_status=401,
                description=f"用户 {user['username']} 错误密码登录",
            )

    def create_blog_posts(self):
        """创建博客文章"""
        self.print_step(3, "创建博客文章")

        if not self.test_users:
            self.print_error("没有可用的用户创建文章")
            return False

        # Alice 作为主要博客作者
        alice = next((u for u in self.test_users if u["username"] == "alice"), None)
        if not alice:
            self.print_error("找不到用户 Alice")
            return False

        posts_data = [
            {
                "title": "Go语言Web开发完整指南",
                "content": """Go语言以其简洁、高效和强大的并发特性，成为了现代Web开发的热门选择。

## 为什么选择Go？

1. **性能卓越**: 编译型语言，运行速度快
2. **并发支持**: 天生的goroutine支持
3. **简洁语法**: 学习曲线平缓
4. **强大生态**: 丰富的第三方库

## Web框架选择

### Gin框架优势
- 轻量级且高性能
- 中间件支持完善
- RESTful API友好
- 丰富的绑定和渲染功能

## 项目结构设计

```
project/
├── main.go          # 程序入口
├── api/             # API处理层
├── service/         # 业务逻辑层  
├── model/           # 数据模型
└── middleware/      # 中间件
```

## 数据库集成

使用GORM作为ORM工具，提供：
- 自动迁移功能
- 关联查询支持
- 事务处理
- 连接池管理

## 最佳实践

1. 错误处理要统一
2. 日志记录要完善
3. 配置管理要规范
4. 测试覆盖要充分

希望这篇文章对大家的Go语言学习有帮助！""",
                "author": alice,
                "tags": ["Go", "Web开发", "教程"],
            },
            {
                "title": "RESTful API设计原则与实践",
                "content": """RESTful API是现代Web服务的基石，良好的API设计能够提升开发效率和用户体验。

## REST基本原则

### 1. 统一接口
- 使用标准HTTP方法 (GET, POST, PUT, DELETE)
- 资源通过URI标识
- 通过表现层操作资源
- 超媒体作为应用状态引擎

### 2. 无状态性
每个请求都包含完整信息，服务器不保存客户端状态。

### 3. 可缓存性
响应数据应该明确标记是否可缓存。

### 4. 分层系统
客户端无需知道服务器架构的复杂性。

## API版本管理

推荐使用URL路径进行版本控制：
```
/api/v1/users
/api/v2/users
```

## 状态码使用规范

- 200: 成功
- 201: 创建成功
- 400: 客户端错误
- 401: 未授权
- 404: 资源不存在
- 500: 服务器错误

## 响应格式统一

```json
{
    "code": 0,
    "msg": "success",
    "data": {...}
}
```

遵循这些原则，你的API将更加标准和易用！""",
                "author": alice,
                "tags": ["API", "REST", "设计模式"],
            },
            {
                "title": "数据库性能优化实战",
                "content": """数据库性能是应用系统的关键瓶颈，掌握优化技巧至关重要。

## 索引优化

### 1. 选择合适的索引类型
- B-Tree索引：适用于等值和范围查询
- 哈希索引：适用于等值查询
- 全文索引：适用于文本搜索

### 2. 复合索引设计
- 遵循最左前缀原则
- 考虑字段的选择性
- 避免过多的索引

## 查询优化

### 1. SQL语句优化
```sql
-- 避免SELECT *
SELECT id, name FROM users WHERE status = 1;

-- 使用LIMIT限制结果集
SELECT * FROM posts ORDER BY created_at DESC LIMIT 10;

-- 合理使用JOIN
SELECT u.name, p.title 
FROM users u 
JOIN posts p ON u.id = p.user_id;
```

### 2. 执行计划分析
使用EXPLAIN分析查询性能：
```sql
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';
```

## 架构优化

### 1. 读写分离
- 主库处理写操作
- 从库处理读操作
- 通过中间件实现自动路由

### 2. 分库分表
- 垂直分库：按业务模块
- 水平分表：按数据量
- 注意跨库事务问题

## 连接池配置

合理配置数据库连接池参数：
- max_connections: 最大连接数
- idle_timeout: 空闲超时时间
- max_lifetime: 连接最大生存时间

持续监控和优化，让你的数据库性能更上一层楼！""",
                "author": alice,
                "tags": ["数据库", "性能优化", "MySQL"],
            },
        ]

        for i, post_data in enumerate(posts_data, 1):
            print(f"\\n  📝 创建文章 {i}: {post_data['title']}")

            response = self.make_request(
                "POST",
                "/post",
                data={
                    "title": post_data["title"],
                    "content": post_data["content"],
                    "user_id": post_data["author"]["id"],
                },
                expected_status=200,
                description=f"创建文章: {post_data['title']}",
            )

            if response.status_code == 200:
                post_id = self.extract_id_from_response(response)
                if post_id:
                    post_info = {
                        "id": post_id,
                        "title": post_data["title"],
                        "author": post_data["author"],
                        "tags": post_data["tags"],
                    }
                    self.test_posts.append(post_info)
                    self.print_success(f"文章创建成功 (ID: {post_id})")

        return len(self.test_posts) >= 3

    def simulate_user_interactions(self):
        """模拟用户互动"""
        self.print_step(4, "模拟用户互动场景")

        if not self.test_posts or len(self.test_users) < 2:
            self.print_error("缺少文章或用户数据")
            return False

        # Bob 作为活跃读者，对所有文章发表评论
        bob = next((u for u in self.test_users if u["username"] == "bob"), None)
        charlie = next((u for u in self.test_users if u["username"] == "charlie"), None)

        if not bob or not charlie:
            self.print_error("找不到测试用户")
            return False

        # Bob 对每篇文章的详细评论
        bob_comments = [
            "这篇Go语言教程写得太棒了！作为初学者，我从中学到了很多实用的知识。特别是项目结构设计部分，对我的实际项目很有帮助。期待更多这样的高质量内容！👍",
            "RESTful API设计一直是我的弱项，这篇文章让我对REST原则有了更深入的理解。特别是状态码的使用规范和响应格式统一，我会在下个项目中应用这些最佳实践。感谢分享！",
            "数据库性能优化是个永恒的话题。文章中提到的索引优化和查询优化技巧很实用，我刚好遇到了慢查询问题，按照文章的建议优化后效果显著。读写分离的架构设计也给了我新的思路。",
        ]

        # Charlie 的简短评论
        charlie_comments = [
            "不错的教程，收藏了！",
            "学习了，API设计确实需要规范化。",
            "数据库优化很重要，感谢分享经验。",
        ]

        print("\\n  💬 Bob 发表详细评论")
        for i, post in enumerate(self.test_posts):
            comment_content = (
                bob_comments[i] if i < len(bob_comments) else "很有用的文章，学习了！"
            )

            response = self.make_request(
                "POST",
                "/comment",
                data={
                    "content": comment_content,
                    "user_id": bob["id"],
                    "post_id": post["id"],
                },
                expected_status=200,
                description=f"Bob 评论文章: {post['title'][:20]}...",
            )

            if response.status_code == 200:
                comment_id = self.extract_id_from_response(response)
                if comment_id:
                    self.test_comments.append(
                        {
                            "id": comment_id,
                            "author": bob,
                            "post": post,
                            "content": comment_content[:30] + "...",
                        }
                    )

        print("\\n  💬 Charlie 发表简短评论")
        for i, post in enumerate(self.test_posts[:2]):  # Charlie 只评论前两篇
            comment_content = (
                charlie_comments[i] if i < len(charlie_comments) else "不错！"
            )

            response = self.make_request(
                "POST",
                "/comment",
                data={
                    "content": comment_content,
                    "user_id": charlie["id"],
                    "post_id": post["id"],
                },
                expected_status=200,
                description=f"Charlie 评论文章: {post['title'][:20]}...",
            )

            if response.status_code == 200:
                comment_id = self.extract_id_from_response(response)
                if comment_id:
                    self.test_comments.append(
                        {
                            "id": comment_id,
                            "author": charlie,
                            "post": post,
                            "content": comment_content,
                        }
                    )

        return True

    def test_content_updates(self):
        """测试内容更新功能"""
        self.print_step(5, "内容更新功能测试")

        if not self.test_posts or not self.test_comments:
            self.print_error("缺少测试数据")
            return False

        # Alice 更新她的第一篇文章
        alice = next((u for u in self.test_users if u["username"] == "alice"), None)
        first_post = self.test_posts[0]

        print("\\n  ✏️ Alice 更新文章内容")
        updated_content = (
            first_post.get("original_content", "")
            + """

## 更新内容 (2024年版)

根据读者反馈，我添加了一些新的内容：

### 微服务架构支持
Go语言在微服务架构中表现出色：
- 轻量级容器化支持
- 服务发现和配置管理
- 分布式追踪和监控

### 安全最佳实践
- JWT认证实现
- HTTPS配置
- 输入验证和防护
- SQL注入预防

### 部署和运维
- Docker容器化
- Kubernetes编排
- CI/CD流水线
- 监控和日志收集

感谢各位读者的建议和反馈！如有问题欢迎继续讨论。

---
*更新时间: 2024年*
*新增内容: 微服务、安全、部署*"""
        )

        response = self.make_request(
            "PUT",
            "/post",
            data={
                "id": first_post["id"],
                "title": first_post["title"] + " (2024更新版)",
                "content": updated_content,
                "user_id": alice["id"],
            },
            expected_status=200,
            description="Alice 更新文章内容",
        )

        # Bob 更新他的一条评论
        if self.test_comments:
            bob_comment = next(
                (c for c in self.test_comments if c["author"]["username"] == "bob"),
                None,
            )
            if bob_comment:
                print("\\n  ✏️ Bob 更新评论内容")
                updated_comment = (
                    bob_comment["content"]
                    + "\\n\\n**更新**: 看到作者更新了文章内容，新增的微服务和安全部分很及时！正好我们公司在考虑微服务架构，这些内容来得正是时候。"
                )

                self.make_request(
                    "PUT",
                    "/comment",
                    data={
                        "id": bob_comment["id"],
                        "content": updated_comment,
                        "user_id": bob_comment["author"]["id"],
                        "post_id": bob_comment["post"]["id"],
                    },
                    expected_status=200,
                    description="Bob 更新评论内容",
                )

        return True

    def test_data_retrieval(self):
        """测试数据检索功能"""
        self.print_step(6, "数据检索功能测试")

        print("\\n  🔍 检索所有用户信息")
        for user in self.test_users:
            response = self.make_request(
                "GET",
                f"/user/{user['id']}",
                expected_status=200,
                description=f"获取用户 {user['username']} 信息",
            )

        print("\\n  🔍 检索所有文章信息")
        for post in self.test_posts:
            response = self.make_request(
                "GET",
                f"/post/{post['id']}",
                expected_status=200,
                description=f"获取文章: {post['title'][:30]}...",
            )

        print("\\n  🔍 检索所有评论信息")
        for comment in self.test_comments:
            response = self.make_request(
                "GET",
                f"/comment/{comment['id']}",
                expected_status=200,
                description=f"获取评论: {comment['content'][:20]}...",
            )

        return True

    def test_error_scenarios(self):
        """测试错误场景"""
        self.print_step(7, "错误场景测试")

        error_tests = [
            {
                "name": "访问不存在的用户",
                "request": ("GET", "/user/99999", None),
                "expected_status": 500,
            },
            {
                "name": "访问不存在的文章",
                "request": ("GET", "/post/99999", None),
                "expected_status": 500,
            },
            {
                "name": "访问不存在的评论",
                "request": ("GET", "/comment/99999", None),
                "expected_status": 500,
            },
            {
                "name": "无效ID格式测试",
                "request": ("GET", "/user/abc", None),
                "expected_status": 400,
            },
            {
                "name": "重复用户名注册",
                "request": (
                    "POST",
                    "/register",
                    {
                        "username": "alice",
                        "password": "test123",
                        "email": "alice2@example.com",
                    },
                ),
                "expected_status": 400,
            },
        ]

        for test in error_tests:
            print(f"\\n  ⚠️ {test['name']}")
            method, endpoint, data = test["request"]
            self.make_request(
                method,
                endpoint,
                data=data,
                expected_status=test["expected_status"],
                description=test["name"],
            )

        return True

    def generate_test_report(self):
        """生成测试报告"""
        self.print_step(8, "生成测试报告")

        report = {
            "测试概览": {
                "测试用户数": len(self.test_users),
                "测试文章数": len(self.test_posts),
                "测试评论数": len(self.test_comments),
            },
            "用户信息": [
                {
                    "用户名": user["username"],
                    "角色": user["role"],
                    "邮箱": user["email"],
                }
                for user in self.test_users
            ],
            "文章信息": [
                {
                    "标题": post["title"],
                    "作者": post["author"]["username"],
                    "标签": post.get("tags", []),
                }
                for post in self.test_posts
            ],
            "评论统计": {
                "总评论数": len(self.test_comments),
                "Bob的评论": len(
                    [c for c in self.test_comments if c["author"]["username"] == "bob"]
                ),
                "Charlie的评论": len(
                    [
                        c
                        for c in self.test_comments
                        if c["author"]["username"] == "charlie"
                    ]
                ),
            },
        }

        print("\\n📊 测试报告:")
        print(json.dumps(report, ensure_ascii=False, indent=2))

        return report

    def cleanup_test_data(self):
        """清理测试数据"""
        self.print_step(9, "清理测试数据")

        # 清理评论
        print("\\n  🗑️ 清理评论数据")
        for comment in self.test_comments[:]:
            try:
                response = self.make_request(
                    "DELETE",
                    f"/comment/{comment['id']}",
                    expected_status=200,
                    description=f"删除评论 ID: {comment['id']}",
                )
                if response.status_code == 200:
                    self.test_comments.remove(comment)
            except Exception as e:
                self.print_error(f"清理评论失败: {str(e)}")

        # 清理文章
        print("\\n  🗑️ 清理文章数据")
        for post in self.test_posts[:]:
            try:
                response = self.make_request(
                    "DELETE",
                    f"/post/{post['id']}",
                    expected_status=200,
                    description=f"删除文章: {post['title'][:30]}...",
                )
                if response.status_code == 200:
                    self.test_posts.remove(post)
            except Exception as e:
                self.print_error(f"清理文章失败: {str(e)}")

        # 清理用户
        print("\\n  🗑️ 清理用户数据")
        for user in self.test_users[:]:
            try:
                response = self.make_request(
                    "DELETE",
                    f"/user/{user['id']}",
                    expected_status=200,
                    description=f"删除用户: {user['username']}",
                )
                if response.status_code == 200:
                    self.test_users.remove(user)
            except Exception as e:
                self.print_error(f"清理用户失败: {str(e)}")
    
    def run_cleanup_tests(self):
        """运行删除相关测试"""
        self.print_test_header("综合删除测试")
        
        try:
            self.cleanup_test_data()
            
            self.print_test_header("综合删除测试完成")
            self.print_success("删除相关测试已执行完成")
            return True
            
        except Exception as e:
            self.print_error(f"删除测试过程中发生异常: {str(e)}")
            return False

    def run_test_suite(self, include_cleanup: bool = None):
        """运行完整的综合测试套件"""
        self.print_test_header("博客系统综合测试套件")

        # 确定是否运行清理
        run_cleanup = include_cleanup if include_cleanup is not None else self.auto_cleanup

        # 检查服务器状态
        if not self.check_server_status():
            self.print_error("服务器未运行！请先启动服务器: go run main.go")
            return False

        self.print_success("服务器运行正常，开始综合测试...")

        try:
            # 执行测试流程（不包括删除操作）
            success = True
            success &= self.create_test_users()
            success &= self.test_user_authentication()
            success &= self.create_blog_posts()
            success &= self.simulate_user_interactions()
            success &= self.test_content_updates()
            success &= self.test_data_retrieval()
            success &= self.test_error_scenarios()

            # 生成测试报告
            self.generate_test_report()

            self.print_test_header("综合测试完成")
            if success:
                self.print_success("🎉 所有测试场景执行成功！")
                self.print_info("✅ 用户注册和认证 - 通过")
                self.print_info("✅ 文章创建和管理 - 通过")
                self.print_info("✅ 用户互动和评论 - 通过")
                self.print_info("✅ 内容更新功能 - 通过")
                self.print_info("✅ 数据检索功能 - 通过")
                self.print_info("✅ 错误场景处理 - 通过")
                
                # 显示创建的测试数据统计
                total_users = len(self.test_users)
                total_posts = len(self.test_posts)
                total_comments = len(self.test_comments)
                self.print_info(f"📊 测试数据统计: {total_users}个用户, {total_posts}篇文章, {total_comments}条评论")
                
                if not run_cleanup:
                    self.print_warning("测试数据未自动清理，如需清理请运行删除测试选项")
            else:
                self.print_warning("⚠️ 部分测试场景未完全成功")

            return success

        except Exception as e:
            self.print_error(f"综合测试过程中发生异常: {str(e)}")
            return False

        finally:
            # 根据设置决定是否清理测试数据
            if run_cleanup:
                self.cleanup_test_data()


def main():
    """主函数"""
    test = ComprehensiveAPITest()
    test.run_test_suite()


if __name__ == "__main__":
    main()
