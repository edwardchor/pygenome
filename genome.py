import ahocorasick
import demjson
from reverse_complementary import reverse_complementary
from process import process


f1= open('./1.txt')
f2= open('./2.txt')
s= open('./seq.txt')
p= open('./param.json')

seq=s.readline().replace('\n', '')
seq=seq

num_of_pairs=f1.__sizeof__()
len_of_seq=seq.__len__()
para=demjson.decode_file('./param.json',None)
para['num_of_pairs']=num_of_pairs
para['len_of_seq']=len_of_seq


# for value in para:
#     print(value,para[value])

#process(f1, f2, seq,demjson.encode(para))


T=ahocorasick.Automaton()

index=93
BIAS=50

l=f1.readlines()[index][0:BIAS-1].replace('\n','')

m=f2.readlines()[index][0:BIAS-1].replace('\n','')

T.add_word(l,(index,l,'ol'))
T.add_word(m,(index,m,'om'))
T.add_word(reverse_complementary(m),(index,reverse_complementary(m),'rm'))
T.add_word(reverse_complementary(l),(index,reverse_complementary(l),'rl'))
T.make_automaton()

Titer=T.iter(seq)

for item in Titer:
    print(item)