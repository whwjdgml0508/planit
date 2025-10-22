# Gunicorn configuration file for PlanIt

import multiprocessing

# Server socket
bind = "0.0.0.0:8000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Restart workers after this many requests, to help prevent memory leaks
max_requests = 1000
max_requests_jitter = 100

# Logging
accesslog = "/var/log/planit/gunicorn_access.log"
errorlog = "/var/log/planit/gunicorn_error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "planit_gunicorn"

# Daemon mode
daemon = False
pidfile = "/var/run/planit/gunicorn.pid"
user = "ubuntu"
group = "ubuntu"
tmp_upload_dir = None

# SSL (uncomment when SSL is configured)
# keyfile = "/etc/ssl/private/planit.key"
# certfile = "/etc/ssl/certs/planit.crt"

# Preload application for better performance
preload_app = True

# Worker timeout
graceful_timeout = 30

# Maximum number of pending connections
backlog = 2048
