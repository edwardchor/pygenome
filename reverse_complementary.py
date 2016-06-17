def reverse_complementary(l=str):
    l=string_reverse(l)
    res=""
    for v in l:
        if v =='A':
            res+='T'
        elif v=='T':
            res+='A'
        elif v=='C':
            res+='G'
        elif v=='G':
            res+='C'
        else:
            res+=v
    return res

def string_reverse(string):
    return string[::-1]