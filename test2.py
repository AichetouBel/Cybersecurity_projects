def missing_number(list1, list2):
    set1 = set(list1)
    set2 = set(list2)
    miss_number = set1 - set2
    return list(miss_number)

def create_list(n):
    l = []
    for i in range(2, n + 1):
        l.append(i)
    return l
n=int(input(''))
input_list = input('')
int_list = input_list.split()
list_n = create_list(n)
int_list = [int(x) for x in int_list]  
dif = missing_number(list_n, int_list)
output_list = dif
print(" ".join(map(str, output_list)))


