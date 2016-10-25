
fruits = ['banana', 'apple',  'mango']
for index in range(len(fruits)):
    print ('当前水果 :', fruits[index])

print ("Good bye!")
'''
year = int(input('year:\n'))
month = int(input('month:\n'))
day = int(input('day:\n'))

months = (0,31,59,90,120,151,181,212,243,273,304,334)
if 0 <= month <= 12:
    sum = months[month - 1]
else:
    print ('data error')
sum += day
leap = 0
if (year % 400 == 0) or ((year % 4 == 0) and (year % 100 != 0)):
    leap = 1
if (leap == 1) and (month > 2):
    sum += 1
print ('it is the %dth day.' % sum
       )
'''
'''
for i in range(1,10):
    for j in range(1,10):
        result = i * j
        print ('%d * %d = % -3d' % (i,j,result))
    print ('')
    '''