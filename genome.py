import ahocorasick
import demjson
import sys

from graph import Graph
from reverse_complementary import reverse_complementary
from process import process

dir='./data/'+sys.argv[1]+'/'

s= open(dir+'seq.txt')


seq=s.readline().replace('\n', '')

len_of_seq=seq.__len__()

para=demjson.decode_file(dir+'./param.json',None)
para['len_of_seq']=len_of_seq
para['dir']=dir

with open(dir+'1.txt') as f1:
    with open(dir+'2.txt') as f2:
        process(f1, f2, seq,demjson.encode(para))

# connections = [(1, 'B'), (3, 'C'), (f1, 'D'),
#                ('2', 'D'), ('E', 'F'), ('F', 'C')]
# g=Graph(connections,False)
# print(g._graph)
#
#
# T=ahocorasick.Automaton()
#
# index=0
# BIAS=50
#
# f1lines=f1.readlines()
# f2lines=f2.readlines()
#
# while(index<f1lines.__len__()):
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
# #
# # for key,value in plate.items():
# #     #print(key,value)
# #     #plate[key]['dis']=abs(plate[key][1]-plate[key][3])
# #     if value.has_key('olpos') and value.has_key('rmpos'):
# #         dis[key]=abs(value['olpos']-value['rmpos'])-BIAS
# #         blankCount=min(value['rmpos'],value['olpos'])-BIAS
# #         s=''
# #         while(blankCount>-1):
# #             s+=' '
# #             blankCount-=1
# #         if min(value['rmpos'],value['olpos'])==value['rmpos']:
# #             s+=value['rm']
# #         else:
# #             s+=value['ol']
# #
# #         blankCount=0
# #         while(blankCount<max(value['rmpos'],value['olpos'])-BIAS):
# #             s+=' '
# #             blankCount+=1
# #         if max(value['rmpos'], value['olpos']) == value['rmpos']:
# #             s += value['rm']
# #         else:
# #             s += value['ol']
# #         print(s)
# #
# #     elif value.has_key('rlpos') and value.has_key('ompos'):
# #         dis[key] = abs(value['rlpos'] - value['ompos']) - BIAS
# #         blankCount = min(value['rlpos'], value['ompos']) - BIAS
# #         s = ''
# #         while (blankCount > -1):
# #             s += ' '
# #             blankCount -= 1
# #         if min(value['rlpos'], value['ompos']) == value['ompos']:
# #             s += value['rl']
# #         else:
# #             s += value['om']
# #
# #         blankCount = 0
# #         while (blankCount < max(value['rlpos'], value['ompos']) - BIAS):
# #             s += ' '
# #             blankCount += 1
# #         if max(value['rlpos'], value['ompos']) == value['rlpos']:
# #             s += value['rl']
# #         else:
# #             s += value['om']
# #         print(s)
# sorted(dis,key= lambda value:value)
#
# for item in dis:
#     #print(item,dis[item])
#     if dis[item] <120:
#       print(plate[item])
