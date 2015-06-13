#!/usr/bin/env python2

packagelist = open("packages.xml", "r")
package_notrans = open("packages.en.xml", "w")

while True:
	line = packagelist.readline()
	
	if "xml:lang" in line:
		pass
	elif line == "\n":
		break;
	else: 
		package_notrans.write(line)

package_notrans.close()
packagelist.close()
