import re

input_string = "2_037"
right_digits = re.search(r'\d+', input_string.split('_')[1]).group() if '_' in input_string else ""
print(right_digits)


if '_' in input_string:
    print(input_string.split('_')[1])
# input_string.split('_')[1]
