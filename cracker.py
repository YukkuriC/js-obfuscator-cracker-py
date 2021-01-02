r'''
解码js obfuscator加密文件
使用全局参数配置相关信息

# 固定参数
INPUT_JS: 输入待替换文件（第一行起始包含base64关键字表；第二行为实际加密内容）
OUTPUT_JS: 输出初步解密文件，请配合格式化工具使用

# 可选覆盖参数
KW_LIST: 关键字查询表，若不指定则尝试由源码获取
OFFSET：关键字表滚转次数，若不指定则尝试由源码获取
GETTER: getter函数名称，若不指定则尝试由源码获取
'''

import base64 as b64, collections as c
import os, re

### 参数
# INPUT_JS = '_(:з」∠)_'
OUTPUT_JS = './output.js'

### 常用正则
Q = lambda s: f'''['"]{s}['"]'''
A = lambda s: r'\[' + s + r'\]'
_ATTR = A(Q('(\w+)'))
_HEX = r'0x[\da-fA-F]+'


def main():
    # 读取原文件
    input_js = globals().get('INPUT_JS')
    if not (input_js and os.path.isfile(INPUT_JS)):
        print('Invalid INPUT_JS param!')
        exit(1)
    with open(INPUT_JS, encoding='utf-8') as f:
        mapper, data = f.read().strip().split('\n', 1)

    # 获取关键字表+滚转
    keywords = globals().get('KW_LIST')
    if not keywords:
        match = re.search(r'\[.+?\]', mapper)
        keywords = eval(match.group())
        keywords = [*map(lambda x: b64.b64decode(x).decode('utf-8'), keywords)]

    # 获取滚转次数
    offset = globals().get('OFFSET')
    if not offset:
        lst_name = re.match(r'var (\w+)=',
                            mapper).groups()[0]  # var _0x254e=[...];
        offset = re.search(rf'\({lst_name},(0x\w+)\)',
                           mapper).groups()[0]  # (_0x254e,0xc0)
        offset = eval(offset)

    # 获取mapper函数
    getter = globals().get('GETTER')
    if not getter:
        tmp = c.Counter(re.findall(rf'''(_{_HEX})\({Q(_HEX)}\)''', data))
        getter = tmp.most_common(1)[0][0]

    # 滚转表
    keywords = c.deque(keywords)
    for i in range(offset):
        keywords.append(keywords.popleft())
    keywords = list(keywords)

    # 替换文本
    def replacer(match):
        val = eval(match.groups()[0])
        return repr(keywords[val])

    data = re.sub(
        rf"""{getter}\('(0x\w+)'\)""",
        replacer,
        data,
    )  # _0x4392('0x13')

    # 替换下标访问简化
    for kw in 'get', 'static':
        data = re.sub(rf"{kw}\s*{_ATTR}", rf'{kw} \1',
                      data)  # get ['param'](args) -> get param(args)
    while 1:  # obj['param'] -> obj.param
        new_data = re.sub(rf"(?<=[\w\]\)]){_ATTR}", r'.\1', data)
        if new_data == data:
            break
        data = new_data

    # 换行
    data = data.replace(r'(?<=;)(?!\s)', '\n')
    data = re.sub(r'(?<=\})(?=[\w\{\[])', '\n', data)

    # 下标访问简化v2
    data = re.sub(rf"^{_ATTR}", r'\1', data,
                  flags=re.M)  # ['param'](args) -> param(args)

    # 替换复杂表示
    data = data.replace('!![]', 'true').replace('![]', 'false')
    data = re.sub(rf'(?<![\w_])({_HEX})', lambda m: str(eval(m.groups()[0])),
                  data)

    # 输出代码
    with open(OUTPUT_JS, 'w', encoding='utf-8') as f:
        print('// auto-gen by cracker.py', file=f)
        print(data, file=f)


if __name__ == '__main__':
    import os, sys
    args = sys.argv
    if len(args) <= 1:
        print('Usage: python cracker.py INPUT_JS [OUTPUT_JS="./output.js"]',
              file=sys.stderr)
        exit(1)
    INPUT_JS = args[1]
    if len(args) > 2:
        OUTPUT_JS = args[2]
    main()
