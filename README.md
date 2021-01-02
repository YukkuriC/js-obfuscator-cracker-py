# JS Obfuscator破解器
解码来源于[`javascript-obfuscator`](https://github.com/javascript-obfuscator/javascript-obfuscator)的加密文件  
使用到了f-string语法，故需要`Python3.6`以上版本  
使用全局参数配置相关信息

## 参数
### 固定参数
* INPUT_JS: 输入待替换文件（第一行起始包含base64关键字表）

### 可选参数
* OUTPUT_JS: 输出初步解密文件（默认为`./output.js`）

### 可选覆盖参数（默认直接从源文件解析，可覆盖）
* KW_LIST: 关键字查询表
* OFFSET：关键字表滚转次数
* GETTER: getter函数名称

# JS Obfuscator Cracker in Python3
Python3 auto cracker for [`javascript-obfuscator`](https://github.com/javascript-obfuscator/javascript-obfuscator) generated files  
`Python3.6` or above is needed for the usage of f-string  
Parameters are passed via `globals()` scope.

## Fixed parameter:
* INPUT_JS: input obfuscated JS file location (beginning of the first line contains the Base64-encoded keyword list)

## Optional parameter:
* OUTPUT_JS: cracked JS file location (default: `./output.js`)

## Optional override parameters:
* KW_LIST: list of keyword mappings
* OFFSET：times the keyword list is rolled
* GETTER: name of the getter function
