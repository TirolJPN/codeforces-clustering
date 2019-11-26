n = int(input())
a = list(int(i) for i in input().split(" "))
print(n-1)
for i in range(n-1):
    min_elem = a[i]
    min_index = i
    for j in range(i+1, n):
        if a[j] < min_elem:
            min_elem = a[j]
            min_index = j
    print("%d %d" % (i, min_index))
    tmp_elem = a[i]
    a[i] = min_elem
    a[min_index] = tmp_elem
