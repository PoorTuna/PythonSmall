def count_plus_ten(num, count):
    arr = []
    while count > 0:
        for num in range(num, num + 10, 1):
            arr.append("help" + str(num))
            print num
            num += 1
        count -= 1
    return arr


help_count = count_plus_ten(0, 3)
print help_count

for item in range(0, len(help_count), 1):
    if 'help' + str(item) in help_count:
        help_count.remove('help' + str(item))
    else:
        print "l"

print help_count
print 4
