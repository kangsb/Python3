import pandas as pd
#빈 DataFrame 생성
df1 = pd.DataFrame(columns=range(5))
print(df1)
print('----------------------------------')
#행 추가
df1.loc[0]=[1,2,3,4,5]
print(df1)
print('----------------------------------')
#열 길이 같은 DataFrame 행 병합
df2 = pd.DataFrame(columns=range(5))
df2.loc[0]=[11,12,13,14,15]
print(df2)
print('----------------------------------')
df1 = df1.append(df2)
print(df1)
print('----------------------------------')
#행 길이 같은 DataFrame 열 병합
df3 = pd.DataFrame([[3],[4]],columns=range(5,6))
print(df3)
print('----------------------------------')
df1 = df1.join((df3))
print(df1)
print('----------------------------------')
df4 = pd.DataFrame()
print(df4)
'''
#행 이름 설정
df1.index = range(1,3)
print(df1)
print('----------------------------------')
#열 이름 설정
df1.columns =range(1,7)
print(df1)
print('----------------------------------')
#특정 행 이름 바꾸기
df1.rename(index={2:4},inplace=True)
print(df1)
print('----------------------------------')
#특정 열 이름 바꾸기
df1.rename(columns={6:7},inplace=True)
print(df1)
print('----------------------------------')
#빈 값으로 데이터 넣기
df1.loc[2]=[3,5,6,7,9,2]
import numpy as np
df1[6] = np.nan
df1.loc[3]=np.nan
print(df1)
print('----------------------------------')
#행 순서 바꾸기
df1 = df1.reindex(index=[1,2,3,4])
#열 순서 바꾸기
df1=df1[list(range(1,8))]#df1[[1,2,3,4,5,6,7]]
print(df1)
print('----------------------------------')

'''