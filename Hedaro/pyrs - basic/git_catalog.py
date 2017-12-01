# runipy imports
from runipy.notebook_runner import NotebookRunner
from IPython.nbformat.current import read
from IPython.nbformat.current import write

# logging
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# utility libraries
import subprocess
import pandas as pd
import os
import uuid
import shutil
import time

# custom scripts
import common as comm

# Without this the html links get truncated....wak
pd.set_option("display.max_colwidth",100000)

###############################################################################
###############################################################################

def git_get(repo_path):
    """ given a valid url, list repo files """

    # create final command
    exe = r'git ls-tree --full-tree -r --name-only HEAD'

    # perform action
    # a zero means successful (not always), 1 means fail
    process = subprocess.Popen(exe, stdout=subprocess.PIPE, cwd=repo_path)
    
    # read and clean each line
    ls_lines = process.stdout.readlines()
    out = [x.strip() for x in ls_lines]
    
    # push data to a dataframe
    df = pd.DataFrame(data = out, columns=['short'])
    df['repo'] = repo_path
    df['full'] = repo_path + r'/' + df['short']
    df['name'] = df['short'].apply(lambda x: x.split('/')[-1])
    df['path'] = repo_path + r'/' + df['short'].apply(lambda x: '/'.join(x.split('/')[0:-1])) 
    df['repo2'] = df['repo'].apply(lambda x: x.replace('\\', '\\\\'))
    df['path2'] = df['path'].apply(lambda x: x.replace('\\', '\\\\'))     
    
    # Get everything that says .ipynb
    # Find everything in the "name" column that ends with ".ipynb"
    mask = df['name'].str.endswith('.ipynb')
    
    # Get everything in "mask"
    df = df[mask] 
    
    return df

def git_checkout(check_from_path, check_to_path):
    """ checkout repo """
    
    #print check_from_path, check_to_path

    # suppress output
    f = open(os.devnull, 'w')
    
    # location of repo
    cfp = check_from_path
    
    # check to path
    ctp = check_to_path

    # create final command
    exe = 'git clone ' + '"' + cfp + '"' + ' ' + '"' + ctp + '"'      
    
    # checkout repo
    # a zero means successful (not always), 1 means fail
    return subprocess.call(exe, stdout=f)
    
def nb_run(fname):
    """ given a valid notebook path, run and save notebook """

    # initialize error flag
    err = False
    
    # file name
    fn = fname

    # run notebook
    try:
        notebook = read(open(fn), 'json')
        r = NotebookRunner(notebook)
        r.run_notebook()
        err = False
    except Exception as e:
        logger.error(e)
        logger.debug('failed to run notebook')
        err = True    

    # save notebook
    try:
        write(r.nb, open(fn, 'w'), 'json')
        err = False
    except Exception as e:
        logger.error(e)
        logger.debug('failed to save notebook')
        err = True
    
    return err

def git_add(fname):
    """ mark all changes to be committed """

    # suppress output    
    f = open(os.devnull, 'w')    
    
    # location of repo (case sensitive)
    workingdir = fname

    # create final command
    exe = 'git add -A'
    
    # perform action
    # a zero means successful (not always), 1 means fail
    return subprocess.call(exe, stdout=f, cwd=workingdir)
    
def git_commit(workingdir, message):
    """ commit changes """
    
    # suppress output    
    f = open(os.devnull, 'w')

    # create final command
    exe = 'git commit -m ' + '"' + message + '"'
    
    # perform action
    # a zero means successful (not always), 1 means fail
    # cwd = current working directory
    return subprocess.call(exe, stdout=f, cwd=workingdir)

def git_pull(repo_path, chktopath):
    """ given a valid folder url, commit changes """
    
    # suppress output    
    f = open(os.devnull, 'w')
    
    # location of repo (case sensitive)
    workingdir = repo_path

    # create final command
    exe = 'git pull ' + '"' + chktopath + '"'
    
    # perform action
    # a zero means successful (not always), 1 means fail
    # cwd = current working directory
    return subprocess.call(exe, stdout=f, cwd=workingdir)    
    
###############################################################################
###############################################################################

def nb_update(repo_path, fpath, fname, msg):
    """ checkout, run, save, commit, pull notebook """
    
    err = True
    #print repo_path, fpath, fname, msg
    
    # current directory
    cdir = os.path.dirname(os.path.realpath(__file__))
    print cdir    

    # notebook  file name
    nbfn = fname
    
    # file path
    fpath = fpath[len(repo_path)+1:]

    # checkout folder name
    # make unique name to avoid issues
    chkfolder = str(uuid.uuid4().hex)

    # check to path
    chktopath = cdir + '\\' + 'tmp' + '\\' + chkfolder
    
    # create temp folder
    if not os.path.exists(chktopath):
        os.makedirs(chktopath)

    # notebook file path
    nbfp = chktopath + '\\' + fpath + '\\' + nbfn

    # go!
    if git_checkout(repo_path, chktopath) == 0:
        if nb_run(nbfp) == 0:
            if git_add(chktopath) == 0:
                if git_commit(chktopath, msg) == 0:
                    if git_pull(repo_path, chktopath) == 0:
                        err = False       

    # delete repo if it exists
    try:
        time.sleep(5) # make sure all previous events have completed
        shutil.rmtree(chktopath, onerror = comm.remove_readonly)
    except OSError:
        pass         
    
    return err    

    


    

      