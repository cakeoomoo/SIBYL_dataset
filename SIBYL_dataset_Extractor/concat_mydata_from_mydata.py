# -*- coding: utf-8 -*-

import pickle
import pprint
import numpy as np

'''
--------------------------------------------------------------------------------------------------
                            show dataset !!!!
--------------------------------------------------------------------------------------------------
'''
'''
    show all contents from all picle dataset
'''
def show_picle_dataset(filefullpath, printElementF, flag_multi):
    f = open(filefullpath, 'rb')
    list_row_output = pickle.load(f)
    f.close()
    print("--file full path    : {}\n--number of function: {}" .format(filefullpath, len(list_row_output)) )

    # decide number of elements mono dataset or multi dataset 
    numOfElement = 4
    if flag_multi == 1:
        numOfElement = 6

    if printElementF:
        for i in range(numOfElement):
            print("--DEBUG: {}" .format(list_row_output[10][i]))


'''
    show abitrary contents from arbitrary file and function name
'''
def show_disasOfFunc_from_dataset(filefullpath, funcName):
    f = open(filefullpath, 'rb')
    list_all = pickle.load(f)
    f.close()

    # using numpy 
    np_list_all = np.array(list_all)

    np_output_fileN = list(np_list_all[:, 0])
    np_output_functionN = list(np_list_all[:, 1])

    # search 
    for np_ele_funcN in np_output_functionN:
        if funcName == np_ele_funcN:
            indexNo = np_output_functionN.index(np_ele_funcN)
            break
    print('--show one elements!!')
    print(indexNo)
    print(np_output_functionN[indexNo])
    print(np_list_all[indexNo][2])
    print(np_list_all[indexNo][3])


'''
--------------------------------------------------------------------------------------------------
                            concat dataset !!!!
--------------------------------------------------------------------------------------------------
    show abitrary function pair from arbitrary file and function name
        return arm and x86 funciton pair

    filename, funcitonname, CFG_x86, BB_x86, CFG_arm, BB_arm
'''
def make_function_pair_from_picle_dataset(filefullpath01, filefullpath02):
    # read dataset file
    f = open(filefullpath01, 'rb')
    list_all_gcc = pickle.load(f)
    f.close()
    f = open(filefullpath02, 'rb')
    list_all_arm = pickle.load(f)
    f.close()

    # using numpy 
    np_list_all_gcc = np.array(list_all_gcc)
    np_list_all_arm = np.array(list_all_arm)

    # make function list
    np_funcList_gcc = list(np_list_all_gcc[:, 1])
    np_funcList_arm = list(np_list_all_arm[:, 1])

    # concat x86 inst and arm inst if two function name is matched in following loop
    newCatList_x86arm = []
    for funcN_gcc in np_funcList_gcc:
        if (funcN_gcc in np_funcList_arm):
            indexNo_gcc = np_funcList_gcc.index(funcN_gcc)
            indexNo_arm = np_funcList_arm.index(funcN_gcc)

            # store new list from x86 dataset list and arm dataset list
            dataset_list = [np_list_all_gcc[indexNo_gcc][0],
                    np_list_all_gcc[indexNo_gcc][1],
                    np_list_all_gcc[indexNo_gcc][2],
                    np_list_all_gcc[indexNo_gcc][3],
                    np_list_all_arm[indexNo_arm][2],
                    np_list_all_arm[indexNo_arm][3]]
            newCatList_x86arm.append(dataset_list)

    return newCatList_x86arm


if __name__ == '__main__': 
    # directory
    mydataset_dir = 'dataset_all_newReplace/'
    sub_dir = 'mydataset_original/'

    # show all mydataset of mono
    if False:
        fileN_all = ['busybox','httpd','openssl','sqlite','gdb','opensslf101','opensslu101',]
        arch_opt = ['armO0','armO2','armO3','clangO0','clangO2','clangO3','gccO0','gccO2','gccO3']
        for fileN in fileN_all:
            for arcopt in arch_opt:
                filepath = 'pickle_'+ fileN +'_'+ arcopt +'.txt'
                filefullpath = mydataset_dir + sub_dir + filepath
                show_picle_dataset(filefullpath, printElementF=0, flag_multi=0)
                show_disasOfFunc_from_dataset(filefullpath, "main")

    if 1:
        # concat mydataset
        concatfilelist =  ['busybox','httpd','openssl','sqlite','gdb']
        primaryOption =   ['gccO0']
        secondaryOption = ['armO0']
        outputfilename = 'outputtest.txt'
    
        filenamepath01_list = []
        filenamepath02_list = []
        for filename in concatfilelist:
            for x in range(len(primaryOption)):
                filenamepath01_list.append( mydataset_dir + sub_dir + 'pickle_'+ filename +'_'+ primaryOption[x] +'.txt' )
                filenamepath02_list.append( mydataset_dir + sub_dir + 'pickle_'+ filename +'_'+ secondaryOption[x] +'.txt' )
                
        pprint.pprint(filenamepath01_list)
        print("----")
        pprint.pprint(filenamepath02_list)
        # get catlist and concat!
        newlist = []
        for i in range(len(filenamepath01_list)):
            CatList = make_function_pair_from_picle_dataset(filenamepath01_list[i], filenamepath02_list[i])
            newlist += CatList
            print("--len(newlist):{}, len(CatList):{}, 01:{} 02:{}"
                    .format(len(newlist), len(CatList), filenamepath01_list[i], filenamepath02_list[i]))

        # save new picle dataset
        output_filepath = mydataset_dir + outputfilename
        f = open(output_filepath, 'wb')
        pickle.dump(newlist, f)
        f.close()

        show_picle_dataset(output_filepath, printElementF=1, flag_multi=1)

'''
---------------------------------------------------------------------------------------------------
'''