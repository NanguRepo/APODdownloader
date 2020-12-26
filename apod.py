# Astronomy Picture of the Day downloader
# Made by Nangu


import shutil
import urllib.request
import re
import os
os.system('cls' if os.name == 'nt' else 'clear')
import sys
import subprocess
try:
   from progress.bar import IncrementalBar
except:
   print("You are missing the module 'progress'. Do you want to install it? (y/n)")
   userinput = input()
   if userinput == "y":
      try:
         os.system('pip3 install progress')
         from progress.bar import IncrementalBar
         os.system('cls' if os.name == 'nt' else 'clear')
      except:
         os.system('sudo apt install python3-pip')
         os.system('sudo pip3 install progress')
   else:
      sys.exit()
from time import sleep
try:
   import requests
except:
   print("You are missing the module 'requests'. Do you want to install it? (y/n)")
   userinput = input()
   if userinput == "y":
      try:
         os.system('pip3 install requests')
         import requests
         os.system('cls' if os.name == 'nt' else 'clear')
      except:
         os.system('sudo apt install python3-pip')
         os.system('sudo pip3 install requests')
   else:
      sys.exit()

args = sys.argv
argnum = len(sys.argv)
downloadAll = False
legacy = False
resume = False
startpoint = 1

if argnum == 2:
   if args[1] == "-all":
      print("This is a very long operation that will take about 10 hours with an optimal internet connection.\nYou can exit the program in Linux by pressing Ctrl+Z, or in Windows by simply closing the terminal window. \nYour progress will be saved, and you will be able to continue at anytime.\nThe program can run in the background while you use your pc, and it won't take up a lot of system resources.\n\nWould you like to continue? (y/n)")
      userinput = input()
      if userinput == "y":
         os.system('cls' if os.name == 'nt' else 'clear')
         pass
      else:
         sys.exit()
      try:
         total, used, free = shutil.disk_usage(os.getcwd())
         mbFree = (free // 1048576)
      except:
         mbFree = 2954

      if mbFree < 4200:
         print("You need to have at least 4200 megabytes free on your drive. Continue anyway? (y/n)")
         userinput = input()
         if userinput == "y":
            pass
         else:
            sys.exit()
      downloadAll = True
      try:
         path = str(os.getcwd() + "/APOD/resumepoint.txt")
         f = open(path, "r")
         progressFile = f.read()
         progress = int(progressFile)
         print("Previous progress has been found. Continue from folder %s? The master ETA will be wrong if you do so. (y/n)" % (progress))
         userinput = input()
         if userinput == "y":
             startpoint = int(progressFile)
         else:
             pass
         f.close()
      except FileNotFoundError:
         print("No progress found. Starting from the beginning...")
   elif args[1] == "-legacy":
      startpoint = 5
      try:
         total, used, free = shutil.disk_usage(os.getcwd())
         mbFree = (free // 1048576)
      except:
         mbFree = 2954

      if mbFree < 2955:
         print("You need to have at least 2955 megabytes free on your drive. Continue anyway? (y/n)")
         userinput = input()
         if userinput == "y":
            pass
         else:
            sys.exit()
      legacy = True
      try:
         path = str(os.getcwd() + "/image/resumepoint.txt")
         print(path)
         f = open(path, "r")
         progressFile = f.read()
         progress = int(progressFile)
         progress = ((progress - 5) / 9322) * 100
         progress = "{:.2f}".format(progress)
         progress = str(progress)
         print("Previous progress has been found. Continue from " + progress + "%? (y/n)")
         userinput = input()
         if userinput == "y":
             startpoint = int(progressFile)
         else:
             pass
         f.close()
      except FileNotFoundError:
         print("No progress found. Starting from the beginning...")

   else:
      print("Argument usage: python3 APOD.py [-all/-legacy]")
      print("This downloads all pictures from NASA's archive.")
         
# 65 columns and 5 lines

if downloadAll == True:
    url = "https://apod.nasa.gov/apod/fap/image"
    os.system('cls' if os.name == 'nt' else 'clear')
    initializationBar = IncrementalBar('Initializing...', max=3, suffix='%(percent)d%%')
    initializationBar.next()
    page = str(urllib.request.urlopen(url).read())
    initializationBar.next()
    sleep(0.5)
    master = re.findall("(?<=/\">).*?(?=/)", page)
    initializationBar.next()
    print("\nStarting download...")
    sleep(1.0)
    os.system('cls' if os.name == 'nt' else 'clear')
    barTarget2 = len(master) - 1
    bar2 = IncrementalBar(max=barTarget2, suffix='%(percent)d%% - ETA: %(eta)d seconds')
    for k in range(1, startpoint):
        bar2.next()
    os.system('cls' if os.name == 'nt' else 'clear')
    for i in range(startpoint, len(master)):
        progress1 = i
        progress2 = len(master) - 1
        progress = str("(%s/%s)" % (progress1, progress2))
        page2 = str(urllib.request.urlopen("https://apod.nasa.gov/apod/fap/image/" + master[i]).read())
        x = re.findall("(?<=<a href=\").*?(?=\")", page2)
        barTarget = len(x) - 5
        bar = IncrementalBar(max=barTarget, suffix='%(percent)d%% - ETA: %(eta)d seconds')
        for j in range(5, len(x)):
            y = str("/APOD/" + master[i] + "/" + x[j])
            z = str("/APOD/" + master[i])
            response = requests.get(str("http://apod.nasa.gov/apod/fap/image/" + master[i] + "/" + x[j]))
            path = str(os.getcwd() + y)
            path2 = str(os.getcwd() + z)
            try:
               os.makedirs(path2)
            except:
               pass
            file = open(path, "wb")
            file.write(response.content)
            file.close()
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Getting images from folder " + master[i] + "... ")
            bar2.update()
            print("\n-------------------------------------------------------")
            print("Succesfully downloaded file " + x[j])
            bar.next()
        bar.finish()
        bar2.next()
        os.system('cls' if os.name == 'nt' else 'clear')
        progresspath = str(os.getcwd() + "/APOD/resumepoint.txt")
        file = open(progresspath, "w")
        file.write(str(i + 1))
        file.close()
    print("Download complete.")
elif legacy == True:
   url = "https://apod.nasa.gov/apod/archivepixFull.html"
   endpoint = 9322
   os.system('cls' if os.name == 'nt' else 'clear')
   page = str(urllib.request.urlopen(url).read())
   master = re.findall("(?<=<a href=\").*?(?=\")", page)
   for i in range(startpoint, endpoint):
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
         targetLength = 165
         for j in range(outputLength, targetLength):
            output = output + ' '
         progress = (((i - 5) / endpoint) * 100)
         formattedProgress = "{:.2f}".format(progress)
         progress = float(formattedProgress)
         print(output + str(progress) + "%")
         progresspath = str(os.getcwd() + "/image/resumepoint.txt")
         file = open(progresspath, "w")
         file.write(str(i))
         file.close()
      except:
         print("Could not get file at " + master[i] + " (probably a YouTube video)")
else:
   print("No arguments were passed to the script.\n\nArguments:\n-all: gets every file in APOD's database. This is the newest version of the APOD downloader.\n-legacy: uses the old script which downloads all pictures in APOD's archive. This doesn't download as many files, has a more primitive user interface, and uses a bad method to download the pictures, which means it'll take a long time to download.")