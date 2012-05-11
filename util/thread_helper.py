################################################################################
# util/hreading_helper.py
# 
# Created by Greg Bayer <greg@gbayer.com>.
# Open sourced at http://github.com/gregbayer/python-threading-utils
################################################################################

import threading
import logging
import sys

class ThreadedWorker(threading.Thread):
    """ Generic Threaded Worker
        Input to work_func: item from work_queue
    
    Example usage:
    
    import Queue
    
    urls_to_process = ["http://url1.com", "http://url2.com", "http://site1.com", "http://site2.com"]
    
    work_queue = Queue.Queue()
    result_queue = Queue.Queue()

    def process_url(url):
        # TODO: Do some work with the url
        return url
    
    def main():
        # spawn a pool of threads, and pass them queue instance 
        for i in range(3):
            t = ThreadedWorker(work_queue, result_queue, work_func=process_url)
            t.setDaemon(True)
            t.start()
            
        # populate queue with data   
        for url in urls_to_process:
            work_queue.put(url)
            
        # wait on the queue until everything has been processed     
        work_queue.join()
        
        # print results
        print repr(result_queue)
    
    main()
    """

    def __init__(self, work_queue, result_queue, work_func, stop_when_work_queue_empty=True, queue_timeout=1):
        threading.Thread.__init__(self)
        self.work_queue = work_queue
        self.result_queue = result_queue
        self.work_func = work_func
        self.stop_when_work_queue_empty = stop_when_work_queue_empty
        self.queue_timeout = queue_timeout


    def should_continue_running(self):
        if self.stop_when_work_queue_empty:
            return not self.work_queue.empty()
        else:
            return True


    def run(self):
        while self.should_continue_running():
            try:
                # grabs item from work_queue
                work_item = self.work_queue.get(timeout=self.queue_timeout)
                
                # works on item
                work_result = self.work_func(work_item)
                
                #place work_result into result_queue
                self.result_queue.put(work_result, timeout=self.queue_timeout)
                
                #signals to work_queue that item is done
                self.work_queue.task_done()
        
            except:
                logging.exception('Error in ThreadedWorker')


def start_logging_with_thread_info():
    try:
        formatter = logging.Formatter('[thread %(thread)-3s] %(message)s')
        logging.getLogger().handlers[0].setFormatter(formatter)
    except:
        logging.exception('Failed to start logging with thread info')


def stop_logging_with_thread_info():
    try:
        formatter = logging.Formatter('%(message)s')
        logging.getLogger().handlers[0].setFormatter(formatter)
    except:
        logging.exception('Failed to stop logging with thread info')


