# MIT Distributed System 2020
Thanks MIT for sharing these lectures..

## Intro
The goal of any distributed System is to achieve (some level of) parallelism, tolerate faults, overcome physical limitations and secure resources.\
Since it is always easier to build a system on one computer, rather than build a distributed system on multiple computers, one should always first try to solve his problem in a non-distributed way.\
When distributed systems fail, the patterns vary. Some pieces might stop working, whilst the others are still functional.

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
* Async programmes might achieve I/O concurrency, but not CPU parallelism. The more cores there are, the more likely it is to gain advantages using concurrent techniques
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

---

# RAFT (Reliable, Replicated, Redundant, And Fault-Tolerant)

Raft offers a generic way to distribute a state machine across a cluster of computing systems, ensuring that each node in the cluster agrees upon the same series of state transitions.

Raft achieves consensus via an elcted leader. A server in a raft cluter is either a leader or a follower, and can be a candidate in the precise case of an election (when leader unavailable). The timeout is reset on receiving the heartbeat. If no heartbeat is received the follower changes its status to candidate and starts a leader election.

Raft implements consensus by a leader approach. The cluster has one and only one elected leader which is fully responsible for managing log replication on the other servers of the cluster. It means that the leader can decide on new entries' placement and establishment of data flow between it and the other servers without consulting other servers. A leader leads until it fails or disconnects, in which case a new leader is elected.
The consensus problem is decomposed in Raft into two relatively independent subproblems listed below.

## Leader Election
When the existing leader fails or when the algorithm initialises, a new leader needs to be elected.
In this case, a new term starts in the cluster. A term is an arbitrary period of time on the server for which a new leader needs to be elected. Each term starts with a leader election. If the election is completed successfully (a single leader is elected) the term keeps going on with normal operations orchestrated by the new leader. If the election is a failure, a new term starts, with a new election.

A leader election is started by a candidate server. A server becomes a candidate if it receives no communication by the leader over a period called the election timeout, so it assumes there is no acting leader anymore. It starts the election by increasing the term counter, voting for itself as new leader, and sending a message to all other servers requesting their vote. A server will vote only once per term, on a first-come-first-served basis. If a candidate receives a message from another server with a term number larger than the candidate's current term, then the candidate's election is defeated and the candidate changes into a follower and recognises the leader as legetimate. If a candidate receives a majority of votes, then it becomes the new leaer. If neither happens (eg. split vote) then a new term starts, and a new election begins.

Raft uses a randomized election timeout to ensure that split vote problems are resolved quickly. this should reduce the chance of a split vote becuase servers won't become candidates at the same time: a single server will time out, win the election, then become leader and send heartbeat messages to other servers before any of the followers can become candidates.

## Log Replication
The leader is responsible for the log replication. It accepts client requests. Each client request consists of a command to be executed by the replicated state machines in the cluster. After being appended to the leader's log as a new entry, each of the requests is forwarded to the followers as AppendEntries messages. In case of unavailability of the followers, the leader retries AppendEntries messages indefinitely, until the log entry is eventually stored by all of the followers.

Once the leader receives confirmation from the majority of its followers that the entry has been replicated, the leader spplies the entry to its local state machine, and the request is considered committed. This event also commits all previous entries in the leader's log. Once a follower learns that a log entry is commimtted, it applies the entry to its local state machine. This ensures consistency of the logs between all the servers through the cluster, ensuring that the safety rule of Log Matching is respected.

In the case of leader crash, the logs can be left inconsistent, with some logs from the old leader not being fully replicated through the cluster. The new leader will then handle inconsistency by forcing the followers to duplicate its own log. To do so, for each of its followers, the leader will compare its log with the log from the follower, find the last entry where they agree, then delete all the entries coming after this critical entry in the follower log and replace it with its own log entries. This mechanism will restore log consistency in a cluster subject to failures.

## Safety
### Safety rules in Raft
* Election safety: at most one leader can be elected in a given term.
* Leader append-only: a leader can only append new entries to its logs (it can neither overwrite nor delete entries).
* Log matching: if two logs contain an entry with the same index and term, then the logs are identical in all entries up through the given index.
* Leader completeness: if a log entry is committed in a given term then it will be present in the logs of the leaders since this term
* State machine safety: if a server has applied a particular log entry to its state machine, then no other server may apply a different command for the same log.

### State Machine Safety
This rule is ensured by a simple restriction: a candidate can't win an election unless its log contains all committed entries. In order to be elected, a candidate has to contact a majority of the cluster, and given the rules for logs to be committed, it means that every committed entry is going to be present on at least one of the servers the candidates contact.

Raft determines which of two logs (carried by two distinct servers) is more up-to-date by comparing the index term of the last entries in the logs. If the logs have a last entry with different terms, then the log with the later term is more up-to-date. If the logs end with the same term, then whichever log is longer is more up-to-date.

