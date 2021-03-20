def test_array1(array):
    for index, i in enumerate(array):
        if i == '0':
            return index


def test_array2(array):
    return array.find('0')


def test_array3(array):
    ones = array.count('1')
    return ones
