# \d = digit 
# \D =  not a digit 
# \w = character 
# \W not a character 
# \s = space, tab, new line 
# \S =  not a space, tab, newline 
# . = any character 
# [] = character set,  [a-zA-Z0-9] range of characters and numbers 
# [^ ] = not these characters,  [^0-9] search anything except 0-9 numbers
# + =  one or more,  \d+ one or more digit
# * = zero or more, \w* zero or more word
# ? = zero or one
# {} = range,  \d{4} = \d\d\d\d
# ^ = start, ^\d shd start from a digit
# $ =  end,  john$ shd end by john
# | = or, cat|dog
# () = group,  (ha)+ one or more occurance of the group ha
# \ = escape,  some charactes have special meaing if ur searching for them in them then u have to use escape 


# -----------------------------------------------------------------------------------------------------------------

# re functions

#   re.search()

import re

#text = "Hello 123 world"
#x = re.search(r"\d+", text) # Search through the text and give me the FIRST match.
#print(x.group()) # to gett he actual value


#text = "Hello 123 world 456"
#x = re.findall(r"\d+", text) # give me all the occurances
#print(x) # not using group as it returns more then one value 

text = "123 hello world"
result = re.match(r"\d+", text) # check s from the begning
print(result)
# text = "hello 123 world"if i taje this as the text and run match to dinf the digits it will come as none as the digits r not in the begining 