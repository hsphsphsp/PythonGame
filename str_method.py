str_center = "Nein".center(10)
print("*" * 10)
print(str_center)

str_count = "Eye Glasses".count("s")
print(str_count)

str_endswith = "LOL"
print(str_endswith.endswith("L"))
print(str_endswith.endswith("O"))

str_find = "Starlight"
print(str_find.find("t"))
print(str_find.find("s"))

str_format = "{0}, {1}".format(3, "4")
print(str_format)

str_index = "SIMPLICITY or simplicity"
print(str_index.index("i"))
#print(str_index.index(a))

str_alnum = "10ten"
str_alpha = "ten"
str_digit = "10"
str_space = "   "

print(str_alnum.isalnum())
print(str_alnum.isalpha())
print(str_alnum.isdigit())
print(str_alpha.isalpha())
print(str_digit.isdecimal())
print(str_digit.isdigit())
print(str_alpha.islower())
print(str_space.isspace())
print(str_alpha.isupper())

str_join = ("a", "b", "c")
print("-".join(str_join))

str_lower = "NEVER".lower()
print(str_lower)

str_partition = "ABCDE"
str_sep = "C"
print(str_partition.partition(str_sep))

str_replace = "Never"
print(str_replace.replace("e", "E"))
print(str_replace.replace("e", "E", 1))

str_split_1 = "Everything\nIs\nA\nLie"
str_split_2 = "No is No"
str_split_3 = "Yooooh Hoooh~"
print(str_split_1.split())
print(str_split_2.split())
print(str_split_3.split("o"))
print(str_split_1.splitlines())
print(str_split_2.splitlines())

str_strip = " 34 "
print(str_strip.strip().isdigit())

str_upper = "lord voldemort"
print(str_upper.upper())
