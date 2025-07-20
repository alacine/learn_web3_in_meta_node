#!/usr/bin/env python3
"""
Python API测试运行器
提供友好的命令行界面来运行各种API测试
"""

import sys
import argparse
from colorama import Fore, Style, init

# 导入测试模块
from tests.test_user_api import UserAPITest
from tests.test_post_api import PostAPITest
from tests.test_comment_api import CommentAPITest
from tests.test_comprehensive import ComprehensiveAPITest

# 初始化colorama
init(autoreset=True)


def print_banner():
    """打印程序横幅"""
    banner = f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════════════════╗
║                    博客系统 API 测试工具                      ║
║                     Python 版本 v1.0                          ║
╚═══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}

{Fore.YELLOW}🚀 支持的测试模块:{Style.RESET_ALL}
  📝 用户API测试      - 注册、登录、CRUD操作
  📄 文章API测试      - 文章的完整生命周期管理  
  💬 评论API测试      - 评论系统功能验证
  🔄 综合测试        - 完整的用户交互场景模拟
  🗑️  删除测试        - 数据删除和清理操作

{Fore.GREEN}💡 使用前请确保:{Style.RESET_ALL}
  ✅ Go服务器正在运行 (go run main.go)
  ✅ MySQL数据库已启动 (docker-compose up -d)
  ✅ 已安装Python依赖 (uv sync)
