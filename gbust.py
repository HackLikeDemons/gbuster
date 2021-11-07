#!/usr/local/bin/python3

''' 
A simple wrapper for GoBuster, just written to avoid typing the same things over and over again
Author: Andreas Wienes - Hack Like Demons - https://twitter.com/AndreasWienes

First draft: 2021-11-07
'''

import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('usecase', help='which wordlist to use - options are: common')
parser.add_argument('method', help='which HTTP method to use - options are: get or post')
parser.add_argument('target', help='target url including http or https')
parser.add_argument('file_extensions', nargs='?', help='one or more file extensions to look for')
args = parser.parse_args()

word_list = '~/hacking/tools/wordlists/hld_web_content.txt' # add your default wordlist
use_case = args.usecase
method = args.method.upper()
target = args.target
file_extensions = args.file_extensions

if file_extensions: 
   file_extensions = "-x " + file_extensions
else:
   file_extensions = ""

match use_case: 
   case "common":
      print(f"Using HackLikeDemons default wordlist to scan {target}")
      gobuster_command = f"gobuster dir -t 50 -w {word_list} -m {method} -u {target} {file_extensions}"
   
   case "backups":
      print(f"Using HackLikeDemons default wordlist to scan {target} for backup files")
      print(f"NOTE 1: This won\'t scan for files that end with a ~ sign, i.e. old_file~")
      print(f"NOTE 2: This usecase will use GET as HTTP method and will ignore the file extensions argument you have chosen.")
      backup_file_extensions = 'old,bak,txt,src,dev,inc,orig,copy,tmp,swp'
      gobuster_command = f"gobuster dir -t 50 -w {word_list} -m GET -u {target} -x {backup_file_extensions}"
      
   case _:
      raise ValueError("Invalid usecase - please use -h option to list available options")

print(gobuster_command)
os.system(gobuster_command)

