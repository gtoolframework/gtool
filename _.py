def flatten(exp):

    def sub(exp, res):
        if type(exp) == dict:
            for k, v in exp.items():
                yield from sub(v, res+[k])
        elif type(exp) == list:
            for v in exp:
                yield from sub(v, res)
        else:
            yield "/".join(res+[exp])

    yield from sub(exp, [])

l = {'a': [
  {'b':
     {'c': 'd', 'e': 'f', 'g': 'h', 'i': {'j': {'k': ['l'], 'm': 'n'}},
                  'o': {'p': {'q': ['r', 's'], 't': 'u'}}
                  }
            }]
     }


for i in sorted(flatten(l)):
  print(i)


print('\n\n','-' * 20, '\n\n',sep='')

m = {'*': {'a': 'b', 'c': ['d', 'e', 'f', {'f' : 'g'}]}}

for i in sorted(flatten(m)):
  print(i)

print('\n\n','-' * 20, '\n\n',sep='')

m = {'a': 'b', 'c': ['d', 'd', 'e', 'f', {'f' : 'g'}]}

s = set()

for i in sorted(flatten(m)):
  print(i)
  s.add(i)

print(s)