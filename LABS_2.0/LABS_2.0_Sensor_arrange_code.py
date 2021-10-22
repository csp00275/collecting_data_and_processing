import numpy as np

DisSenTheta = np.zeros(24)

for i in range(0,24):
    eight = divmod(i, 8) # eight[0] 몫   eight[1] 나머지
    four = divmod(i, 4) # four[0] 몫   four[1] 나머지
    ind = divmod(four[0],2) # indicator[0] 몫 indicator[1] 나머지  (ind : indicator)

    DisSenR = 50 #센서 반지름
    first = ((-1) ** ind[1]) * 30 * eight[1]
    second = 210 * ind[1]
    third = 90 * ind[0]
    DisSenTheta[i] = ((-1) ** ind[1]) * 30 * eight[1] + 210 * ind[1] + 120 * ind[0]
    print('i:'+ format(i,' 02d')+ ' eight[0]:', eight[0], 'eight[1]:', eight[1], 'four[0]:', four[0], 'four[1]:', four[1], 'ind[0]:', ind[0], 'ind[1]:', ind[1], '1st:',
          first, '2nd:', second, '3rd:', third,'theta:',DisSenTheta[i])

    # print('i:',i, ' four[0]:',four[0],' four[1]:',four[1],' ind[0]:',ind[0],' ind[1]:',ind[1],' theta:',DisSenTheta[i])