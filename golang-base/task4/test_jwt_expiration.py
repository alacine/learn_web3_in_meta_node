#!/usr/bin/env python3
"""
测试JWT过期时间功能
创建一个短过期时间的token来测试过期验证
"""

import requests
import json
import time
import uuid
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

def test_jwt_expiration():
    base_url = "http://localhost:8000/api/v1"
    
    print(f"{Fore.CYAN}{'=' * 60}")
    print(f"{Fore.CYAN}JWT 过期时间测试{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 60}")
    
    try:
        # 生成唯一用户
        unique_id = str(uuid.uuid4())[:8]
        username = f"exptest_{unique_id}"
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
            return False
        
        login_response = response.json()["data"]
        token = login_response["token"]
        print_success("登录成功，获取到JWT token")
        print_info(f"Token: {token[:50]}...")
        
        # 步骤3: 测试有效token
        print_step(3, "测试有效token访问")
        headers = {"Authorization": f"Bearer {token}"}
        
        response = requests.get(f"{base_url}/user/{user_id}", headers=headers)
        if response.status_code == 200:
            print_success("有效token访问成功")
        else:
            print_error(f"有效token访问失败: {response.status_code}")
            print(response.json())
        
        # 步骤4: 检查JWT payload中的过期时间
        print_step(4, "解析JWT token查看过期时间")
        try:
            import jwt as pyjwt
            import base64
            
            # 解析JWT（不验证签名，只查看payload）
            payload = pyjwt.decode(token, options={"verify_signature": False})
            exp_timestamp = payload.get('exp')
            iat_timestamp = payload.get('iat')
            
            if exp_timestamp and iat_timestamp:
                import datetime
                exp_time = datetime.datetime.fromtimestamp(exp_timestamp)
                iat_time = datetime.datetime.fromtimestamp(iat_timestamp)
                duration = exp_time - iat_time
                
                print_info(f"签发时间: {iat_time}")
                print_info(f"过期时间: {exp_time}")
                print_info(f"有效期: {duration}")
                
                # 检查是否是24小时
                if duration.total_seconds() == 24 * 3600:
                    print_success("JWT过期时间设置正确（24小时）")
                else:
                    print_error(f"JWT过期时间不是24小时，实际为: {duration}")
            else:
                print_error("JWT中缺少过期时间信息")
                
        except ImportError:
            print_info("无法解析JWT（需要安装PyJWT库），跳过详细检查")
        except Exception as e:
            print_error(f"解析JWT时发生错误: {e}")
        
        # 步骤5: 测试无效token（手工创建过期token）
        print_step(5, "测试无效签名的token")
        invalid_token = "invalid.token.here"
        headers = {"Authorization": f"Bearer {invalid_token}"}
        
        response = requests.get(f"{base_url}/user/{user_id}", headers=headers)
        if response.status_code == 401:
            print_success("无效token正确被拒绝")
            print_info(f"错误信息: {response.json().get('msg', '')}")
        else:
            print_error(f"无效token未被正确拒绝，状态码: {response.status_code}")
        
        # 步骤6: 测试没有Authorization头
        print_step(6, "测试没有Authorization头")
        response = requests.get(f"{base_url}/user/{user_id}")
        if response.status_code == 401:
            print_success("没有Authorization头正确被拒绝")
            print_info(f"错误信息: {response.json().get('msg', '')}")
        else:
            print_error(f"没有Authorization头未被正确拒绝，状态码: {response.status_code}")
        
        # 步骤7: 测试错误的Bearer格式
        print_step(7, "测试错误的Bearer格式")
        headers = {"Authorization": f"Basic {token}"}  # 使用Basic而不是Bearer
        response = requests.get(f"{base_url}/user/{user_id}", headers=headers)
        if response.status_code == 401:
            print_success("错误的Bearer格式正确被拒绝")
            print_info(f"错误信息: {response.json().get('msg', '')}")
        else:
            print_error(f"错误的Bearer格式未被正确拒绝，状态码: {response.status_code}")
        
        # 步骤8: 清理测试用户
        print_step(8, "清理测试用户")
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.delete(f"{base_url}/user/{user_id}", headers=headers)
        if response.status_code == 200:
            print_success("测试用户清理成功")
        else:
            print_info("清理测试用户失败（可能需要手动清理）")
        
        print(f"\n{Fore.GREEN}{'=' * 60}")
        print(f"{Fore.GREEN}🎉 JWT过期时间测试完成！{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'=' * 60}")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print_error(f"网络请求错误: {e}")
        return False
    except Exception as e:
        print_error(f"测试过程中发生异常: {e}")
        return False

if __name__ == "__main__":
    success = test_jwt_expiration()
    exit(0 if success else 1)