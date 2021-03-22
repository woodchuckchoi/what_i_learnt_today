bigList = range(10000)
rdd = sc.parallelize(bigList, 2) # partition bigList into 2 and store them in executor(s)
odd = rdd.filter(lambda x: x % 2 != 0)
print('Num of odd numbers smaller than 10000 is {}'.format(odd.count()))
print('First five odd numbers are {}'.format(odd.take(5)))

