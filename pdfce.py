#! /bin/python

import sys
import zlib

#Extract the encoded ToUnicode Cmap from the pdf
def extractdata (pdf):
	#Look for ToUnicode string
	offset = pdf.find("\x54\x6F\x55\x6E\x69\x63\x6F\x64\x65",0)
	if (offset < 0):
		print "Error: ToUnicode not found"
		return
	start_block = pdf[offset+10:pdf.find("\x52",offset)]
	start_block = pdf.find(start_block,0)
	start_block = pdf.find('\x78',start_block)
	end_block = pdf.find('\x65\x6E\x64', start_block)	
	return pdf[start_block:end_block]

#Decompress the Cmap and save it into output_cmap file
def getCmap (pdf, output_cmap):
	decomp = zlib.decompress(extractdata(pdf))
	open(output_cmap,'w').write(decomp)

#Compress the input_cmap and put it inside the pdf
def putCmap (path, pdf, input_cmap):
	comp = zlib.compress(open(input_cmap,"r").read())
	open(path,'w').write(pdf.replace(extractdata(pdf),comp))

#Delete the Cmap from the pdf
def deletedata (path, pdf):
	open(path,'w').write(pdf.replace(extractdata(pdf),""))

if (len(sys.argv) < 3):
	print "\nUsage: "+sys.argv[0]+" "+"<option> [<cmap_file>] <pdf>\n"
	print "option:\n\t--strip,-s\tRemove the ToUnicode Cmap\n"
	print "\t--export,-e\tExtract the Cmap from the pdf\n"
	print "\t--import,-i\tPut the Cmap into the pdf\n"
else:
	if (sys.argv[1] == "-s") or (sys.argv[1] == "--strip"):
		pdf = open(sys.argv[2], "rb").read()
		deletedata (sys.argv[2],pdf);
	elif (sys.argv[1] == "-e") or (sys.argv[1] == "--extract"):
		pdf = open(sys.argv[3], "rb").read()
		getCmap(pdf,sys.argv[2])
	elif (sys.argv[1] == "-i") or (sys.argv[1] == "--import"):
		pdf = open(sys.argv[3], "rb").read()
		putCmap(sys.argv[3],pdf,sys.argv[2])