import ahocorasick
import demjson
from analyse import Analysor

from reverse_complementary import reverse_complementary

def process(f1,f2,seq,para):

    Param=demjson.decode(para)
    READ_LENGTH=Param['read_length']

    t1 = ahocorasick.Automaton()
    t2 = ahocorasick.Automaton()

    index1 = 0
    index2 = 0

    plate1 = {}
    plate2={}
    flag1 = {}
    flag2={}

    BIAS=60

    for l in f1.readlines():
        index1 += 1  # record the index of line to match the lines from two files
        l=l.replace('\n','')
        l = l[0:BIAS - 1]  #cut out the first BIAS long string to avoid error
        rcl=reverse_complementary(l)  #calculate the revers_complementary string of l
        l=l[0:BIAS-1]
        t1.add_word(l, (l, index1, 1,'o'))
        t2.add_word(rcl, (rcl, index1, 1,'r'))
        flag1[index1]=0
        flag2[index1]=0

    for m in f2.readlines():
        index2 += 1
        m=m.replace('\n','')
        m=m[0:BIAS-1]
        rcm=reverse_complementary(m)
        t1.add_word(rcm, (rcm, index2, 2,'r'))
        t2.add_word(m,( m,index2,2,'o'))


    t1.make_automaton()
    t2.make_automaton()


    Titer1 = t1.iter(seq)
    Titer2 = t2.iter(seq)

    RECORDS_NUM_OF_TRIE1 = 0
    RECORDS_NUM_OF_TRIE2 = 0
    MATCH_COUNT_IN_TRIE1=0
    MATCH_COUNT_IN_TRIE2=0


    for pos,value in Titer1:
        #print(pos,value)
        RECORDS_NUM_OF_TRIE1+=1
        if plate1.has_key(value[1]):
            flag1[value[1]] += 1
            MATCH_COUNT_IN_TRIE1+=1
            #print(plate[value[1]])
            plate1[value[1]][value[2]]=value[0]
            plate1[value[1]][str(value[2])+'pos']=pos+READ_LENGTH-BIAS
            plate1[value[1]][str(value[2])+'state']=value[3]
            #print(plate[value[1]])
        else:
            flag1[value[1]]+=1
            plate1[value[1]]={value[2]:value[0],str(value[2])+'pos':pos+READ_LENGTH-BIAS,str(value[2])+'state':value[3]}
        #print(pos,value)

    for pos,value in Titer2:
        RECORDS_NUM_OF_TRIE2+=1
        #print(pos,value)
        if plate2.has_key(value[1]):
            flag2[value[1]] += 1
            MATCH_COUNT_IN_TRIE2+=1
            #print(plate[value[1]])
            plate2[value[1]][value[2]]=value[0]
            plate2[value[1]][str(value[2])+'pos']=pos+READ_LENGTH-BIAS
            plate2[value[1]][str(value[2]) + 'state'] = value[3]
            #print(plate[value[1]])
        else:
            flag2[value[1]] += 1
            plate2[value[1]]={value[2]:value[0],str(value[2])+'pos':pos+READ_LENGTH-BIAS,str(value[2])+'state':value[3]}

    #print(index1, index2)

    PLATE={}

    for key,value in plate1.iteritems():
        if value.has_key('1pos') and value.has_key('2pos'):
            if PLATE.has_key(key):
                print("Conflict!")
            else:
                PLATE[key]=value
                PLATE[key]['dis']=abs(value['1pos']-value['2pos'])-READ_LENGTH
            # print(value[1],value['1pos'],value[2],value['2pos'])

    for key, value in plate2.iteritems():
        if value.has_key('1pos') and value.has_key('2pos'):
            if PLATE.has_key(key):
                print("Conflict!")
            else:
                PLATE[key] = value
                PLATE[key]['dis'] = abs(value['1pos'] - value['2pos'])-READ_LENGTH
            # print(value[1], value['1pos'], value[2], value['2pos'])

    # for each in PLATE:
    #     print(each,PLATE[each])

    Ana=Analysor(para,seq,PLATE)
    Ana.calcDistance(False)
    Ana.analyse()