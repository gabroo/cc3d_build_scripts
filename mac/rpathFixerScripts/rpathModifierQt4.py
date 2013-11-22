# this script generates shell file with commands which change hard-coded library dependency path to @rpath convention.
# you typically run this script from the directory level one above CC3D installation directory . The string  fromPathReStr is actually used filter out Qt install paths in the dependency list
# after this script finishes running a shell script is generated which is meant to be run from the console from the same directory level as this script

rootDir='./CC3D_3.7.1/Deps/'

fileMatchExpr='*Qt*'





# fromPathReStr='/Users/Shared/CC3Ddev/Qt-4.8.3/[*]+/Versions/4/'
fromPathReStr='/Users/Shared/CC3Ddev/Qt-4.8.3/'

import fnmatch
import os
import re

fromPathRe=re.compile(fromPathReStr)


matches = []
for root, dirnames, filenames in os.walk(rootDir):
  for filename in fnmatch.filter(filenames, fileMatchExpr):
      matches.append(os.path.join(root, filename))

print 'matches=',matches

matchesDylibs = []
for root, dirnames, filenames in os.walk(rootDir):
  for filename in fnmatch.filter(filenames, '*.dylib'):
      matchesDylibs.append(os.path.join(root, filename))


print 'matchesDylibs=',matchesDylibs
matches+=matchesDylibs
from subprocess import Popen,PIPE
print Popen("echo Hello World", stdout=PIPE, shell=True).stdout.read()


command_file = open('rpathizerQt4.sh','w')
for libname in matches:
	outLines=Popen("otool -L "+libname, stdout=PIPE, shell=True).stdout.read()
	outLines=outLines.split('\n')
	# print 'outLines=',outLines
	for lineLib in outLines:
		# print 'will try to to match on ',line		
		# pathRegex=re.compile('([\S]*)([\s\S]*)(\(comp[\s\s*])')
		pathRegex=re.compile('([\s]*/Users/[\s\S]*)(\()')
		pathGroups=pathRegex.search(lineLib)
		if pathGroups: 
			# print lineLib
			# print 'FOUND:', pathGroups.group(1)
			orig_path=pathGroups.group(1)
			orig_path=orig_path.strip()
			orig_path_split=orig_path.split('/')

			libCoreName=orig_path_split[-1]
			print 'libCoreName=',libCoreName 
			command='install_name_tool -change '+orig_path+' @rpath/Deps/'+libCoreName+' '+libname

			print >>command_file , command

			print 'command=',command
			# outLines=Popen("otool -L "+libname, stdout=PIPE, shell=True).stdout.read()
			# break

		# print 'pathMatch=',pathMatch
	# 	matchObj=fromPathRe.match(line)
	# 	print matchObj
	# break

command_file.close()