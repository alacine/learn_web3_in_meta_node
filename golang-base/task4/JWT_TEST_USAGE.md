# JWT 认证测试使用指南

## 概述

所有API测试现在都支持JWT认证。主要变更：

1. **base_test.py** - 添加了JWT认证支持
2. **auth_helper.py** - 新增认证助手类
3. **所有测试文件** - 更新以支持JWT认证

## 测试运行方式

### 1. 用户API测试
```bash
cd tests
python test_user_api.py
```

测试流程：
- 创建用户（无需认证）
- 用户登录获取JWT token
- 使用token进行其他操作（获取、更新、删除用户）

### 2. 其他API测试（Post、Comment等）

这些测试继承自 `AuthenticatedAPITest`，会自动：
- 创建认证用户
- 登录获取JWT token
- 在所有API调用中使用token

### 3. 手动测试JWT认证

```python
from tests.base_test import BaseAPITest

# 创建测试实例
test = BaseAPITest()

# 注册用户
user_data = {"username": "testuser", "password": "testpass", "email": "test@example.com"}
response = test.make_request("POST", "/register", data=user_data, require_auth=False)

# 登录获取token
login_data = {"id": 1, "password": "testpass"}  # 使用返回的用户ID
response = test.make_request("POST", "/login", data=login_data, require_auth=False)

# 从响应中提取token并设置
token = response.json()["data"]["token"]
test.set_jwt_token(token)

# 现在可以进行需要认证的API调用
response = test.make_request("GET", "/user/1")  # 会自动使用JWT认证
```

## API认证要求

### 需要认证的端点：
- `GET /user/:id`
- `PUT /user`
- `DELETE /user/:id`
- 所有Post相关端点
- 所有Comment相关端点

### 无需认证的端点：
- `POST /register`
- `POST /login`

## 测试流程最佳实践

1. **创建用户** - 使用 `require_auth=False`
2. **登录获取token** - 使用 `require_auth=False`
3. **设置token** - 调用 `set_jwt_token(token)`
4. **进行认证测试** - 正常调用API（默认 `require_auth=True`）

## 错误处理

如果收到401未授权错误：
1. 检查是否调用了 `set_jwt_token()`
2. 检查token是否有效
3. 确认端点是否需要认证

## 示例：完整的认证测试流程

```python
# 1. 注册
response = test.make_request("POST", "/register", 
                           data={"username": "test", "password": "pass", "email": "test@example.com"}, 
                           require_auth=False)
user_id = response.json()["data"]["id"]

# 2. 登录
response = test.make_request("POST", "/login", 
                           data={"id": user_id, "password": "pass"}, 
                           require_auth=False)
token = response.json()["data"]["token"]
test.set_jwt_token(token)

# 3. 使用认证进行操作
response = test.make_request("GET", f"/user/{user_id}")  # 自动使用JWT
```