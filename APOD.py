# Astronomy Picture of the Day downloader
# Made by Nangu



import urllib.request
import re
import requests
import os
import sys, getopt

args = sys.argv
argnum = len(sys.argv)
downloadAll = False
resume = False
startpoint = 5

if argnum == 2:
   if args[1] == "-all":
      downloadAll = True
   else:
      print("Argument usage: python3 APOD.py -all")
      print("This downloads all pictures from NASA's archive.")
if argnum == 3:
   if args[1] == "-all":
      downloadAll = True
   else:
      print("Argument usage: python3 APOD.py -all")
      print("This downloads all pictures from NASA's archive.")
   if args[2] == "-resume":
      try:
         path = str(os.getcwd() + "/image/resumepoint.txt")
         f = open(path, "r")
         startpoint = int(f.read())
         f.close()
      except FileNotFoundError:
         print("No progress found. Starting from the beginning...")
         


if downloadAll == True:
   page = str(urllib.request.urlopen("https://apod.nasa.gov/apod/archivepix.html").read())
   master = re.findall("(?<=<a href=\").*?(?=\")", page)
   for i in range(startpoint, 2187):
      try:
         page2 = str(urllib.request.urlopen("https://apod.nasa.gov/apod/" + master[i]).read())
         x = re.findall("(?<=<IMG SRC=\").*?(?=\")", page2)
         y = str("http://apod.nasa.gov/" + x[0] + "--END--")
         response = requests.get(str("http://apod.nasa.gov/" + x[0]))
         z = re.findall("(?<=apod.nasa.gov).*?\d+", y)
         img = re.findall("(?<=apod.nasa.gov).*?(?=--END--)", y)
         path = str(os.getcwd() + z[0] + "/")
         path2 = str(os.getcwd() + img[0])

         try:
            os.makedirs(path)
         except:
            pass

         file = open(path2, "wb")
         file.write(response.content)
         file.close()

         output = "Succesfully downloaded file at " + path2
         outputLength = len(output)
         targetLength = 180
         for j in range(outputLength, targetLength):
            output = output + ' '
         progress = (((i - 5) / 2182) * 100)
         formattedProgress = "{:.2f}".format(progress)
         progress = float(formattedProgress)
         print(output + str(progress) + "%")
         progresspath = str(os.getcwd() + "/image/resumepoint.txt")
         file = open(progresspath, "w")
         file.write(str(i))
         file.close()
      except:
         print("Could not get file at " + master[i] + " (probably a YouTube video)")



page = str(urllib.request.urlopen("https://apod.nasa.gov/").read())
x = re.findall("(?<=<IMG SRC=\").*?(?=\")", page)
y = str("http://apod.nasa.gov/" + x[0] + "--END--")
response = requests.get(str("http://apod.nasa.gov/" + x[0]))
z = re.findall("(?<=apod.nasa.gov).*?\d+", y)
img = re.findall("(?<=apod.nasa.gov).*?(?=--END--)", y)
path = str(os.getcwd() + z[0] + "/")
path2 = str(os.getcwd() + img[0])

try:
   os.makedirs(path)
except:
   pass

file = open(path2, "wb")
file.write(response.content)
file.close()

print("Picture saved.")
