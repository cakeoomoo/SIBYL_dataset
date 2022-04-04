 # -*- coding: utf-8 -*-

from idautils import *
from idaapi import *
from idc import *
import re
import pickle
import time

print_flag = False # True

outputdir = '/home/output'
filename_opt = 'gccO3'

'''
    does not make sense and do not use this fucntion in this file
'''
def check_vul_function():
    danger_funcs = ["strcpy","sprintf","strncpy"]

    for func in danger_funcs:
        addr = LocByName( func )
        if addr != BADADDR:
            cross_refs = CodeRefsTo( addr, 0 )
            print("Cross References to {}" .format(func))
            print("-------------------------------")
            for ref in cross_refs:
                print("{}" .format(hex(ref)))


'''
    print md5 hash and return strings of hash
'''
def get_hash_info():
    md5_str = GetInputFileMD5()
    if print_flag:
        print("MD5: {}" .format(md5_str))
    return md5_str


'''
    return all segmetns information
'''
def get_segments_info():
    list_allsegments = []
    for ea in Segments():
        list_allsegments.append([SegStart(ea), SegEnd(ea)])
    if print_flag:
        print("All segments addr: {}" .format(list_allsegments))
    return list_allsegments


'''
    return .text segments information
'''
def print_text_segments_info():
    segment_name = ".text"
    text_seg_addr_start = SegByName(segment_name)
    text_seg_addr_end = SegEnd(text_seg_addr_start)
    if print_flag:
        print("text_seg_addr_start:{:02x}　text_seg_addr_end:{:02x}" \
            .format(text_seg_addr_start, text_seg_addr_end))
    function_list = Functions(text_seg_addr_start, text_seg_addr_end)
    if print_flag:
        print(function_list)
        for f in function_list:
            print(hex(f))


'''
    does not make sense, or do not know following routine 
'''
def block_split(output_file, startEA, endEA):
    print("--block_split()")

    curName = GetFunctionName(startEA);
    dem = idc.Demangle(curName, idc.GetLongPrm(INF_SHORT_DN));
    if dem != None:
        curName = dem;
    
    first=startEA
    h = idautils.Heads(startEA, endEA)
    for i in h:
        mnem = idc.GetMnem(i)
        if mnem == "call" and i != endEA:
            first=idc.NextHead(i, endEA+1)

'''
----------------------------------------------------------------------------------

----------------------------------------------------------------------------------
'''
            
list_fileN = []
list_funcN = []
list_CFG = []
list_BB_Insts = []


'''
    get BB-ID, start-addrss, end-address
'''
opTypeDict = { 0:"NoOp",  # No Operand
               1:"GER",   # General Register 
               2:"DATA",  # Direct Memory Reference (DATA)
               3:"MEM",   # Memory Ref [Base Reg + Index Reg]
               4:"VAR",  # Memory Reg [Base Reg + Index Reg + Displacement]
               5:"IMM",   # Immediate Value
               6:"FADDR",  # Immediate Far Address (CODE)
               7:"NADDR",  # Immediate Near Address (CODE)
               8:"PSY1", # processor specific type
               9:"PSY2", # processor specific type
              10:"PSY3", # processor specific type
              11:"PSY4", # processor specific type
              12:"PSY5", # processor specific type
              13:"PSY6", # processor specific type
              }
