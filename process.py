import ahocorasick
import demjson
from analyse import Analysor
from graph import Graph
from reverse_complementary import reverse_complementary

def process(f1,f2,seq,para):

    Param=demjson.decode(para)
    READ_LENGTH=Param['read_length']


    t0 = ahocorasick.Automaton()
    t1 = ahocorasick.Automaton()
    t2 = ahocorasick.Automaton()
    t3 = ahocorasick.Automaton()

    index1 = 0
    index2 = 0

    plate0 = {}
    plate1 = {}
    plate2 = {}
    plate3 = {}

    flag0 = {}
    flag1 = {}
    flag2 = {}
    flag3 = {}

    BIAS=50

    for line in f1.readlines():
        index1 += 1  # record the index of line to match the lines from two files
        line=line.replace('\n','')
        l = line[0:BIAS - 1]  #cut out the first BIAS long string to avoid error
        rcline=reverse_complementary(line)  #calculate the revers_complementary string of l
        rcl=rcline[-(BIAS-1):READ_LENGTH-1]

        t0.add_word(l, (l, index1, 1,'o'))
        t1.add_word(l, (l, index1, 1,'o'))
        t2.add_word(rcl, (rcl, index1, 1,'r'))
        t3.add_word(rcl, (rcl, index1, 1,'r'))

        flag0[index1]=0
        flag1[index1]=0
        flag2[index1]=0
        flag3[index1]=0


    for line in f2.readlines():
        index2 += 1
        line=line.replace('\n','')
        m=line[0:BIAS-1]
        rcline=reverse_complementary(line)
        rcm=rcline[-(BIAS-1):READ_LENGTH]
        t0.add_word(m,( m,index2,2,'o'))
        t1.add_word(rcm, (rcm, index2, 2,'r'))
        t2.add_word(m,( m,index2,2,'o'))
        t3.add_word(rcm, (rcm, index2, 2,'r'))

    t0.make_automaton()
    t1.make_automaton()
    t2.make_automaton()
    t3.make_automaton()

    Titer0 = t0.iter(seq)
    Titer1 = t1.iter(seq)
    Titer2 = t2.iter(seq)
    Titer3 = t3.iter(seq)

    RECORDS_NUM_OF_TRIE0 = 0
    RECORDS_NUM_OF_TRIE1 = 0
    RECORDS_NUM_OF_TRIE2 = 0
    RECORDS_NUM_OF_TRIE3 = 0

    MATCH_COUNT_IN_TRIE0 = 0
    MATCH_COUNT_IN_TRIE1 = 0
    MATCH_COUNT_IN_TRIE2 = 0
    MATCH_COUNT_IN_TRIE3 = 0


    for pos,value in Titer0:
        #print(pos,value)
        RECORDS_NUM_OF_TRIE1+=1
        if plate0.has_key(value[1]):
            flag0[value[1]] += 1
            MATCH_COUNT_IN_TRIE0+=1
            # print(plate0[value[1]],value)
            # print(plate0[value[1]])
            if plate0[value[1]].has_key(value[2]):
                print('there exists a third item!')
                print(plate0[value[1]],value)
            else:
                plate0[value[1]][value[2]]=value[0]
                plate0[value[1]][str(value[2])+'pos']=pos
                plate0[value[1]][str(value[2])+'state']=value[3]
                #print(plate[value[1]])
        else:
            flag0[value[1]]+=1
            plate0[value[1]]={value[2]:value[0],str(value[2])+'pos':pos,str(value[2])+'state':value[3]}
        #print(pos,value)


    for pos,value in Titer1:
        #print(pos,value)
        RECORDS_NUM_OF_TRIE1+=1
        if plate1.has_key(value[1]):
            flag1[value[1]] += 1
            MATCH_COUNT_IN_TRIE1+=1
            # print(plate1[value[1]],value)
            # print(plate1[value[1]])
            if plate1[value[1]].has_key(value[2]):
                print('there exists a third item!')
                print(plate1[value[1]],value)
            else:
                plate1[value[1]][value[2]]=value[0]
                plate1[value[1]][str(value[2])+'pos']=pos
                plate1[value[1]][str(value[2])+'state']=value[3]
                #print(plate[value[1]])
        else:
            flag1[value[1]]+=1
            plate1[value[1]]={value[2]:value[0],str(value[2])+'pos':pos,str(value[2])+'state':value[3]}
        #print(pos,value)

    for pos,value in Titer2:
        RECORDS_NUM_OF_TRIE2+=1
        #print(pos,value)
        if plate2.has_key(value[1]):
            flag2[value[1]] += 1
            MATCH_COUNT_IN_TRIE2+=1
            # print(plate2[value[1]],value)
            # print(plate2[value[1]])
            if plate2[value[1]].has_key(value[2]):
                print('there exists a third item!')
                print(plate2[value[1]], value)
            else:
                plate2[value[1]][value[2]]=value[0]
                plate2[value[1]][str(value[2])+'pos']=pos
                plate2[value[1]][str(value[2]) + 'state'] = value[3]
                #print(plate[value[1]])
        else:
            flag2[value[1]] += 1
            plate2[value[1]]={value[2]:value[0],str(value[2])+'pos':pos,str(value[2])+'state':value[3]}

        for pos, value in Titer3:
            RECORDS_NUM_OF_TRIE3 += 1
            # print(pos,value)
            if plate3.has_key(value[1]):
                flag3[value[1]] += 1
                MATCH_COUNT_IN_TRIE2 += 1
                # print(plate2[value[1]],value)
                # print(plate2[value[1]])
                if plate3[value[1]].has_key(value[2]):
                    print('there exists a third item!')
                    # print(plate3[value[1]], value)
                else:
                    plate3[value[1]][value[2]] = value[0]
                    plate3[value[1]][str(value[2]) + 'pos'] = pos
                    plate3[value[1]][str(value[2]) + 'state'] = value[3]
                    # print(plate[value[1]])
            else:
                flag3[value[1]] += 1
                plate3[value[1]] = {value[2]: value[0], str(value[2]) + 'pos': pos, str(value[2]) + 'state': value[3]}

    #print(index1, index2)

    PLATE={}
    INV_PLATE={}

    for key,value in plate0.iteritems():
        if value.has_key('1pos') and value.has_key('2pos'):
            if INV_PLATE.has_key(key):
                print("Conflict!")
            else:
                INV_PLATE[key]=value
                INV_PLATE[key]['dis']=value['1pos']-value['2pos']-2*BIAS
            # print(value[1],value['1pos'],value[2],value['2pos'])

    for key,value in plate1.iteritems():
        if value.has_key('1pos') and value.has_key('2pos'):
            if PLATE.has_key(key):
                print("Conflict!")
            else:
                PLATE[key]=value
                PLATE[key]['dis']=value['1pos']-value['2pos']-2*BIAS
            # print(value[1],value['1pos'],value[2],value['2pos'])

    for key, value in plate2.iteritems():
        if value.has_key('1pos') and value.has_key('2pos'):
            if PLATE.has_key(key):
                print("Conflict!")
            else:
                PLATE[key] = value
                PLATE[key]['dis'] = value['2pos'] - value['1pos']-2*BIAS
            # print(value[1], value['1pos'], value[2], value['2pos'])

    for key, value in plate3.iteritems():
        if value.has_key('1pos') and value.has_key('2pos'):
            if INV_PLATE.has_key(key):
                print("Conflict!")
            else:
                INV_PLATE[key] = value
                INV_PLATE[key]['dis'] = value['2pos'] - value['1pos'] - 2 * BIAS
                # print(value[1], value['1pos'], value[2], value['2pos'])
    # for each in PLATE:
    #     print(each,PLATE[each])


    #
    # for each in INV_PLATE:
    #     print(INV_PLATE[each])

    Ana=Analysor(para,seq,PLATE,INV_PLATE)

    Ana.calcDistance(False)
    Ana.analyse()
    # for each in PLATE:
    #     print(PLATE[each])