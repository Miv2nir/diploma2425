import multiprocessing

bind = "0.0.0.0:8000"  # Replace with your desired IP and port
#worker_class = 'gevent'
workers = 3
worker_class = "gthread"
threads = 2
timeout = 60