import pandas as pd
import numpy as np
import openpyxl
import os
import sys

calParam_Raw = np.array([
    [0, 254, 819, 1611, 3574, 10389, 11389, 12389],
    [0, 387, 1076, 2244, 4971, 13976, 14976, 15976],
    [0, 372, 1115, 2211, 4660, 12016, 13016, 14016],
    [0, 228, 744, 1489, 3323, 10087, 11087, 12087],
    [0, 245, 711, 1452, 3227, 9861, 10861, 11861],
    [0, 72, 232, 517, 1190, 4380, 5380, 6380],
    [0, 282, 811, 1659, 3734, 10770, 11770, 12770],
    [0, 190, 614, 1272, 2829, 8384, 9384, 10384]
])
calParam_Mea = np.array([
    [0, 18, 39, 74, 154, 448, 548, 648],
    [0, 18, 39, 74, 154, 448, 548, 648],
    [0, 18, 39, 74, 154, 448, 548, 648],
    [0, 18, 39, 74, 154, 448, 548, 648],
    [0, 18, 39, 74, 154, 448, 548, 648],
    [0, 18, 39, 74, 154, 448, 548, 648],
    [0, 18, 39, 74, 154, 448, 548, 648],
    [0, 18, 39, 74, 154, 448, 548, 648]
])
temper_table = np.array([[270, 81], [700, 100], [860, 122], [960, 151], [1090, 192]])


def find_table_index(temp):
    i = 0
    for i in range(len(temper_table)):
#        print(i, temper_table[i][0])
        if temp > temper_table[i][0]:
            continue
        else:
            break
    i = i - 1
    if i < 0:
        i = 0
    if i >= 4:
        i = 3
    return i

def fLinearEq(x1, y1, x2, y2, x):
    if x <= x1:
        y = y1
    elif x >= x2:
        y = y2
    else:
        if x2 == x1:
            y = 0
        else:
            y = (((y2 - y1) / (x2 - x1)) * x) + (((x2 * y1) - (x1 * y2)) / (x2 - x1)); 

    return y

def convert_concent(ch, value):
    if value > calParam_Raw[ch][6]:
        i = 6
    elif value > calParam_Raw[ch][5]:
        i = 5
    elif value > calParam_Raw[ch][4]:
        i = 4
    elif value > calParam_Raw[ch][3]:
        i = 3
    elif value > calParam_Raw[ch][2]:
        i = 2
    elif value > calParam_Raw[ch][1]:
        i = 1
    else:
        i = 0

    if value >= calParam_Raw[ch][i]:
        temp = (value - calParam_Raw[ch][i])
    else:
        temp = 0
                
    temp1 = (calParam_Mea[ch][i+1] - calParam_Mea[ch][i]) * temp
    temp2 = calParam_Raw[ch][i+1] - calParam_Raw[ch][i]
                
    if temp2 == 0:
        temp2 = 1
                
    concentValue = calParam_Mea[ch][i] + (temp1 / temp2)
    return concentValue



if __name__ == '__main__':
    if len(sys.argv) == 2:
        input_file = sys.argv[1]
    else:
        print("usage: %s [input txt]" % sys.argv[0])
        sys.exit()

    split_name = os.path.splitext(input_file)
    df = pd.read_excel(input_file)
    df_exel = pd.DataFrame(df['Date'])

    ch = 7 # for change the channel number, modify this

    output_file = split_name[0] + '_New' + split_name[1]

    for ch in range(8):
        ch_name = 'CH' + str(ch + 1)
        ch_conc_df = df[ch_name]
        ch_cnt_df = df[ch_name + '_CNT1']
        ch_temp_df = df[ch_name + '_Temp']
        df[ch_name + '_ORIGIN'] = 0
        df[ch_name + '_FACTOR'] = 0

        for i in range(len(ch_cnt_df)):
            value = ch_cnt_df[i]
            sensorTemp = ch_temp_df[i] * 10
            concentValue = convert_concent(ch, value)
            df[ch_name + '_ORIGIN'][i] = concentValue
            #print("%d original concentValue = %d" % (i, df['ORG'][i]), end=" ")
            index = find_table_index(sensorTemp)
            tempFactor = fLinearEq(temper_table[index][0], temper_table[index][1], temper_table[index+1][0], temper_table[index+1][1], sensorTemp)
            #print("tempFactor = %d" % tempFactor, end=" ")
            concentValue = (concentValue * tempFactor) / 100
            df[ch_name + '_FACTOR'][i] = concentValue
    #        print("factored concentValue = %d" % df['TEM'][i], end=" ")
    #        print()

        df_exel = df_exel.join(ch_conc_df)
        df_exel = df_exel.join(df[ch_name + '_ORIGIN'])
        df_exel = df_exel.join(df[ch_name + '_FACTOR'])
        df_exel = df_exel.join(ch_cnt_df)
        df_exel = df_exel.join(ch_temp_df)
    
    with pd.ExcelWriter(output_file, mode='w', engine='openpyxl') as writer:
        df_exel.to_excel(writer, index=False)

