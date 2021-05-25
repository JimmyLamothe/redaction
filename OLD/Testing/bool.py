def test_bool(var1, var2):
    result1 = False
    result2 = False
    if not var1 or not var2:
        print(True)
        result1 = True
    if (not var1) or (not var2):
        print(True)
        result2 = True
    print('1', result1)
    print('2', result2)
    print('same?', result1 == result2)

