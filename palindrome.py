def palindrome(num):
    n1 = num
    n1_r = int(str(n1)[::-1])
    lis_nums = []
    steps = 0
    while n1 != n1_r:
        lis_nums.append((n1, n1_r, n1+n1_r))
        n1 = n1 + n1_r
        n1_r = int(str(n1)[::-1])
        
        steps += 1
        if steps == 300:
            break
    if len(lis_nums) == 0:
        lis_nums.append((n1, n1_r, n1+n1_r))
    
    result = ""
    for i in lis_nums:
        result += f"{i[0]} + {i[1]} = {i[2]} ->\n\t"
    
    #when not solved
    if steps >= 300:
        exc = "``` \n\.\.\. not solved"
        result = f"``` {result}"[0:2000] + "\.\.\."
        result += exc
        return {'text':result, 'solvable':False, 'reached_num':n1_r}
    #when solved
    else:
        exc = f" ``` \nthe answer is {n1_r}"
        result = f"``` {result}"[0:4096-len(exc)]
        result += exc
        return {'text':result, 'solvable':True, 'reached_num':n1_r}
