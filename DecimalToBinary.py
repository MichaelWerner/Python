iInput = input("Enter a number to be converted to binary: ")
sBinary = []

iResult = 0
iPower = 0

if iInput.isnumeric():
  iNum = int(iInput)
  #Get the highest power of 2 that is smaller than iNum
  while iResult <= iNum:
    sBinary.append(0)
    iPower += 1
    iResult = 2 ** iPower

  #iPower - 1  is now the highest power of 2, it's value in the list is changed to 1 
  iPower -= 1
  sBinary[iPower] = 1

  if 2 ** iPower < iNum:
    iNum -= 2 ** iPower
    iPower -= 1

    for i in range(iPower, -1, -1):  # the stop value is excluded, so we stop at 0
      iTemp = 2 ** i
      if iTemp <= iNum:
        sBinary[i] = 1
        iNum -= iTemp 

  print(iInput, "is binary:", ''.join(map(str, sBinary[::-1])))
else:
  print(iInput, "is not a valid number!")

