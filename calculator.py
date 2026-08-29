"""
Python智能计算器 - 支持连续计算的强大工具
================================================
功能特性:
1. 基础四则运算 (+, -, *, /)
2. 连续计算模式 (基于上次结果继续计算)
3. 计算历史记录 (最多保存10条)
4. 友好的交互界面
"""

import os

# ==================== 全局变量 ====================
history = []  # 历史记录列表
MAX_HISTORY = 10  # 最大历史记录数


# ==================== 辅助函数 ====================

def print_separator(char="=", length=50):
    """打印分隔线"""
    print(char * length)


def clear_screen():
    """清屏功能"""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_valid_number(prompt="请输入数字: "):
    """
    获取有效的数字输入
    使用try/except处理非法输入
    """
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("错误: 请输入有效的数字!")


def get_valid_operator(prompt="请输入运算符 (+, -, *, /): "):
    """
    获取有效的运算符
    必须是 +, -, *, / 之一
    """
    valid_operators = ['+', '-', '*', '/']
    while True:
        operator = input(prompt).strip()
        if operator in valid_operators:
            return operator
        print(f"错误: 运算符必须是以下之一: {', '.join(valid_operators)}")


# ==================== 核心计算功能 ====================

def calculate(num1, operator, num2):
    """
    执行计算并返回结果
    包含除零保护
    """
    if operator == '+':
        result = num1 + num2
    elif operator == '-':
        result = num1 - num2
    elif operator == '*':
        result = num1 * num2
    elif operator == '/':
        if num2 == 0:
            raise ZeroDivisionError("除数不能为零!")
        result = num1 / num2
    
    # 格式化表达式字符串
    expression = f"{num1} {operator} {num2}"
    result_str = f"{result}"
    
    # 如果结果是整数,去掉小数部分
    if result == int(result):
        result = int(result)
        result_str = str(result)
    
    full_expression = f"{expression} = {result_str}"
    return result, full_expression


def add_to_history(expression):
    """添加计算历史记录(最多保留10条)"""
    history.append(expression)
    # 如果超过最大记录数,删除最早的记录
    if len(history) > MAX_HISTORY:
        history.pop(0)


# ==================== 主菜单功能 ====================

def show_welcome():
    """显示欢迎界面"""
    clear_screen()
    print_separator("=")
    print("     欢迎使用 Python 智能计算器!")
    print_separator("=")
    print()
    print("  支持连续计算,让数学运算更简单!")
    print()


def show_menu():
    """显示主菜单"""
    print_separator("-")
    print("         主菜单")
    print_separator("-")
    print("  1. 开始计算")
    print("  2. 查看历史")
    print("  3. 退出程序")
    print_separator("-")


def show_history():
    """显示计算历史记录"""
    print_separator("*")
    print("         计算历史")
    print_separator("*")
    
    if not history:
        print("  暂无历史记录")
    else:
        # 使用for循环打印历史记录,带序号
        print(f"  共 {len(history)} 条记录:")
        print()
        for index, record in enumerate(history, start=1):
            print(f"  {index}. {record}")
    
    print_separator("*")


# ==================== 单次计算功能 ====================

def single_calculation():
    """
    单次计算功能
    用户输入: 数字1 运算符 数字2
    返回: 计算结果和格式化的表达式字符串
    """
    print()
    print_separator("-")
    print("  单次计算模式")
    print_separator("-")
    
    num1 = get_valid_number("请输入第一个数字: ")
    operator = get_valid_operator()
    num2 = get_valid_number("请输入第二个数字: ")
    
    try:
        result, expression = calculate(num1, operator, num2)
        print()
        print(f"  计算结果: {expression}")
        add_to_history(expression)
        return result
    except ZeroDivisionError as e:
        print(f"\n  错误: {e}")
        return None


# ==================== 连续计算功能 ====================

def continuous_calculation():
    """
    连续计算功能
    
    逻辑说明:
    1. 第一次计算: 用户输入 数字1 运算符 数字2
    2. 得到结果后,显示选项菜单
    3. 如果选择继续,用户只需输入运算符和新数字
       程序自动使用上次结果作为第一个数
    4. 循环直到用户选择返回主菜单
    
    这种设计让连续计算变得直观高效,
    特别适合连续加减的应用场景
    """
    print()
    print_separator("-")
    print("  连续计算模式")
    print_separator("-")
    print("  输入格式: 数字1 运算符 数字2")
    print("  例如: 10 + 5  或  3 * 4")
    print()
    
    # 第一次计算:获取完整输入
    num1 = get_valid_number("请输入第一个数字: ")
    operator = get_valid_operator()
    num2 = get_valid_number("请输入第二个数字: ")
    
    # 执行第一次计算
    try:
        result, expression = calculate(num1, operator, num2)
        print()
        print(f"  {expression}")
        add_to_history(expression)
    except ZeroDivisionError as e:
        print(f"\n  错误: {e}")
        return
    
    # 连续计算循环
    while True:
        print()
        print_separator("=")
        print("  请选择下一步操作:")
        print("  1. 继续基于结果计算")
        print("  2. 重新开始")
        print("  3. 返回主菜单")
        print_separator("=")
        
        choice = input("  请输入选择 (1/2/3): ").strip()
        
        if choice == '1':
            # 继续基于结果计算
            print()
            print(f"  当前结果: {result}")
            
            # 只获取运算符和新数字(使用上次result作为第一个数)
            operator = get_valid_operator("请输入运算符: ")
            num2 = get_valid_number("请输入第二个数字: ")
            
            # 执行计算
            try:
                result, expression = calculate(result, operator, num2)
                print()
                print(f"  {expression}")
                add_to_history(expression)
            except ZeroDivisionError as e:
                print(f"\n  错误: {e}")
                continue
            
        elif choice == '2':
            # 重新开始 - 重新输入完整表达式
            print()
            print("  重新开始计算...")
            num1 = get_valid_number("请输入第一个数字: ")
            operator = get_valid_operator()
            num2 = get_valid_number("请输入第二个数字: ")
            
            try:
                result, expression = calculate(num1, operator, num2)
                print()
                print(f"  {expression}")
                add_to_history(expression)
            except ZeroDivisionError as e:
                print(f"\n  错误: {e}")
                continue
                
        elif choice == '3':
            # 返回主菜单
            print()
            print("  返回主菜单...")
            break
            
        else:
            print("\n  无效选择,请输入 1, 2 或 3")


# ==================== 主程序入口 ====================

def main():
    """主程序 - 使用while循环保持运行"""
    
    show_welcome()
    
    while True:
        show_menu()
        
        choice = input("\n  请输入您的选择 (1/2/3): ").strip()
        
        if choice == '1':
            # 开始计算 - 直接进入连续计算模式
            continuous_calculation()
            
        elif choice == '2':
            # 查看历史
            show_history()
            input("\n  按回车键继续...")
            
        elif choice == '3':
            # 退出程序
            print()
            print_separator("=")
            print("  感谢使用 Python 智能计算器!")
            print("  再见!")
            print_separator("=")
            break
            
        else:
            print("\n  无效选择,请输入 1, 2 或 3")


# ==================== 程序入口 ====================

if __name__ == "__main__":
    main()
# 作者：@Minos-star
