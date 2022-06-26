import pandas as pd

df = pd.read_csv('chen.csv')
a = df['Tahun'].tolist()
b = df['Produksi(Ton)'].tolist()

#Penentuan dMax, dMin, d1, d2, u
dMax = max(b)
dMin = min(b)
# d1 = 20287
# d2 = 1640
d1 = int(input('Masukkan d1: '))
d2 = int(input('Masukkan d2: '))
u = [dMin-d2, dMax+d1] 

def setDifference(b):
  lst = []
  for i in range(len(b)):
    if i == len(b)-1:
      x = b[i]
    else:
      x = abs(b[i+1]-b[i])
    lst.append(x)
  return lst

def calcDiffAmount(data):
  result = 0
  for i in data:
    result += i
  return result

def roundTenThousand(x, base=5):
    return base * round(x/base)

def intervalTable(min, intervalLength, numClass):
  lst = []
  for i in range(numClass):
    lst.append([])

  for i in range(numClass):
    if i == 0:
      lst[i].append(min)
      lst[i].append("A"+str(i+1))
      lst[i].append(min+intervalLength)
      lst[i].append(int((lst[i][0]+lst[i][2])/2))
    else:
      lst[i].append(lst[i-1][2])
      lst[i].append("A"+str(i+1))
      lst[i].append(lst[i-1][2]+intervalLength)
      lst[i].append(int((lst[i][0]+lst[i][2])/2))

  return lst

def fuzzyfy(listIntervalTable ,b):
  lst = []
  for i in b:
    for x in listIntervalTable:
      if i >= x[0] and i <= x[2]:
        lst.append(x[1])
  return lst

def flr(listFuzzyfy):
  lst = []
  for i in range(len(listFuzzyfy)):
    lst.append([])

  for i in range(len(listFuzzyfy)):
    if i == len(listFuzzyfy)-1:
      lst[i].append(listFuzzyfy[i])
      lst[i].append(listFuzzyfy[i])
    else:
      lst[i].append(listFuzzyfy[i])
      lst[i].append(listFuzzyfy[i+1])

  return lst

def convertFLR(tempFLR):
  lst = []
  for i in tempFLR:
    lst.append(i[0]+">"+i[1])
  return lst

def flrg(listIntervalTable,tempFLR):
  curr = []
  for i in listIntervalTable:
    curr.append(i[1])

  tempNext = []
  for i in range(len(listIntervalTable)):
    tempNext.append([])
  for i in range(len(tempNext)):
    for x in tempFLR:
      if curr[i] == x[0] and x[1] not in tempNext[i]:
        tempNext[i].append(x[1])
    tempNext[i].sort(key= lambda x: (len(x), x))
  
  next = []
  for i in range(len(tempNext)):
    str = ""
    str = ", ".join(tempNext[i])
    next.append(str)
  
  res=[]
  for i in range(len(tempNext)):
    amount = 0 
    if len(tempNext[i]) == 0:
      for n in listIntervalTable:
        if curr[i] == n[1]:
          amount += n[3]
    for x in tempNext[i]:
      for n in listIntervalTable:
        if x == n[1]:
          amount += n[3]
    
    if len(tempNext[i]) > 1:
      amount = int(amount/len(tempNext[i])) 
    res.append(amount)
  return list(zip(curr, next, res)),list(zip(curr, tempNext, res))

def forecast(lstTempFLRG, lstFuzzyfy):
  lst = []
  lst.append(0)
  for i in range(1, len(lstFuzzyfy)):
    for x in lstTempFLRG:
      if lstFuzzyfy[i-1] == x[0]:
        lst.append(x[2])
        break

  return lst

def forecastDiff(b, lstForecast):
  lst = []
  lst.append(0)
  for i in range(1, len(b)):
    lst.append(abs(b[i]-lstForecast[i]))
  return lst

def forecastDiff2(b, lstDiffForecast):
  lst = []
  lst.append(0)
  for i in range(1, len(b)):
    lst.append(abs(round((lstDiffForecast[i]/b[i])*100)))
  return lst

def NextPredict(num, lstTempFLRG):
  for i in lstTempFLRG:
    if num in i[1]:
      return i[2]

def showToConsole(final):
  final = final.loc[ : , final.columns != 'Fuzzyfikasi']
  final = final.loc[ : , final.columns != 'FLR']
  return final

