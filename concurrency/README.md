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

# Lecture 2 RPC and Threads
Thread is the main tool to manage concurrency. In this class, Go will be the main language of choice, since it has goroutine, which is the simplified light-weight implementation of thread in Go, and the language is straight-forward, garbage collected.

Different threads hold different stacks, still, since the threads from one process can access each others' stacks, if they knew the address.

Thread is implemented to...

1. To achieve I/O concurrency (calling some other functions somewhere else, and whilst waiting run some other bits of code)
2. To achieve parallelism (up to the number of cores in your machine, your threads will run truly in parallel)
3. For convenience (do some arbitrary tasks periodically)

Asynchronous(event-driven) <-> Concurrency
* Async system only has one thread of control and it keeps activities in a table with the status
* It is often easier to write concurrent programmes using threads than async programmes
* Async programmes might not achieve I/O concurrency. The more cores there are, the more likely it is to gain advantages using concurrent techniques
* Async is cheaper(lighter) than thread

Differences between threads and processes
* OS creates a big box that is a process, within that box, more than one thread can exist.

Always keep in mind to avoid race conditions.

Coordination
* Channels
* Condition Variables
* Wait Groups

Replication
1. State Transfer
Somehow stores the state of a machine (contents of the ram) in another
2. Replicate State Machine
When external events intervene store the events

Replicate State Machine Implementation Points
1. What events to store? Not all bits of memory -> some level of application state
2. How closely (quick) replication takes place (synchronisation lag)
3. Cut-over
4. Anomalies
5. New replicas

Non-deterministic events may happen?
Input packet data and the timing of interruption should match (state)

resp is held by the primary until the replica acknowledges the req
network error between master and worker -> appealing outside authority to decide which of (primary/backup) should survive

---

Raft only allows servers with up-to-date logs to become leaders, whereas Paxos allows any server to be leader provided it then updates its log to ensure it is up-to-date.
Raft's approach is surprisingly efficient given its simplicity as, unlike Paxos, it does not require log entries to be exchanged during leader election. 
