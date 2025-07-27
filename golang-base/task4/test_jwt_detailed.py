#!/usr/bin/env python3
"""
详细的JWT过期测试
包括解析JWT payload并验证过期时间
"""

import requests
import json
import base64
import time
import uuid
from datetime import datetime, timedelta
from colorama import Fore, Style, init

# 初始化colorama
init(autoreset=True)

def print_step(step, desc):
    print(f"\n{Fore.YELLOW}📋 步骤{step}: {desc}{Style.RESET_ALL}")

def print_success(msg):
    print(f"{Fore.GREEN}✅ {msg}{Style.RESET_ALL}")

def print_error(msg):
    print(f"{Fore.RED}❌ {msg}{Style.RESET_ALL}")

def print_info(msg):
    print(f"{Fore.BLUE}ℹ️  {msg}{Style.RESET_ALL}")

def decode_jwt_payload(token):
    """解析JWT payload（不验证签名）"""
    try:
        # JWT格式: header.payload.signature
        parts = token.split('.')
        if len(parts) != 3:
            return None
        
        # Base64解码payload
        payload = parts[1]
        # 添加padding如果需要
        payload += '=' * (-len(payload) % 4)
        decoded = base64.urlsafe_b64decode(payload)
        
        return json.loads(decoded.decode('utf-8'))
    except Exception as e:
        print_error(f"解析JWT失败: {e}")
        return None

def test_jwt_expiration_detailed():
    base_url = "http://localhost:8000/api/v1"
    
    print(f"{Fore.CYAN}{'=' * 70}")
    print(f"{Fore.CYAN}JWT 过期时间详细测试{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 70}")
    
    try:
        # 生成唯一用户
        unique_id = str(uuid.uuid4())[:8]
        username = f"jwtexp_{unique_id}"
        password = "testpass123"
        email = f"{username}@example.com"
        
        # 步骤1: 注册用户
        print_step(1, f"注册测试用户: {username}")
        register_data = {
            "username": username,
            "password": password,
            "email": email
        }
        
        response = requests.post(f"{base_url}/register", json=register_data)
        if response.status_code != 200:
            print_error("用户注册失败")
            print(response.json())
            return False
        
        user_data = response.json()["data"]
        user_id = user_data["id"]
        print_success(f"用户注册成功，ID: {user_id}")
        
        # 步骤2: 登录获取JWT token
        print_step(2, "登录获取JWT token")
        login_data = {
            "id": user_id,
            "password": password
        }
        
        response = requests.post(f"{base_url}/login", json=login_data)
        if response.status_code != 200:
            print_error("登录失败")
            print(response.json())
            return False
        
        login_response = response.json()["data"]
        token = login_response["token"]
        print_success("登录成功，获取到JWT token")
        print_info(f"Token: {token[:50]}...{token[-20:]}")
        
        # 步骤3: 解析JWT payload
        print_step(3, "解析JWT token内容")
        payload = decode_jwt_payload(token)
        
        if payload:
            print_info("JWT Payload内容:")
            for key, value in payload.items():
                if key in ['exp', 'iat']:
                    # 转换时间戳为可读格式
                    dt = datetime.fromtimestamp(value)
                    print_info(f"  {key}: {value} ({dt.strftime('%Y-%m-%d %H:%M:%S')})")
                else:
                    print_info(f"  {key}: {value}")
            
            # 检查过期时间
            if 'exp' in payload and 'iat' in payload:
                exp_time = datetime.fromtimestamp(payload['exp'])
                iat_time = datetime.fromtimestamp(payload['iat'])
                duration = exp_time - iat_time
                now = datetime.now()
                
                print_info(f"当前时间: {now.strftime('%Y-%m-%d %H:%M:%S')}")
                print_info(f"令牌有效期: {duration}")
                print_info(f"剩余时间: {exp_time - now}")
                
                if duration.total_seconds() == 24 * 3600:
                    print_success("JWT过期时间设置正确（24小时）")
                else:
                    print_error(f"JWT过期时间异常: {duration}")
            else:
                print_error("JWT中缺少时间信息")
        else:
            print_error("无法解析JWT payload")
        
        # 步骤4: 测试有效token
        print_step(4, "验证有效token访问")
        headers = {"Authorization": f"Bearer {token}"}
        
        response = requests.get(f"{base_url}/user/{user_id}", headers=headers)
        if response.status_code == 200:
            print_success("有效token访问成功")
        else:
            print_error(f"有效token访问失败: {response.status_code}")
            print_error(f"错误信息: {response.json()}")
        
        # 步骤5: 创建一个手工过期的token（使用过去的时间）
        print_step(5, "测试手工创建的过期token")
        try:
            import jwt as pyjwt
            
            # 创建一个已过期的token（1秒前过期）
            expired_payload = {
                "id": user_id,
                "username": username,
                "iat": int(time.time()) - 3600,  # 1小时前签发
                "exp": int(time.time()) - 1      # 1秒前过期
            }
            
            expired_token = pyjwt.encode(expired_payload, "mock secrect key", algorithm="HS256")
            print_info(f"过期token: {expired_token[:50]}...")
            
            headers = {"Authorization": f"Bearer {expired_token}"}
            response = requests.get(f"{base_url}/user/{user_id}", headers=headers)
            
            if response.status_code == 401:
                print_success("过期token正确被拒绝")
                error_msg = response.json().get('msg', '')
                print_info(f"错误信息: {error_msg}")
                
                if "expired" in error_msg.lower():
                    print_success("错误信息正确显示token已过期")
                else:
                    print_info("错误信息未明确指出过期（可能是其他验证错误）")
            else:
                print_error(f"过期token未被正确拒绝，状态码: {response.status_code}")
                
        except ImportError:
            print_info("无法创建过期token（需要安装PyJWT库）")
            print_info("跳过过期token测试")
        except Exception as e:
            print_error(f"创建过期token时发生错误: {e}")
        
        # 步骤6: 测试无效签名
        print_step(6, "测试错误签名的token")
        try:
            import jwt as pyjwt
            
            # 使用错误的密钥签名
            wrong_payload = {
                "id": user_id,
                "username": username,
                "iat": int(time.time()),
                "exp": int(time.time()) + 3600
            }
            
            wrong_token = pyjwt.encode(wrong_payload, "wrong secret key", algorithm="HS256")
            
            headers = {"Authorization": f"Bearer {wrong_token}"}
            response = requests.get(f"{base_url}/user/{user_id}", headers=headers)
            
            if response.status_code == 401:
                print_success("错误签名token正确被拒绝")
                print_info(f"错误信息: {response.json().get('msg', '')}")
            else:
                print_error(f"错误签名token未被正确拒绝，状态码: {response.status_code}")
                
        except ImportError:
            print_info("跳过错误签名测试（需要PyJWT库）")
        except Exception as e:
            print_error(f"创建错误签名token时发生错误: {e}")
        
        # 步骤7: 清理测试用户
        print_step(7, "清理测试用户")
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.delete(f"{base_url}/user/{user_id}", headers=headers)
        if response.status_code == 200:
            print_success("测试用户清理成功")
        else:
            print_info("清理测试用户失败（可能需要手动清理）")
        
        print(f"\n{Fore.GREEN}{'=' * 70}")
        print(f"{Fore.GREEN}🎉 JWT过期时间详细测试完成！{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'=' * 70}")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print_error(f"网络请求错误: {e}")
        return False
    except Exception as e:
        print_error(f"测试过程中发生异常: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_jwt_expiration_detailed()
    exit(0 if success else 1)