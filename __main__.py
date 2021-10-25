import ast
import re
import json

# 나중에 dfs로 변경
def is_recursive(ast_tree):
    """ Returns
    Args:
        tree (ast.Module): ast tree

    Returns:
        bool: return recursive or not
    """
    for child in ast.iter_child_nodes(ast_tree):
        if isinstance(child, ast.FunctionDef):
            function_name = child.name # function name
            for c in ast.iter_child_nodes(child):
                if ('Call(func=Name(id=\'' + function_name) in ast.dump(c):
                    return True
    return False

# binary search를 사용하는지 확인
# import한 라이브러리를 알 수 있음
# 수정 => body 안에서 타고 내려갈 수 있도록
def get_libraries(ast_tree):
    """ Returns
    Args:
        tree (ast.Module): ast tree

    Returns:
        list
    """
    dump_ast_tree = ast.dump(ast_tree, indent=0).split()
    # code = code.split()
    libraries = []
    import_pattern = re.compile('name=[a-z\']+')
    import_from_pattern = re.compile('module=[a-z\']+')

    for i in range(len(dump_ast_tree)):
        if dump_ast_tree[i][:-1] == 'Import':
            libraries.append(import_pattern.search(dump_ast_tree[i+2]).group()[6:-1])
        elif dump_ast_tree[i][:-1] == 'ImportFrom':
            libraries.append(import_pattern.search(dump_ast_tree[i+3]).group()[6:-1] + ' from ' + import_from_pattern.search(dump_ast_tree[i+1]).group()[8:-1])

    return libraries

# list, dictionary, set, deque
# queue 1. Collection 모듈의 deque, 2. queue 모듈의 Queue
# flattening한 ast_tree필요 -> ast.dump(ast_tree)
# return : dictionary로 변환 -> json형태를 위해
def get_data_structure_list(ast_tree):
    """ Returns
    Args:
        tree (ast.Module): ast tree

    Returns:
        list
    """
    return_list = []

    t = ast.dump(ast_tree)

    # count set
    if 'Call(func=Name(id=\'set\'' in t:
        return_list.append(('set', t.count('Call(func=Name(id=\'set\'')))
    
    # count deque
    if 'value=Call(func=Name(id=\'deque\'' in t:
        return_list.append(('deque', t.count('value=Call(func=Name(id=\'deque\'')))
    
    # count list
    value = 0
    value += t.count('Call(func=Name(id=\'list\'')
    value += t.count('value=List')

    if value:
        return_list.append(('list', value))
    
    value = 0
    value += t.count('value=Dict')
    value += t.count('Call(func=Name(id=\'dict\'')

    if value:
        return_list.append(('dictionary', value))    


    return return_list

def get_data_structure(ast_tree):
    """ Returns
    Args:
        tree (ast.Module): ast tree

    Returns:
        dict
    """
    ret = {}

    t = ast.dump(ast_tree)

    # count set
    if 'Call(func=Name(id=\'set\'' in t:
        ret['set'] = t.count('Call(func=Name(id=\'set\'')
    
    # count deque
    if 'value=Call(func=Name(id=\'deque\'' in t:
        ret['set'] = t.count('Call(func=Name(id=\'deque\'')
    
    # count list
    value = 0
    value += t.count('Call(func=Name(id=\'list\'')
    value += t.count('value=List')

    if value:
        ret['list'] = value
    
    value = 0
    value += t.count('value=Dict')
    value += t.count('Call(func=Name(id=\'dict\'')

    if value:
        ret['dictionary'] = value


    return ret

# binary search를 사용하고 있는지 검사
# ast.dump(ast_tree)
def is_bisect(ast_tree):
    """ Returns
    Args:
        tree (ast.Module): ast tree

    Returns:
        bool: return whether binary searching is used or not
    """
    dump_ast_tree = ast.dump(ast_tree)
    if 'Call(func=Name(id=\'bisect_left\'' in dump_ast_tree or 'Call(func=Name(id=\'bisect_right\'' in dump_ast_tree:
        return True
    return False

def get_func(ast_tree):
    """ Returns
    Args:
        tree (ast.Module): ast tree

    Returns:
        list
    """
    # print(ast.dump(ast_tree))
    def_pattern = re.compile(r'FunctionDef\(name=\'[A-Za-z0-9\_]+\'')
    find_defs = def_pattern.findall(ast.dump(ast_tree))
    defs = []
    
    for f in find_defs:
        defs.append(f.split('\'')[1])

    call_pattern1 = re.compile(r'Call\(func=Name\(id=\'[A-Za-z0-9\_]+\'')
    call_pattern2 = re.compile(r'Call\(func=Attribute\(value=Name\(id=\'[A-Za-z0-9\_]+\'\, ctx=Load\(\)\)\, attr=\'[A-Za-z0-9\_]+\'')

    
    find_calls = call_pattern1.findall(ast.dump(ast_tree))
    calls=[]
    for f in find_calls:
        cname = f.split('\'')[1]
        if cname not in defs:
            calls.append(cname)
    
    

    find_calls = call_pattern2.findall(ast.dump(ast_tree))
    for f in find_calls:
        cname = f.split('\'')[-2]
        if cname not in defs:
            calls.append(cname)

    return calls

def return_json(code):
    """ Returns
    Args:
        string: python code

    Returns:
        dict
    """

    lines = code.split("\\r\\n")
    code = ""
    for line in lines:
        code += (line + "\r\n")
    
    ret = {}


    ast_tree = ast.parse(code)

    ret['library'] = get_libraries(ast_tree)
    ret['recursion'] = is_recursive(ast_tree)
    ret['data_structure'] = get_data_structure(ast_tree)
    ret['binary search'] = is_bisect(ast_tree)
    ret['function'] = get_func(ast_tree)

    print(ret)
    return json.dumps(ret)
    

def main(code):
    ast_tree = ast.parse(code)
    print(ast.dump(ast_tree, indent=4))

    print("<library>")
    print(get_libraries(ast_tree))
    
    print("<recursion>")
    print(is_recursive(ast_tree))

    print("<data structure>")
    print(get_data_structure(ast_tree))

    print("<binary search>")
    print(is_bisect(ast_tree))

    print('<functions>')
    print(get_func(ast_tree))

# binary search
# 중첩 for문
if __name__ == "__main__":
    f = open("test/test.py", 'r')
    try:
        return_json(f.read())
        # main(f.read())
    finally:
        f.close()
