
train =  open('2048_test.csv', 'w')
test = open('2048_train.csv', 'w')
with open('2048.csv', 'r') as f:
    count = 1
    for line in f:
        count += 1
        if count % 2 == 0:
            test.write(line)
        else:
            train.write(line)
