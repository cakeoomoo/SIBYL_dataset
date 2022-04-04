# -*- coding: utf-8 -*-

import re
import pickle
import os
import pprint
import time

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

sudo_cmd = 'sudo '

idaCmdPath = '/home/'
inputDir = '/home/'
outputDir = '/home/'

#---------------------------------------------------------------------------------------------
binaryfile_list = ['CRC32', 'TEST_BIN', 'ssh_O2', 'ssh_O3']
#binaryfile_list = ['ssh_O2']


binaryfile_list_all = ['busybox','httpd','openssl','sqlite']
binaryfile_list_all_sub = ['gccO3']
binaryfile_list_all_fileN = ['busybox','httpd','openssl','sqlite']

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------


def ida_python_cmd_run():
    for x in binaryfile_list:
        cmd01 = sudo_cmd + idaCmdPath + inputDir + x
        print(cmd01)
        os.system(cmd01)
        time.sleep(1)


def concat_picle_dataset():
    # input arbitrary file
    for x in binaryfile_list:
        print("\n\n-----------------------------------")
        f = open(outputDir + 'picle_' + x + '.txt', 'rb')
        list_row_output = pickle.load(f)
        f.close()
        # control dataset from picle dataset 
        print(list_row_output)
    #pprint.pprint(list_row_output)
    print(len(list_row_output))

    pprint.pprint(list_row_output[100])




def ida_python_cmd_run_all():
    for x in binaryfile_list_all:
        for dsub in binaryfile_list_all_sub:
            cmd01 = sudo_cmd + idaCmdPath + inputDir + x +'/'+ dsub +'/'+ x
            print(cmd01)
            os.system(cmd01)
            time.sleep(1)


def concat_picle_dataset_all():
    # input arbitrary file
    for x in binaryfile_list_all:
        for dsub in binaryfile_list_all_sub:
            print("\n\n-----------------------------------")
            f = open(outputDir + 'picle_' + x + dsub + '.txt', 'rb')
            list_row_output = pickle.load(f)
            f.close()
            # control dataset from picle dataset 
            print(list_row_output)
    #pprint.pprint(list_row_output)
    print(len(list_row_output))

    pprint.pprint(list_row_output[100])


if __name__ == '__main__': 
	
	if 1:
		return 0

    # make dataset by picle 
    print("--concat_picle_dataset start!")

    # flag setting 
    test_flag = False
    all_flag = True

    makedataset_flag = True

    if test_flag:
        if makedataset_flag:
            ida_python_cmd_run()
        else:
            concat_picle_dataset()

    if all_flag:
        if makedataset_flag:
            ida_python_cmd_run_all()
        else:
            concat_picle_dataset_all()


    print("--concat_picle_dataset exit!")







