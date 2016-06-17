import ahocorasick
import demjson
from reverse_complementary import reverse_complementary
from process import process

dir='./data/alpha/'

f1= open(dir+'1.txt')
f2= open(dir+'2.txt')
s= open(dir+'seq.txt')

seq=s.readline().replace('\n', '')
seq=seq

num_of_pairs=f1.__sizeof__()
len_of_seq=seq.__len__()

para=demjson.decode_file(dir+'./param.json',None)
para['num_of_pairs']=num_of_pairs
para['len_of_seq']=len_of_seq


# for value in para:
#     print(value,para[value])

process(f1, f2, seq,demjson.encode(para))


#
#
# T=ahocorasick.Automaton()
#
# index=0
# BIAS=76
#
# f1lines=f1.readlines()
# f2lines=f2.readlines()
#
# while(index<num_of_pairs):
#     l=f1lines[index][0:BIAS-1].replace('\n','')
#
#     m=f2lines[index][0:BIAS-1].replace('\n','')
#
#     T.add_word(l,(index,l,'ol'))
#     T.add_word(m,(index,m,'om'))
#     T.add_word(reverse_complementary(m),(index,reverse_complementary(m),'rm'))
#     T.add_word(reverse_complementary(l),(index,reverse_complementary(l),'rl'))
#
#     index+=1
#
# T.make_automaton()
#
# Titer=T.iter(seq)
# plate={}
#
# for key,value in Titer:
#     #print(key,value)
#     if plate.has_key(value[0]):
#         plate[value[0]][value[2]]=value[1]
#         plate[value[0]][str(value[2])+'pos']=key
#     else:
#         plate[value[0]]={value[2]:value[1],str(value[2])+'pos':key}
#
# dis={}
#
# for key,value in plate.items():
#     #print(key,value)
#     #plate[key]['dis']=abs(plate[key][1]-plate[key][3])
#     if value.has_key('olpos') and value.has_key('rmpos'):
#         dis[key]=abs(value['olpos']-value['rmpos'])-BIAS
#     elif value.has_key('rlpos') and value.has_key('ompos'):
#         dis[key] = abs(value['rlpos'] - value['ompos']) - BIAS
#
# sorted(dis,key= lambda value:value)
#
#
# print(max(dis.values()))
# print(min(dis.values()))
#
# for item in dis:
#     #print(item,dis[item])
#     if dis[item] <120:
#       print(plate[item])
