import utils

test_correct = "0.7 -0.6"

test_ints = "1 -1"

test_zeroes = "0 0"

test_bad_spacing_fails = "0.5    0.6"

test_bad_values_fails = "1000 0.6"

test_not_float_fails = "aaa bbaewf"


def test(data):
    parsedData = utils.parse(data)

    if(parsedData is None):
        print(f"{data} is bad")
    else:
        print(f"{data} is good. [0]={parsedData[0]}, [1]={parsedData[1]}")

test(test_correct)
test(test_ints)
test(test_zeroes)
test(test_bad_spacing_fails)
test(test_bad_values_fails)
test(test_not_float_fails)



