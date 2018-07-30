a = [1,2,3]
b = a

if a == b:
	print("a=b")

if a is b:
	print("a's identity is equal to b's")

c = [1,2,3]
if a is c:
	print("a's identity is equal to c's")

print(a)
print(b)
del b
print(b)
