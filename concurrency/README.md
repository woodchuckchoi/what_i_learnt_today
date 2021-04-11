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

---

# RAFT (Reliable, Replicated, Redundant, And Fault-Tolerant)

Raft offers a generic way to distribute a state machine across a cluster of computing systems, ensuring that each node in the cluster agrees upon the same series of state transitions.

Raft achieves consensus via an elcted leader. A server in a raft cluter is either a leader or a follower, and can be a candidate in the precise case of an elction (when leader unavailable). The timeout is reset on receiving the heartbeat. If no heartbeat is received the follower changes its status to candidate and starts a leader election.

Raft implements consensus by a leader approach. The cluster has one and only one elected leader which is fully responsible for managing log replication on the other servers of the cluster. It means that the leader can decide on new entries' placement and establishment of data flow between it and the other servers without consulting other servers. A leader leads until it fails or disconnects, in which case a new leader is elected.
The consensus problem is decomposed in Raft into two relatively independent subproblems listed below.

## Leader Election
When the existing leader fails or when the algorithm initialises, a new leader needs to be elected.
In this case, a new term starts in the cluster. A term is an arbitrary period of time on the server for which a new leader needs to be elected. Each term starts with a leader election. If the elction is completed successfully (a single leader is elected) the term keeps going on with normal operations orchestrated by the new leader. If the election is a failure, a new term starts, with a new election.

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
