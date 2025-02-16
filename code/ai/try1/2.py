from openai import OpenAI
import sys
import os
import shutil
import glob
import subprocess
import logging
from time import gmtime, strftime
import time
import getopt
from git import Repo

client = OpenAI(
    base_url="https://api.aimlapi.com/v1",
    api_key="7344b1a12e2c482687f9ebe0143a6435",
)

diff_output='1'

def gitdiff():
  repo = Repo('~/src/itc-test1')
  t = repo.head.commit.tree
 # filename = '~/src/itc-test1/a_folder/tb.code-workspace'
  diff_output = repo.git.diff(t)
  return diff_output
  #print(diff_output)



def aiask(question,diff_output):
#        print(diff_output)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI assistant who knows everything.",
                },
                {
                    "role": "user",
                    "content": "base on this git diff , give me one line commit message : the git diff is in file /tmp/a1 "
                },
            ],
        )
        message = response.choices[0].message.content
        print(f"Assistant: {message}")







BLNAME = ''
QUESTION = ''

#default list
LIST1 = ['.msi','.exe','.zip']

tnow = strftime('%Y%m%d%H%M%S', gmtime())

def del_folder(dest_dir):
    if os.path.exists(dest_dir):
        try:
            shutil.rmtree(dest_dir)
        except:
            raise

def flushdir(dir):
    now = time.time()
    for f in os.listdir(dir):
        fullpath = os.path.join(dir, f)
        if fullpath.endswith('.zip'):
            print(fullpath)
            if os.stat(fullpath).st_mtime < (now - 84400):
                if os.path.isfile(fullpath):
                    os.remove(fullpath)
                elif os.path.isdir(fullpath):
                    flushdir(fullpath)

def copy_ext_files(source_dir, dest_dir, ext):
    print('copy files from ' + source_dir + ' to ' + dest_dir + ' ext ' + ext)
    if not os.path.exists(source_dir):
        logging.error("Source folder %s not exist" % source_dir)
        sys.exit(1)
    if not os.path.exists(dest_dir):
        logging.info("Target folder %s not exist. now created" % dest_dir)
        os.makedirs(dest_dir)
    os.chdir(source_dir)
    for file in glob.glob(ext):
        try:
            shutil.copy2(os.path.join(source_dir, file), dest_dir)
        except IOError as e:
            logging.error("Copy Problem : %s" % e)
            sys.exit(1)

def check_pre_requirements():
    logging.info("Checking that the mandatory parameters are not empty")
    if QUESTION == "":
        logging.error("Error missing mandatory SERVER")
        usage()
  
    logging.info("End of base checks")

def usage(exit_value=2):
    print( 'This script does .. ')
    print( '--question "ask ai stuff"')
    sys.exit(exit_value)

def main():
    print( 'main'  )
    #//print 'Call python exe_msi.py to text file list1.txt'  	
    #var = "python exe_msi.py --folder_name " + FOLDER + " --list_ext " + FILES    
    print('The Question '+QUESTION)
    
    diff_output=gitdiff()
    aiask(QUESTION,diff_output)
    #os.system('%s > list1.txt' % var)

if __name__ == '__main__':
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "hq:b:c:", ["question=", "bl_name=","list1="])
    except getopt.GetoptError:
        usage()
    for opt, arg in opts:
        if opt == '-h':
            usage()
        elif opt in ("-q", "--question"):
            QUESTION = arg        
        elif opt in ("-b", "--bl_name"):
            BLNAME = arg
        elif opt in ("-c", "--list1"):
            LISTMP = arg
            LIST1 = LISTMP.split(',')


    logger = logging.getLogger('myapp')
    hdlr = logging.FileHandler('/tmp/myapp.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 

    #logger.setLevel(logging.WARNING)
    logger.setLevel(logging.DEBUG)

    logger.error('We have a problem')
    logger.info('While this is just info')

    LOG_PATH = '/tmp'
    if not os.path.exists(LOG_PATH):
        os.makedirs(LOG_PATH)

    check_pre_requirements()
    main()