"""
    print(banner)


def run_user_tests(auto_cleanup: bool = False):
    """运行用户API测试"""
    print(f"{Fore.CYAN}启动用户API测试...{Style.RESET_ALL}")
    test = UserAPITest(auto_cleanup=auto_cleanup)
    return test.run_test_suite()


def run_post_tests(auto_cleanup: bool = False):
    """运行文章API测试"""
    print(f"{Fore.CYAN}启动文章API测试...{Style.RESET_ALL}")
    test = PostAPITest(auto_cleanup=auto_cleanup)
    return test.run_test_suite()


def run_comment_tests(auto_cleanup: bool = False):
    """运行评论API测试"""
    print(f"{Fore.CYAN}启动评论API测试...{Style.RESET_ALL}")
    test = CommentAPITest(auto_cleanup=auto_cleanup)
    return test.run_test_suite()


def run_comprehensive_tests(auto_cleanup: bool = False):
    """运行综合测试"""
    print(f"{Fore.CYAN}启动综合测试...{Style.RESET_ALL}")
    test = ComprehensiveAPITest(auto_cleanup=auto_cleanup)
    return test.run_test_suite()


def run_cleanup_tests():
    """运行删除测试"""
    print(f"{Fore.RED}🗑️  启动删除测试...{Style.RESET_ALL}")
    
    cleanup_tests = [
        ("用户删除测试", lambda: UserAPITest().run_cleanup_tests()),
        ("文章删除测试", lambda: PostAPITest().run_cleanup_tests()),
        ("评论删除测试", lambda: CommentAPITest().run_cleanup_tests()),
        ("综合删除测试", lambda: ComprehensiveAPITest().run_cleanup_tests())
    ]
    
    results = []
    
    for test_name, test_func in cleanup_tests:
        print(f"\n{Fore.YELLOW}{'='*50}")
        print(f"开始执行: {test_name}")
        print(f"{'='*50}{Style.RESET_ALL}")
        
        try:
            success = test_func()
            results.append((test_name, success))
            
            if success:
                print(f"{Fore.GREEN}✅ {test_name} - 完成{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ {test_name} - 失败{Style.RESET_ALL}")
                
        except Exception as e:
            print(f"{Fore.RED}💥 {test_name} - 发生异常: {str(e)}{Style.RESET_ALL}")
            results.append((test_name, False))
    
    # 打印删除测试报告
    print(f"\n{Fore.CYAN}{'='*50}")
    print("🗑️  删除测试执行报告")
    print(f"{'='*50}{Style.RESET_ALL}")
    
    total_tests = len(results)
    passed_tests = sum(1 for _, success in results if success)
    
    for test_name, success in results:
        status_icon = "✅" if success else "❌"
        status_color = Fore.GREEN if success else Fore.RED
        print(f"  {status_icon} {status_color}{test_name}{Style.RESET_ALL}")
    
    print(f"\n📈 总计: {passed_tests}/{total_tests} 删除测试通过")
    
    if passed_tests == total_tests:
        print(f"{Fore.GREEN}🎉 所有删除测试执行完成！{Style.RESET_ALL}")
        return True
    else:
        print(f"{Fore.YELLOW}⚠️ 部分删除测试失败，请检查日志{Style.RESET_ALL}")
        return False


def run_all_tests(include_cleanup: bool = False):
    """运行所有测试"""
    print(f"{Fore.MAGENTA}🎯 运行完整测试套件...{Style.RESET_ALL}")
    
    if include_cleanup:
        print(f"{Fore.YELLOW}⚠️  注意：将自动清理测试数据{Style.RESET_ALL}")
    else:
        print(f"{Fore.BLUE}ℹ️  注意：测试数据不会自动清理，如需清理请单独运行删除测试{Style.RESET_ALL}")

    tests = [
        ("用户API测试", lambda: run_user_tests(auto_cleanup=include_cleanup)),
        ("文章API测试", lambda: run_post_tests(auto_cleanup=include_cleanup)),
        ("评论API测试", lambda: run_comment_tests(auto_cleanup=include_cleanup)),
        ("综合场景测试", lambda: run_comprehensive_tests(auto_cleanup=include_cleanup)),
    ]

    results = []

    for test_name, test_func in tests:
        print(f"\n{Fore.YELLOW}{'=' * 60}")
        print(f"开始执行: {test_name}")
        print(f"{'=' * 60}{Style.RESET_ALL}")

        try:
            success = test_func()
            results.append((test_name, success))

            if success:
                print(f"{Fore.GREEN}✅ {test_name} - 完成{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ {test_name} - 部分失败{Style.RESET_ALL}")

        except Exception as e:
            print(f"{Fore.RED}💥 {test_name} - 发生异常: {str(e)}{Style.RESET_ALL}")
            results.append((test_name, False))

    # 打印最终报告
    print(f"\n{Fore.CYAN}{'=' * 60}")
    print("📊 测试执行报告")
    print(f"{'=' * 60}{Style.RESET_ALL}")

    total_tests = len(results)
    passed_tests = sum(1 for _, success in results if success)

    for test_name, success in results:
        status_icon = "✅" if success else "❌"
        status_color = Fore.GREEN if success else Fore.RED
        print(f"  {status_icon} {status_color}{test_name}{Style.RESET_ALL}")

    print(f"\n📈 总计: {passed_tests}/{total_tests} 测试模块通过")

    if passed_tests == total_tests:
        print(f"{Fore.GREEN}🎉 所有测试模块执行完成！{Style.RESET_ALL}")
        if not include_cleanup:
            print(f"{Fore.BLUE}💡 提示：如需清理测试数据，请运行删除测试选项{Style.RESET_ALL}")
        return True
    else:
        print(f"{Fore.YELLOW}⚠️ 部分测试模块未完全通过，请检查日志{Style.RESET_ALL}")
        return False


def check_dependencies():
    """检查依赖"""
    try:
        import requests
        import colorama

        return True
    except ImportError as e:
        print(f"{Fore.RED}❌ 缺少依赖: {str(e)}")
        print(f"{Fore.YELLOW}请运行: uv sync{Style.RESET_ALL}")
        return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="博客系统API测试工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python run_tests.py                 # 显示菜单选择
  python run_tests.py --all           # 运行所有测试
  python run_tests.py --user          # 仅运行用户API测试
  python run_tests.py --post          # 仅运行文章API测试  
  python run_tests.py --comment       # 仅运行评论API测试
  python run_tests.py --comprehensive # 仅运行综合测试
  python run_tests.py --cleanup       # 仅运行删除测试
  python run_tests.py --all --auto-cleanup    # 运行所有测试并自动清理数据
  python run_tests.py --base-url http://localhost:8080/api/v1  # 自定义API地址
        """,
    )

    parser.add_argument("--all", action="store_true", help="运行所有测试")
    parser.add_argument("--user", action="store_true", help="运行用户API测试")
    parser.add_argument("--post", action="store_true", help="运行文章API测试")
    parser.add_argument("--comment", action="store_true", help="运行评论API测试")
    parser.add_argument("--comprehensive", action="store_true", help="运行综合测试")
    parser.add_argument("--cleanup", action="store_true", help="运行删除测试")
    parser.add_argument("--auto-cleanup", action="store_true", help="测试后自动清理数据（与其他测试选项一起使用）")
    parser.add_argument(
        "--base-url",
        default="http://localhost:8000/api/v1",
        help="API基础URL (默认: http://localhost:8000/api/v1)",
    )
    parser.add_argument("--no-banner", action="store_true", help="不显示横幅")

    args = parser.parse_args()

    # 检查依赖
    if not check_dependencies():
        sys.exit(1)

    # 显示横幅
    if not args.no_banner:
        print_banner()

    # 如果指定了命令行参数，直接执行对应测试
    if args.all:
        success = run_all_tests(include_cleanup=args.auto_cleanup)
        sys.exit(0 if success else 1)
    elif args.user:
        success = run_user_tests(auto_cleanup=args.auto_cleanup)
        sys.exit(0 if success else 1)
    elif args.post:
        success = run_post_tests(auto_cleanup=args.auto_cleanup)
        sys.exit(0 if success else 1)
    elif args.comment:
        success = run_comment_tests(auto_cleanup=args.auto_cleanup)
        sys.exit(0 if success else 1)
    elif args.comprehensive:
        success = run_comprehensive_tests(auto_cleanup=args.auto_cleanup)
        sys.exit(0 if success else 1)
    elif args.cleanup:
        success = run_cleanup_tests()
        sys.exit(0 if success else 1)

    # 否则显示交互式菜单
    while True:
        print(f"\n{Fore.CYAN}请选择要运行的测试:{Style.RESET_ALL}")
        print("  1. 👤 用户API测试")
        print("  2. 📄 文章API测试")
        print("  3. 💬 评论API测试")
        print("  4. 🔄 综合场景测试")
        print("  5. 🎯 运行所有测试")
        print("  6. 🗑️ 运行删除测试")
        print("  0. 🚪 退出")

        try:
            choice = input(
                f"\n{Fore.YELLOW}请输入选择 (0-6): {Style.RESET_ALL}"
            ).strip()

            if choice == "0":
                print(f"{Fore.GREEN}👋 再见！{Style.RESET_ALL}")
                break
            elif choice == "1":
                run_user_tests()
            elif choice == "2":
                run_post_tests()
            elif choice == "3":
                run_comment_tests()
            elif choice == "4":
                run_comprehensive_tests()
            elif choice == "5":
                run_all_tests()
            elif choice == "6":
                run_cleanup_tests()
            else:
                print(f"{Fore.RED}❌ 无效选择，请输入 0-6{Style.RESET_ALL}")

        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}👋 用户中断，再见！{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"{Fore.RED}❌ 发生错误: {str(e)}{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