def intervalRound(num):
  if num > 0 and num <= 1:
    return round(num, 1)
  elif num > 1 and num <= 10:
    return round(num)
  elif num > 10 and num <= 100:
    return round(num, -1)
  elif num > 100 and num <= 1000:
    return round(num, -2)
  elif num > 1000 and num <= 10000:
    return round(num, -3)
  elif num > 10000 and num <= 100000:
    return round(num, -4)


# Menentukan selisih
diff = setDifference(b)

# Menentukan jumlah selisih
diffAmount = calcDiffAmount(diff)
lstDiffAmount = [' ']*len(b)
lstDiffAmount[0] = diffAmount

# Mencari mean selisih
meanDiff = int(diffAmount/len(b))
lstMeanDiff = [' ']*len(b)
lstMeanDiff[0] = meanDiff

# Menentukan panjang interval
intervalLength = int(meanDiff/2)
intervalLength = intervalRound(intervalLength)
lstIntervalLength = [' ']*len(b)
lstIntervalLength[0] = intervalLength

# Menentukan jumlah kelas
numClass = int((u[1]-u[0])/intervalLength)
lstNumClass = [' ']*len(b)
lstNumClass[0] = numClass

# Membuat tabel interval
listIntervalTable = intervalTable(u[0], intervalLength, numClass)
# print(listIntervalTable)
dfIntervalTable = pd.DataFrame(listIntervalTable)

# Fuzzyfikasi
lstFuzzyfy = fuzzyfy(listIntervalTable ,b)
dfFuzzyfy = pd.DataFrame(lstFuzzyfy, columns = ["Fuzzyfikasi"])

# Menentukan FLR
tempFLR = flr(lstFuzzyfy)
lstFLR = convertFLR(tempFLR)
dfFLR = pd.DataFrame(lstFLR, columns = ["FLR"])

# Menentukan FLRG
lstFLRG, lstTempFLRG = flrg(listIntervalTable,tempFLR)

# Menentukan ramalan
lstForecast = forecast(lstTempFLRG, lstFuzzyfy)

# Menentukan selisih ramalan
lstDiffForecast = forecastDiff(b, lstForecast)

# Menentukan selisih ramalan akhir
lstDiffForecast2 = forecastDiff2(b, lstDiffForecast)

# Menentukan jumlah selisih ramalan akhir
sumDiffForecast = sum(lstDiffForecast2)
lstSumDiffForecast = [' ']*len(b)
lstSumDiffForecast[0] = sumDiffForecast

# Menentukan mape
mape = sumDiffForecast/len(lstDiffForecast2)
lstMape = [' ']*len(b)
lstMape[0] = mape

lstDMax = [' ']*len(b)
lstDMax[0] = dMax

lstDMin = [' ']*len(b)
lstDMin[0] = dMin

# Menentukan ramalan selanjutnya
nextPredict = NextPredict(tempFLR[len(tempFLR)-1][1], lstTempFLRG)
lstNextPredict = [' ']*len(b)
lstNextPredict[0] = nextPredict

final = pd.DataFrame(zip(a, b, diff, lstFuzzyfy, lstFLR, lstForecast, lstDiffForecast, lstDiffForecast2, lstSumDiffForecast, lstNextPredict, lstMape, lstDMax, lstDMin, lstDiffAmount, lstMeanDiff, lstIntervalLength, lstNumClass), columns=['Tahun', 'Produksi', 'Selisih', 'Fuzzyfikasi', 'FLR', 'Nilai Ramalan', 'Selisih Forecasting', 'Selisih Final Forecasting', 'Jumlah Selisih Final Forecasting', 'Ramalan Selanjutnya', 'MAPE', 'Produksi Terbesar', 'Produksi Terkecil', 'Jumlah Selisih Produksi', 'Mean Selisih Produksi', 'Panjang Interval', 'Jumlah Kelas Interval'])

print(showToConsole(final))
print()
print(pd.concat([pd.DataFrame(a), dfFuzzyfy, dfFLR], axis = 1))
# print(final)
dfFLRG = pd.DataFrame(lstFLRG, columns=['Current State', 'Next State', 'Hasil Peramalan'])
final[' '] = [' ']*len(b)
final['Current State'] = dfFLRG['Current State']
final['Next State'] = dfFLRG['Next State']
final['Hasil Peramalan'] = dfFLRG['Hasil Peramalan']
final['  '] = [' ']*len(b)
final['Minimum'] = dfIntervalTable[0]

final['Kelas'] = dfIntervalTable[1]

final['Maksimum'] = dfIntervalTable[2]

final['Median'] = dfIntervalTable[3]


# write DataFrame to excel
final.to_excel('result.xlsx') 