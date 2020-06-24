import inspect


def methods_with_decorator(controller_name, decorator_name: str) -> [(str, str)]:
    # raise Warning("\"_methods_with_decorator\" Method works with errors! do unit tests and rewrite it")
    source_lines = inspect.getsourcelines(controller_name)[0]
    result = []
    for i, line in enumerate(source_lines):
        line = line.strip()
        if line.split('(')[0].strip() == '@' + decorator_name:
            param = line.split('(')[1].split(')')[0]
            next_line = source_lines[i + 1]
            while '@' in next_line:
                i += 1
                next_line = source_lines[i + 1]
            decor_name = next_line.split('def')[1].split('(')[0].strip()
            item = (decor_name, param)
            result.append(item)
    return result