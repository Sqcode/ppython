def reverse_cartesian_product(cartesian_product):
    array1 = set()
    array2 = set()
    
    for item in cartesian_product:
        print(item)
        has_key = any(char.isalpha() for char in item) or "无" in item

        if has_key :
            char_part = item[-1]
            array2.add(char_part)
            num_part = item[:-1]
        else:
            num_part = item
            
        
        if num_part not in array1:
            array1.add(num_part)

        array1.add(num_part)
        # array2.add(char_part)
    
    return sorted(list(array1)), list(array2)

# cartesian_product = ['37A', '38A', '37无', '38无']
# cartesian_product = ['37', '38']
# cartesian_product = ['46', '48', '50', '54']
# cartesian_product = ['170AA', '180AA', '170A无', '180A无']
# cartesian_product = ['37A','37无','38A','38无','39A','39无','40A','40无']
# cartesian_product = ['2_040A', '2_040无', '2_037A', '2_038无', '2_039A', '2_038A', '2_039无', '2_037无']
# result1, result2 = reverse_cartesian_product(cartesian_product)
# print(result1)
# print(result2)
