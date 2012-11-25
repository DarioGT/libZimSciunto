#!/usr/bin/env python

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>

"""
Functions dealing with zim notebooks
"""

import os
import glob
import logging
logger = logging.getLogger(__name__)

def get_zim_files(zim_root):
    """
    Get the list of txt zim files

    :param zim_root: filepath of the zim root directory
    :returns: list
    """
    logger.info('Looking for zim files in ' + str(zim_root))
    zim_files = []
    for root, dirnames, filenames in os.walk(zim_root):
        #Do not inspect .Archive
        if '.Archive' in dirnames:
            dirnames.remove(".Archive")
        logger.debug('look in ' + str(root))
        for filename in glob.glob(os.path.join(root, '*.txt')):
            logger.debug('file ' + filename)
            
            zim_files.append(filename)
    if zim_files == []:
        logger.warning('No zim file found!')
    logger.debug('List of zim files')
    logger.debug(zim_files)
    return zim_files


import threading
from queue import Queue

class ThreadZimfiles(threading.Thread):
    """
    Process Zim files to create archives

    :param lock: lock from Threading
    :param timechecker: Instance of TimeChecker
    :param zim_file_queue: Queue contraing zim files
    :param zim_root: filepath of the zim notebook root
    :param zim_archive_path: .Archive
    :param process_text_method: Function processing the text
    :param args: arguments for process_text_method


    Note: The method 'process_text_method' should return a tuple (bool, string).
    The boolean (if True) is used to avoid a modification of the time database
    by timechecker. This is useful when some modifications could not be done
    now but that have a chance to suceed later.
    The string contains the modified text.
    """
    def __init__(self, lock, timechecker, zim_file_queue, zim_root, process_text_method, *args):
        """
        Constructor
        """
        threading.Thread.__init__(self)
        self.lock = lock
        self.timechecker = timechecker
        self.zim_file_queue = zim_file_queue
        self.zim_root = zim_root
        self.process_text_method = process_text_method
        self.args = args
    
    def run(self):
        """ Job: 

        * Read the zim file
        * Look for links
        * Archive links when necessary
        """
        while True:
            zim_file = self.zim_file_queue.get()
            print(zim_file)
            #read
            with open(zim_file, 'r') as thefile:
                original_text = thefile.read()
            
            #process
            (error, new_text) = self.process_text_method(original_text, *self.args)
            
            #write
            with open(zim_file, 'w') as thefile:
                thefile.write(new_text)

            #Update time
            #In case of error, we don't set the current time.
            #Maybe the user missed something, and the script should not
            #skip the file next time to try again.
            if not error:
                relativepath = os.path.relpath(zim_file, start=self.zim_root)
                with self.lock:
                    self.timechecker.set_time(relativepath)

            #Done
            self.zim_file_queue.task_done()

def process_zim_file(timechecker, zim_root, zim_files, process_text_method, checktime, num_thread, *method_args):
    """
    Archive links in zim_files
    
    :param timechecker: Instance of TimeChecker()
    :param zim_root: filepath of the zim notebook root
    :param zim_files: 
    :param process_text_method: Function processing the text
    :param checktime: Check last modification time prior processing
    :param num_threads: number of threads
    :param method_args: arguments for process_text_method
    """

    file_queue = Queue()
    lock = threading.Lock()
    #Set up threads
    for thread in range(num_thread):
        worker = ThreadZimfiles(lock, timechecker, file_queue, zim_root, process_text_method, *method_args)
        worker.setDaemon(True)
        worker.start()

    for thisfile in zim_files:
        thisfile_relativepath = os.path.relpath(thisfile, start=zim_root)
        with lock:
            filestatus = timechecker.get_file_modif_status(thisfile_relativepath)
        if filestatus and checktime:
            #This zimfile has been updated, do it
            file_queue.put(thisfile)
        elif not checktime: 
            #We don't check time, do it
            file_queue.put(thisfile)
        else:
            #Nothing to do
            pass

    file_queue.join()

if __name__ == '__main__':
    pass

