# MIT Distributed System 2020
Thanks MIT for sharing these lectures..

## Intro
The goal of any distributed System is to achieve (some level of) parallelism, tolerate faults, overcome physical limitations and secure resources.\
Since it is always easier to build a system on one computer, rather than build a distributed system on multiple computers, one should always first try to solve his problem in a non-distributed way.\
When distributed systems fail, the patterns vary. Some pieces might stop working, whilst the others are still functional.\

Hence the challenges are...

1. concurrency
2. partial failure
3. performance

Infrastructure for distributed systems

1. Storage
2. Communication
3. Computation

weak consistency does not necessarily mean inferior, this concept is often used in building distributed systems.

MapReduce splits data and maps functions to each data partition, reduces the results.

To do: implement Key-Value Store(MapReduce)
input: file
output: num of occurences of each word

Is there a way to provide the map function at runtime?