def BB_extract(output_file, func):
    cnt = 0
    f = FlowChart(get_func(func))
    cfg_adjmat = []
    temp_BB_Insts = []
    for block in f:
        cfg_row =[0]*f.size
        if print_flag:
            print("{}" .format(output_file))
            print("--Basic Block:")
            print("--BB_ID: [{}]" .format(block.id))
        
        bb_asm_start_address = "{0:x}".format(block.startEA)
        bb_asm_end_address = "{0:x}".format(block.endEA)        

        # get BB instruction
        temp_inst = ""
        for head in Heads(block.startEA, block.endEA):
            if print_flag:
                print("0x{:02x} : {}" .format(head, GetDisasm(head)))
            '''
                regure expression routine
            '''
            if 0: OpHex(head, 1)
            re_routine = GetDisasm(head)
            if print_flag:
                print("oprand | type : \t\t\t\t {} {} {} {} {} | {} {} {} {} {}"
                    .format(GetOpnd(head, 0)
                        ,GetOpnd(head, 1)
                        ,GetOpnd(head, 2)
                        ,GetOpnd(head, 3)
                        ,GetOpnd(head, 4)
                        ,GetOpType(head, 0)
                        ,GetOpType(head, 1)
                        ,GetOpType(head, 2)
                        ,GetOpType(head, 3)
                        ,GetOpType(head, 4)))
            # replace to tag from ida's replacement variable if this match the number of type
            for opNo in range(0, 5):
                if ( GetOpType(head, opNo) in [4,5,6,7,8,9,10,11,12,13] ):
                    re_routine = re_routine.replace(
                                                    GetOpnd(head, opNo),
                                                    opTypeDict[GetOpType(head, opNo)],
                                                    1)

            # all intermediate value(number) change to 0
            #re_routine = re.sub(r"\d+[h]*", "0", re_routine)

            # replace to '' from [ptr, qword, dword, word, short]  into x86 binary 
            if 1:
                re_routine = re.sub(r"[b][y][t][e]", "", re_routine)
                re_routine = re.sub(r"[p][t][r]", "", re_routine)
                re_routine = re.sub(r"[q][w][o][r][d]", "", re_routine)
                re_routine = re.sub(r"[d][w][o][r][d]", "", re_routine)
                re_routine = re.sub(r"[w][o][r][d]", "", re_routine)
                re_routine = re.sub(r"[s][h][o][r][t]", "", re_routine)

            # replace to ~ from space at first 
            re_routine = re.sub(r"\s+", "~", re_routine, 1)
            # replace to ~ from space since second
            re_routine = re.sub(r"\s+", "", re_routine)
            # exception ; of comment
            re_routine = re.sub(r"\;.+$", "", re_routine)

            # change to big string
            re_routine = re_routine.upper()
            if print_flag:
                print("re_routine 1: {}" .format(re_routine))




            temp_inst = temp_inst + " " + re_routine

        # replace to none from space at first 
        temp_inst = temp_inst.lstrip()
        temp_BB_Insts.append([block.id, temp_inst])

        for succ_block in block.succs():
            cfg_row[succ_block.id] = 1
            if print_flag:
                print("Starting Address: {:02x} - Ending Address: {:02x} - BB_ID: [{}]" \
                    .format(succ_block.startEA, succ_block.endEA, succ_block.id))

        cfg_adjmat.append(cfg_row)
    list_BB_Insts.append(temp_BB_Insts)

    temp_cfg = []
    if print_flag:
        print("CFG Adjacency Matrix for Function: {}" .format(GetFunctionName(func)))
    for cfg_row in cfg_adjmat:
        if print_flag:
            print("BB_ID [{}]: {}" .format(cnt, cfg_row))
        cnt += 1
        temp_cfg.append(cfg_row)
    list_CFG.append(temp_cfg)


'''
    get each instructions, basic-block No, and CFG
    [[dataset format]]
        fileN <tab> funcN <tab> CFG <tab> BB_No <tab> Insts <tab> BB_No <tab> Insts ...
'''
def get_all_function_info():
    print("--get_all_function_info()")

    filename = idc.GetInputFile()
    segment_name = ".text"

    count = 1
    for segea in Segments():
        if SegName(segea) == segment_name:
            for funcea in Functions(segea, SegEnd(segea)):
                count += 1
                functionName = GetFunctionName(funcea)

                list_funcN.append(functionName)
                list_fileN.append(filename)

                # get CFG from following function 
                BB_extract(filename, funcea)            

                # get function-Instruction
                for (startea, endea) in Chunks(funcea):
                    for head in Heads(startea, endea):
                        if print_flag:
                            print("{}: 0x{:02x} : {}" .format(functionName, head, GetDisasm(head)))
    print(count)

    # concat all list
    concat_all_list = []
    for x in range(len(list_funcN)):
        concat_all_list.append([list_fileN[x], list_funcN[x], list_CFG[x], list_BB_Insts[x]])

    f = open(outputdir + '/pickle_' + filename +'_'+ filename_opt + '.txt', 'wb')
    list_row_input = concat_all_list
    pickle.dump(list_row_input, f)
    f.close()


    if 0:
        # debug
        print("CONTENTS------------------------------------------------")
        print("list_fileN is {}" .format(list_fileN))
        print("list_funcN is {}" .format(list_funcN))
        print("list_CFG is {}" .format(list_CFG))
        print("list_BB_Insts is {}" .format(list_BB_Insts))
        print("size------------------------------------------------")
        print("list_fileN is {}" .format(len(list_fileN)))
        print("list_funcN is {}" .format(len(list_funcN)))
        print("list_CFG is {}" .format(len(list_CFG)))
        print("list_BB_Insts is {}" .format(len(list_BB_Insts)))
        # print all elements 
        for x in range(len(list_funcN)):
            concat_str = list_fileN[x] +"\t"+ list_funcN[x] +"\t"+ \
                         str(list_CFG[x])[1:-1] +"\t"+ str(list_BB_Insts[x])[1:-1]
            print(concat_str)

'''
----------------------------------------------------------------------------------

----------------------------------------------------------------------------------
'''

'''
    main funciton which make a dataset for nlp machine learning
    and, call making_dataset(), controling each dataset file.txt
'''
if __name__ == '__main__': 
    if False:
        get_hash_info()
    if False:
        get_segments_info()
    if False:
        print_text_segments_info()

    get_all_function_info()

    print("Finish!!")
    
    if 0:
        idc.Exit(0)
