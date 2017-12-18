uwsgi + gevent + pymysql + dbpool:

Running 20s test @ http://127.0.0.1:8000/polls/
  4 threads and 500 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   448.05ms   58.54ms   1.10s    85.87%
    Req/Sec    95.15     31.67   250.00     68.29%
  7432 requests in 20.06s, 0.96MB read
  Socket errors: connect 0, read 9351, write 39, timeout 0
Requests/sec:    370.49
Transfer/sec:     48.84KB