In Raft, the request from a candidate to a voter includes information about the candidate's log. If its own log is more up-to-date than the candidate's log, the voter denies its vote to the candidate. This implementation ensures the State Machine Safety rule.

### Follower Crashes
If a follower crashes, AppendEntries and vote requests sent by other servers will fail. Such failures are handled by the servers trying indefinitely to reach the downed follower. If the follower restarts, the pending requests will complete. If the request has already been taken into account before the failure, the restarted follower will just ignore it.

### Timing and Availability
Timing is critical in Raft to elect and maintain a steady leader over time, in order to have a perfect availability of the cluster. Stability is ensured by respecting the timing requirement of the algorithm; broadcastTime << electionTimeout << MTBF

* broadcastTime is the average time it takes a server to send request to every server in the cluster and receive responses. It is relative to the infrastructure used.
* MTBF (Mean Time Between Failures) is the average time between failures for a server. It is also relative to the infrastructure.
* electionTimeout is the same as described in the Leader Election section. It is something the programmer must choose.

Typical number for these values can be 0.5 ms to 20 ms for broadcastTime, which implies that the programmer sets the electionTimeout somewhere between 10 ms and 500 ms. It can take several weeks or months between single server failures, which means the values are sufficient for a stable cluster.

---

# How to do distributed locking

```
Redlock(redis-lock)
Redis is a good fit if the situation is 
1. share some transient, approximate, fast-changing data between servers
2. it's not a big deal if you occasionally lose the data for some reason
For example, a good use case is maintaining request counters per IP address (for rate limiting purposes) and sets of distinct IP addresses per user ID (for abuse detection).
```

```
The purpose of a lock is to ensure that amongst several nodes that might try to do the same piece of work, only one actually does it.
At higher level, there are two reasons one might want a lock in a distributed application: for efficiency and correctness
```

```
Making the lock safe with fencing
The fix for this problem is actually pretty simple: you need to include a fencing token with every write request to the storage service. In this context, a fencing token is simply a number that increases (e.g. incremented by the lock service) every time a client acquires the lock.
```

---

# Master-Master VS Master-Slave Clustering

## Master-Master
```
All nodes are masters and replicas of each other at the same time (circular replication)
It is recommended to configure the masters to log the transactions from the replication thread, but ignores its own already-replicated transactions to prevent infinite replication loops.

Pros
1. Masters can be distributed across multiple physical sites. (like CDN)
2. Fault-tolerant

Cons
1. Complex system
2. Data will be loosely consistent due to multi-master replication
3. May cause conflicts as the number of nodes grows (or network latency grows)
```

## Master-Slave
```
Master controls writes data (and reads, if needed) and slaves asynchronously copies the log, hence are able to handle read requests.

Pros
1. Fast (no additional overhead)
2. Easy to keep data consistency, Requests can be split between master(write) and slave(read)

Cons
1. if master fails, some data might not be available in slaves
2. Hard to scale write requests.
3. Failover process is manual in most cases.
```

## Multi-Master
Multi master is a synchronous cluster of databases, whilst master-master replicates asynchronously in the background.\
When a request is received by any master, it relays the request to the other masters, and find out the latest result then responds.\
it is reliable, automatically restores from failure and read requests can be fast, scaled efficiently.\
However, due to the consensus (relay, collect, respond) larege performance overhead is inevitable.

## CAP theorem
It is impossible for a distributed data store to simultaneously provide more than two out of the following three guarantees:
* Consistency: Every read receives the most recent write or an error
* Availability: Every request receives a (non-error) response, without the guarantee that it contains the most recent write.
* Partition Tolerance: The system continues to operate despite an arbitrary number of messages being dropped (or delayed) by the network between nodes.

When a network partition failure happens should we decide to:
1. Cancel the operation and thus decrease the availability but ensure consistency
2. Proceed with the operation and thus provide availability but risk inconsistency

"two out of three" concept can be somewhat misleading because system designers only need to sacrifice consistency or availability

---

# Deadlocks

## Phantom Deadlock
* Phantom Deadlock
```
The resource release messages arrive later than the resource request messages for some specific resources. The deadlock detection algorithm treats the situation as a deadlock and may abort some processes to break the deadlock. But in actual, no deadlocks were present, the deadlock detection algorithms detected the deadlock based on outdated messages from the processes due to communication delays. Such a deadlock is called Phantom Deadlock.
```

* Solution
```
A solution to this problem is to introduce a coordinator to which each server forwards it's wait-for graph, the idea here is that the coordinator will be able to produce a wait-for graph for the entire system and can therefore make a decision about which process/transaction should be aborted to resolve the deadlock.
```

---
