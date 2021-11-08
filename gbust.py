#!/usr/local/bin/python3

# TODO: Add output to files
# TODO: add ffuf -w ~/hacking/tools/wordlists/test.txt -u http://andreaswienes.de/FUZZ -e \~
# TODO wrapper for ffuf

''' 
A simple wrapper for GoBuster, just written to avoid typing the same things over and over again
Author: Andreas Wienes - Hack Like Demons - https://twitter.com/AndreasWienes

First draft: 2021-11-07
'''

import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('usecase', help='which wordlist to use - options are: common, backup, compressed, office')
parser.add_argument('method', help='which HTTP method to use - options are: get or post')
parser.add_argument('target', help='target url including http or https')
parser.add_argument('file_extensions', nargs='?', help='one or more file extensions to look for')
args = parser.parse_args()

word_list = '~/hacking/tools/wordlists/hld_web_content.txt' # add your default wordlist here
use_case = args.usecase
method = args.method.upper()
target = args.target
file_extensions = args.file_extensions

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'

if file_extensions: 
   file_extensions = "-x " + file_extensions
else:
   file_extensions = ""

match use_case: 
   case "common":
      print(f"Using HackLikeDemons default wordlist to scan {target}")
      gobuster_command = f"gobuster dir -t 50 -w {word_list} -m {method} -u {target} {file_extensions} --user-agent={user_agent}"

   case 'compressed':
      print(f"Using HackLikeDemons default wordlist to scan {target} for compressed files")      
      print(f"NOTE 1: This usecase will use GET as HTTP method and will ignore the file extensions argument you have chosen.")
      compressed_file_extensions = 'zip,tar,gz,tgz,tar.gz,rar'
      gobuster_command = f"gobuster dir -t 50 -w {word_list} -m GET -u {target} -x {compressed_file_extensions} --user-agent={user_agent}"
   
   case 'office':
      print(f"Using HackLikeDemons default wordlist to scan {target} for office-like files")      
      print(f"NOTE 1: This usecase will use GET as HTTP method and will ignore the file extensions argument you have chosen.")
      office_file_extensions = 'doc,docx,rtf,xls,xlsx,pptx,pdf,csv'
      gobuster_command = f"gobuster dir -t 50 -w {word_list} -m GET -u {target} -x {office_file_extensions} --user-agent={user_agent}"

   case "backups":
      print(f"Using HackLikeDemons default wordlist to scan {target} for backup files")
      print(f"NOTE 1: This won\'t scan for files that end with a ~ sign, i.e. old_file~")
      print(f"NOTE 2: This usecase will use GET as HTTP method and will ignore the file extensions argument you have chosen.")
      backup_file_extensions = 'old,bak,txt,src,dev,inc,orig,copy,tmp,swp,conf,cfg'
      gobuster_command = f"gobuster dir -t 50 -w {word_list} -m GET -u {target} -x {backup_file_extensions} --user-agent={user_agent}"

   case "php":
      print(f"Using HackLikeDemons default wordlist to scan {target} for php files")      
      php_file_extensions = 'php,php3,php4,php5,phtm,phtml'
      gobuster_command = f"gobuster dir -t 50 -w {word_list} -m {method} -u {target} -x {php_file_extensions} --user-agent={user_agent}"

   case _:
      raise ValueError("Invalid usecase - please use -h option to list available options")

print(gobuster_command)
os.system(gobuster_command)


