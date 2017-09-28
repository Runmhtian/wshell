# coding=utf-8
# eval 函数可实现，这里选择将中缀表达式转为后缀表达式

operator={
    '(':0,
    ')':0,
    '*':2,
    '/':2,
    '+':1,
    '-':1
}


def cal(command):
    command = command.strip('cal').strip()

    cal_list=postfix_convert(command)
    stack=[]
    while len(cal_list)!=0:
        char= cal_list.pop()
        if char in operator:
            b,a=stack.pop(),stack.pop()
            stack.append(cal_help(int(a),int(b),char))
        else:
            stack.append(char)
        # print stack
    return stack[0]


def cal_help(a,b,op):
    if op=='+':
        return a+b
    elif op=='-':
        return a-b
    elif op=='/':
        return a/b
    elif op=='*':
        return a*b
    else:
        return None


def postfix_convert(cal_str):
    s=[]   # 运算符
    l=[]    # 中间结果
    cal_str_list=[]
    char=''
    for i in cal_str:
        if i not in operator.keys():
            char += i
        else:
            cal_str_list.append(char)
            char = ''
            cal_str_list.append(i)
    cal_str_list.append(char)
    # print(cal_str_list)
    for char in cal_str_list:
        if char not in operator.keys():
            l.append(char)
        else:
            if len(s)==0:
                s.append(char)
            else:
                if char=='(':
                    s.append(char)
                elif char==')':
                    while s[-1]!='(':
                        l.append(s.pop())
                    s.pop()
                else:
                    while len(s)!=0:
                        if s[-1]=='(' or operator[char]>operator[s[-1]]:
                            break
                        l.append(s.pop())
                    s.append(char)
    while len(s)!=0:
        l.append(s.pop())
    l.reverse()
    return l


if __name__ == '__main__':
    s='120+145'
    # print(postfix_convert(s))
    print(cal(s))
