import math
# 参考https://www.51cto.com/article/718337.html


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def evaluate(expression, valueOfX):
    ALLOWED_NAMES = {
        k: v for k, v in math.__dict__.items() if not k.startswith("__")
    }
    ALLOWED_NAMES['x'] = valueOfX
    """Evaluate a math expression."""
    # 编译表达式
    code = compile(expression, "<string>", "eval")

    # 验证允许名称
    for name in code.co_names:
        if name not in ALLOWED_NAMES:
            raise NameError(f"The use of '{name}' is not allowed")

    return eval(code, {"__builtins__": {}, 'x': valueOfX}, ALLOWED_NAMES)


def calculateFx(expression, valueOfX):
    __version__ = "1.0"

    """Main loop: Read and evaluate user's input."""
    # print(WELCOME)

    # 对表达式进行计算并处理错误
    try:
        result = evaluate(expression, valueOfX)
    except SyntaxError:
        # 如果用户输入了一个无效的表达式
        print("ERRcode -1: Invalid input expression syntax")
        return 'ERR-1       f(x)表达式语法错误'
    except (NameError, ValueError) as err:
        # 如果用户试图使用一个不允许的名字
        # 对于一个给定的数学函数来说是一个无效的值
        print('ERRcode -2:')
        print(err)
        return 'ERR-2       f(x)表达式语法错误'

    # 如果没有发生错误，则打印结果
    # print(f"The result is: {result}")
    return result









