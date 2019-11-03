sBinary = input("Enter a binary number to be converted to decimal: ")

#initial values
iDecimal = 0
lError = False
iLength = len(sBinary)

for i in range(0, iLength, 1):
  sTest = sBinary[i]
  
  if sTest != "0" and sTest != "1":         #Only 0 an 1 are allowed in the binary system 
    print(sBinary, "is not a valid binary number!")
    lError = True
    break
  else:
    # Example: sBinary is '101'
    # iLength is 3
    # in the first iteration i is 0
    # iLength - i - 1 is 2
    #     that is the value we need as an exponent because 
    #       the first number in the example is sBinary[0] and represents 2 ** 2, 
    #       the second is sBinary[1] and represents 2 ** 1 
    #       and the third is sBinary[2] and represents 2 ** 0

    iDecimal += int(sTest) * 2 ** (iLength - i - 1)             

if not lError:
  print("Binary", sBinary, "is decimal: ",iDecimal)
