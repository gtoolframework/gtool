from gtool.filewalker import StructureFactory

mypath = 'test\\test11data'

sf3 = StructureFactory.treewalk(mypath)

print(sf3.children[0].path)
print(sf3.children[3].dataasobject)