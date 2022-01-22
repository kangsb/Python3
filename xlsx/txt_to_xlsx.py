import pandas as pd
import sys
import os

input_file = 'Chamber_Data_20220118/-20.txt'

if __name__ == '__main__':
    verbose = False
    if len(sys.argv) == 2:
        input_file = sys.argv[1]
        file_name = os.path.splitext(input_file)
        output_file = file_name[0] + '.xlsx'
    elif len(sys.argv) == 3:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
    else:
        print("usage: %s [input txt]" % sys.argv[0])
        print("               or")
        print("       %s [input txt] [output xlsx]" % sys.argv[0])
        sys.exit()

    df = pd.DataFrame(pd.read_csv(input_file, sep=' '))
    df.rename(columns={df.columns[0]: 'Date'}, inplace=True)
#    print(df.columns)
    df.to_excel(output_file,index=False) 