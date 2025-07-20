# Python HTTP API 测试套件

这是一套完整的Python HTTP API测试工具，用于测试博客系统的REST API接口。

## 🚀 快速开始

### 1. 安装依赖

使用 uv 管理Python依赖：

```bash
# 安装 uv (如果还没有)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安装项目依赖
uv sync
```

### 2. 启动服务

确保Go服务器和MySQL数据库正在运行：

```bash
# 启动MySQL数据库
docker-compose up -d

# 启动Go服务器
go run main.go
```

### 3. 运行测试

#### 方式一：交互式菜单

```bash
python run_tests.py
```

#### 方式二：命令行参数

```bash
# 运行所有测试
python run_tests.py --all

# 运行特定测试模块
python run_tests.py --user          # 用户API测试
python run_tests.py --post          # 文章API测试
python run_tests.py --comment       # 评论API测试
python run_tests.py --comprehensive # 综合测试

# 自定义API地址
python run_tests.py --all --base-url http://localhost:8080/api/v1
```

#### 方式三：直接运行测试模块

```bash
# 运行单个测试模块
python -m tests.test_user_api
python -m tests.test_post_api
python -m tests.test_comment_api
python -m tests.test_comprehensive
```

## 📦 项目结构

```
├── pyproject.toml              # 项目配置文件
├── run_tests.py               # 测试运行器
├── README_PYTHON_TESTS.md     # 说明文档
└── tests/                     # 测试模块目录
    ├── __init__.py
    ├── base_test.py           # 基础测试类
    ├── test_user_api.py       # 用户API测试
    ├── test_post_api.py       # 文章API测试
    ├── test_comment_api.py    # 评论API测试
    └── test_comprehensive.py  # 综合测试
```

## 🧪 测试模块说明

### 1. 用户API测试 (`test_user_api.py`)

测试功能：
- ✅ 用户注册（正常和异常情况）
- ✅ 用户登录验证
- ✅ 获取用户信息
- ✅ 更新用户信息
- ✅ 删除用户
- ✅ 边界条件测试

### 2. 文章API测试 (`test_post_api.py`)

测试功能：
- ✅ 文章创建（包括长内容）
- ✅ 文章获取和查询
- ✅ 文章更新操作
- ✅ 文章删除功能
- ✅ 无效数据处理
- ✅ 特殊字符支持

### 3. 评论API测试 (`test_comment_api.py`)

测试功能：
- ✅ 评论创建和管理
- ✅ 多语言和特殊字符
- ✅ 长评论内容支持
- ✅ 评论更新和删除
- ✅ 关联数据验证

### 4. 综合测试 (`test_comprehensive.py`)

模拟真实场景：
- 👥 多用户注册和认证
- 📝 博客文章创建和发布
- 💬 用户互动和评论
- ✏️ 内容更新和维护
- 🔍 数据检索和验证
- ⚠️ 错误场景处理
- 📊 测试报告生成

## 🎨 测试特性

### 彩色输出

使用 `colorama` 库提供彩色终端输出：
- 🟢 成功操作 - 绿色
- 🔴 错误信息 - 红色  
- 🟡 警告信息 - 黄色
- 🔵 普通信息 - 蓝色

### 详细日志

每个HTTP请求都会显示：
- 请求方法和URL
- 请求数据（JSON格式）
- 响应状态码
- 响应数据（格式化显示）

### 自动清理

测试完成后自动清理创建的测试数据，确保数据库的干净状态。

### 错误处理

完善的异常处理机制：
- 网络连接错误
- API响应错误
- 数据解析错误
- 测试执行异常

## 🔧 配置选项

### 基础配置

可以通过修改 `base_test.py` 中的 `BaseAPITest` 类来调整：

```python
class BaseAPITest:
    def __init__(self, base_url: str = "http://localhost:8000/api/v1"):
        self.base_url = base_url
        # 其他配置...
```

### 超时设置

HTTP请求超时可以在会话中配置：

```python
self.session.timeout = 30  # 30秒超时
```

## 📊 测试报告

综合测试会生成详细的测试报告，包括：
- 测试数据统计
- 用户和内容信息
- 交互行为分析
- 执行结果汇总

## 🐛 故障排除

### 常见问题

1. **服务器连接失败**
   ```
   ❌ 服务器未运行！请先启动服务器: go run main.go
   ```
   解决：确保Go服务器在8000端口运行

2. **依赖缺失**
   ```
   ❌ 缺少依赖: No module named 'requests'
   ```
   解决：运行 `uv sync` 安装依赖

3. **数据库连接错误**
   ```
   数据库连接失败
   ```
   解决：确保MySQL容器运行 `docker-compose up -d`

4. **端口冲突**
   ```
   连接被拒绝
   ```
   解决：检查端口8000是否被占用，或修改base_url

### 调试模式

如需更详细的调试信息，可以在测试代码中添加：

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🚀 扩展开发

### 添加新的测试模块

1. 继承 `BaseAPITest` 类
2. 实现 `run_test_suite()` 方法
3. 添加具体的测试方法
4. 在 `run_tests.py` 中注册新模块

示例：

```python
from tests.base_test import BaseAPITest

class NewAPITest(BaseAPITest):
    def run_test_suite(self):
        self.print_test_header("新功能测试")
        # 实现测试逻辑
        return True
```

### 自定义断言

可以扩展基类添加更多断言方法：

```python
def assert_user_data(self, response, expected_username):
    data = response.json()
    actual_username = data.get('data', {}).get('username')
    assert actual_username == expected_username
```

## 📝 最佳实践

1. **测试隔离**: 每个测试都应该是独立的，不依赖其他测试的结果
2. **数据清理**: 测试完成后清理创建的数据
3. **错误处理**: 妥善处理各种异常情况
4. **可读性**: 使用描述性的测试名称和日志信息
5. **参数化**: 对于相似的测试，使用参数化减少重复代码

## 🤝 贡献指南

欢迎提交Pull Request来改进测试套件：

1. Fork 项目
2. 创建功能分支
3. 添加测试用例
4. 确保所有测试通过
5. 提交PR

---

📧 如有问题或建议，欢迎提交Issue或PR！