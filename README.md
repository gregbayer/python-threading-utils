# python-threading-utils

A set of helper classes and functions that make it easier to work with threads in Python.

* ThreadedWorker - Makes it easy to create a thread that will pull work from a syncronized work_queue and write it to a syncronized result_queue.
* start_logging_with_thread_info - Helper to add thread id to all log messages. (assumes there is a root logging handler already)
* stop_logging_with_thread_info - Helper to remove thread id from all log messages. (assumes there is a root logging handler already)

# ThreadedWorker Example

    import Queue
    
    urls_to_process = ["http://url1.com", "http://url2.com", "http://site1.com", "http://site2.com"]
    
    work_queue = Queue.Queue()
    result_queue = Queue.Queue()

    def process_url(url):
        # TODO: Do some work with the url
        return url
    
    def main():
        # spawn a pool of threads, and pass them queue instance 
        for i in range(5):
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


# Dependencies: 
* [Python threading](http://docs.python.org/library/threading.html)
* [Python Queue](http://docs.python.org/library/queue.html)


# References
* [IBM article on python threading](http://www.ibm.com/developerworks/aix/library/au-threadingpython/)
