L = ['one', 2, 'three', 4, 'five', 6]

L[-1] = 'Alegruz'

for i in range(len(L)):
    if type(L[i]) == str:
        alpha_index = i
        break

print(L[-4], L[i])
