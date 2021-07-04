# Hadoop & Spark Background
Hadoop framework is based on a simple programming model (MapReduce) and it enables a computing solution that is scalable.

As opposed to the common belief, Spark is not a modified version of Hadoop and neither is it dependent on Hadoop because Spark has its own cluster management. Hadoop is just one of the ways to implement Spark.\
Spark uses Hadoop in two ways, one is storage and second, processing. Since Spark has its own cluster management computation abilities, it uses Hadoop for storage purpose only (HDFS).\

## HDFS
```
The Hadoop Distributed File System (HDFS) is a distributed file system designed to run on commodity hardware. It has many similarities with existing distributed file systems. However, the differences from other distributed file systems are significant. HDFS is highly fault-tolerant and is designed to be deployed on low-cost hardware. HDFS provides high throughput access to application data and is suitable for applications that have large data sets. HDFS relaxes a few POSIX requirements to enable streaming access to file system data.

The way HDFS works is by having a main « NameNode » and multiple « data nodes » on a commodity hardware cluster. All the nodes are usually organized within the same physical rack in the data center. Data is then broken down into separate « blocks » that are distributed among the various data nodes for storage. Blocks are also replicated across nodes to reduce the likelihood of failure.

The NameNode is the «smart» node in the cluster. It knows exactly which data node contains which blocks and where the data nodes are located within the machine cluster. The NameNode also manages access to the files, including reads, writes, creates, deletes and replication of data blocks across different data nodes.

The NameNode operates in a “loosely coupled” way with the data nodes. This means the elements of the cluster can dynamically adapt to the real-time demand of server capacity by adding or subtracting nodes as the system sees fit.

The data nodes constantly communicate with the NameNode to see if they need complete a certain task. The constant communication ensures that the NameNode is aware of each data node’s status at all times. Since the NameNode assigns tasks to the individual datanodes, should it realize that a datanode is not functioning properly it is able to immediately re-assign that node’s task to a different node containing that same data block. Data nodes also communicate with each other so they can cooperate during normal file operations. Clearly the NameNode is critical to the whole system and should be replicated to prevent system failure.

Again, data blocks are replicated across multiple data nodes and access is managed by the NameNode. This means when a data node no longer sends a “life signal” to the NameNode, the NameNode unmaps the data note from the cluster and keeps operating with the other data nodes as if nothing had happened. When this data node comes back to life or a different (new) data node is detected, that new data node is (re-)added to the system. That is what makes HDFS resilient and self-healing. Since data blocks are replicated across several data nodes, the failure of one server will not corrupt a file. The degree of replication and the number of data nodes are adjusted when the cluster is implemented and they can be dynamically adjusted while the cluster is operating.
```

## Spark
```
Apache Spark is a lightning-fast cluster computing technology, designed for fast computation. It is based on Hadoop MapReduce and it extends the MapReduce model to efficiently use it for more types of computations, which includes interactive queries and stream processing. The main feature of Spark is its in-memory cluster computing that increases the processing speed of an application.
```

### Spark Built on Hadoop
* Standalone - Spark Standalone deployment means Spark occupies the place on top of HDFS(Hadoop Distributed File System) and space is allocated for HDFS, explicitly. Here, Spark and MapReduce will run side by side to cover all spark jobs on cluster.
* Hadoop Yarn - Hadoop Yarn deployment means, simply, spark runs on Yarn without any pre-installation or root access required. It helps to integrate Spark into Hadoop ecosystem or Hadoop stack. It allows other components to run on top of stack.
* Spark in MapReduce (SIMR) - Spark in MapReduce is used to launch spark job in addition to standalone deployment. With SIMR, user can start Spark and uses its shell without any administrative access.

---

### Spark Components
* Apache Spark Core
Spark Core is the underlying general execution engine for spark platform that all other functionality is built upon. It provides In-Memory computing and referencing datasets in external storage systems.

* Spark SQL
Spark SQL is a component on top of Spark Core that introduces a new data abstraction called SchemaRDD, which provides support for structured and semi-structured data.

* Spark Streaming
Spark Streaming leverages Spark Core's fast scheduling capability to perform streaming analytics. It ingests data in mini-batches and performs RDD (Resilient Distributed Datasets) transformations on those mini-batches of data.

* MLlib (Machine Learning Library)
MLlib is a distributed machine learning framework above Spark because of the distributed memory-based Spark architecture. It is, according to benchmarks, done by the MLlib developers against the Alternating Least Squares (ALS) implementations. Spark MLlib is nine times as fast as the Hadoop disk-based version of Apache Mahout (before Mahout gained a Spark interface).

* GraphX
GraphX is a distributed graph-processing framework on top of Spark. It provides an API for expressing graph computation that can model the user-defined graphs by using Pregel abstraction API. It also provides an optimized runtime for this abstraction.

---

Spark is written in Scala, but Python, Java, R are also supported.

```
SparkContext is the entry point to any spark functionality. When we run any Spark application, a driver program starts, which has the main function and your SparkContext gets initiated here. The driver program then runs the operations inside the executors on worker nodes.

SparkContext uses Py4J to launch a JVM and creates a JavaSparkContext. By default, PySpark has SparkContext available as ‘sc’, so creating a new SparkContext won't work.
```

```
# test pyspark app
logFile = 'file:///home/hyuck/spark/README.md'
logData = sc.textFile(logFile).cache() # keeps the assigned part of the data in memory of executor
numAs = logData.filter(lambda x: 'a' in x).count() # has the number of lines that have 'a' in them 
numBs = logData.filter(lambda x: 'b' in x).count() # has the number of lines that have 'b' in them
```

## RDD

```
RDD stands for Resilient Distributed Dataset, these are the elements that run and operate on multiple nodes to do parallel processing on a cluster. RDDs are immutable elements, which means once you create an RDD you cannot change it. RDDs are fault tolerant as well, hence in case of any failure, they recover automatically. You can apply multiple operations on these RDDs to achieve a certain task.
```

To apply operations on these RDD's there are two ways -
* Transformation - Operations that are applied on a RDD to create a new RDD. Filter, groupBy and map are the examples.
* Action - Operations that are applied on a RDD, which instructs Spark to perform computation and send the result back to the driver.

To apply any operation in PySpark, we need to create a PySpark RDD first.

```
words = sc.parallelize(
  ["scala",
   "java",
   "hadoop",
   "spark",
   "akka",
   "spark vs hadoop",
   "pyspark",
   "pyspark and spark",
   ]
)
counts = words.count() # num of the words variable
collects = words.collect() # all elements of the words variable
words.foreach(lambda x: print(x)) # map the function to all member variables
filtered = words.filter(lambda x: len(x) < 6).collect() # filter the word variable so that only the variables shorter than 6 can be filtered
words.map(lambda x: 'movie name: {}'.format(x)).collect() # puts the prefix before all the vars
words.reduce(lambda x, y: x + y) # scalajavahadoop... reduces the RDD

x = sc.parallelize([('spark', 1), ('hadoop', 2)])
y = sc.parallelize([('spark', 3), ('hadoop', 4)])

joined = x.join(y)
joined.collect() # [('spark', (1, 3)), ('hadoop', (2, 4))]

words.cache() # Persist RDD with the default storage level (MEMORY_ONLY)
words.persist().is_cached == True
```

## Broadcast & Accumulator

```
For parallel processing, Apache Spark uses shared variables. A copy of shared variable goes on each node of the cluster when the driver sends a task to the executor on the cluster, so that it can be used for performing tasks.
```

There are two types of shared variables supported by Apache Spark −

* Broadcast - Broadcast variables are used to save the copy of data across all nodes. This variable is cached on all the machines and not sent on machines with tasks.

```
Broadcast variables are read-only variables that will be cached in all the executors instead of shipping every time with the tasks. Basically, broadcast variables are used as lookups without any shuffle, as each executor will keep a local copy of it, so no network I/O overhead is involved here. Imagine you are executing a Spark Streaming application and for each input event, you have to use a lookup data set which is distributed across multiple partitions in multiple executors; so, each event will end up doing network I/O that will be a huge, costly operation for a streaming application with such frequency.

Now, the question is how big of a lookup dataset do you want to broadcast!! The answer lies in the amount of memory you are allocating for each executor. See, if we broadly look at memory management in Spark, we'll observe that Spark keeps 75% of the total memory for its own storage and execution. Out of that 75%, 50% is allocated for storage purposes, and the other 50% is allocated for execution purposes.

Spark stores broadcast variables in this memory region, along with cached data. There is a catch here. This is the initial Spark memory orientation. If Spark execution memory grows big with time, it will start evicting objects from a storage region, and as broadcast variables get stored with MEMORY_AND_DISK persistence level, there is a possibility that it also gets evicted from memory. So, you could potentially end up doing disk I/O, which is again a costly operation in terms of performance.
```

## Then what is the difference between cache and broadcast
```
cache() or persist() allows a dataset to be used across operations.

When you persist an RDD, each node stores any partitions of it that it computes in memory and reuses them in other actions on that dataset (or datasets derived from it). This allows future actions to be much faster (often by more than 10x). Caching is a key tool for iterative algorithms and fast interactive use.

Each persisted RDD can be stored using a different storage level, allowing you, for example, to persist the dataset on disk, persist it in memory but as serialized Java objects (to save space), replicate it across nodes, or store it off-heap

Broadcast variables allow the programmer to keep a read-only variable cached on each machine rather than shipping a copy of it with tasks. They can be used, for example, to give every node a copy of a large input dataset in an efficient manner. Spark also attempts to distribute broadcast variables using efficient broadcast algorithms to reduce communication cost.
```

```
words = sc.broadcast(['scala', 'java', 'hadoop', 'spark', 'akka'])
data = words.value
print(data) # ['scala', 'java', 'hadoop', 'spark', 'akka']
```

* Accumulator - Accumulator variables are used for aggregating the information through associative and commutative operations. For example, you can use an accumulator for a sum operation or counters (in MapReduce).


```
num = sc.accumulator(0)
def f(x):
  global num
  num += x

rdd = sc.parallelize([2, 3, 4, 5])
rdd.foreach(f)
print(num.value) # 14
```

parallelize() splits a collection into partitions (>= 1). Each partition lives on an executor which processes it. On the other hand, broadcast copies&sends the parameter to each executor.

## Storage Level

StorageLevel decides how RDD should be stored. In Apache Spark, StorageLevel decides whether RDD should be stored in the memory or should it be stored over the disk, or both. It also decides whether to serialize RDD and whether to replicate RDD partitions.

```
class pyspark.StorageLevel(useDisk, useMemory, useOffHeap, deserialized, replication = 1)

DISK_ONLY = StorageLevel(True, False, False, False, 1)

DISK_ONLY_2 = StorageLevel(True, False, False, False, 2)

MEMORY_AND_DISK = StorageLevel(True, True, False, False, 1)

MEMORY_AND_DISK_2 = StorageLevel(True, True, False, False, 2)

MEMORY_AND_DISK_SER = StorageLevel(True, True, False, False, 1)

MEMORY_AND_DISK_SER_2 = StorageLevel(True, True, False, False, 2)

MEMORY_ONLY = StorageLevel(False, True, False, False, 1)

MEMORY_ONLY_2 = StorageLevel(False, True, False, False, 2)

MEMORY_ONLY_SER = StorageLevel(False, True, False, False, 1)

MEMORY_ONLY_SER_2 = StorageLevel(False, True, False, False, 2)

OFF_HEAP = StorageLevel(True, True, True, False, 1)
```

## RDD vs DataFrame vs DataSet

---

* RDD – RDD is a distributed collection of data elements spread across many machines in the cluster. RDDs are a set of Java or Scala objects representing data. (RDD is a distributed collection of data elements without any schema)

No in-built optimization engine for RDDs. Developers need to write the optimized code themselves.

No in-built optimization engine for RDDs. Developers need to write the optimized code themselves.

RDD is slower than both Dataframes and Datasets to perform simple operations like grouping the data.

---

* DataFrame – A DataFrame is a distributed collection of data organized into named columns. It is conceptually equal to a table in a relational database. (It is also the distributed collection organized into the named columns)

It is also the distributed collection organized into the named columns

It uses a catalyst optimizer for optimization.

It provides an easy API to perform aggregation operations. It performs aggregation faster than both RDDs and Datasets.

---

* DataSet – It is an extension of DataFrame API that provides the functionality of – type-safe, object-oriented programming interface of the RDD API and performance benefits of the Catalyst query optimizer and off heap storage mechanism of a DataFrame API. (It is an extension of Dataframes with more features like type-safety and object-oriented interface.) (PySpark doesn't support this feature)

It also uses a catalyst optimizer for optimization purposes.

It will also automatically find out the schema of the dataset by using the SQL Engine.

Dataset is faster than RDDs but a bit slower than Dataframes.

---

## ETC

One of the key distinctions between RDDs and other data structures is that processing is delayed until the result is requested. This is similar to a Python generator. Developers in the Python ecosystem typically use the term lazy evaluation to explain this behavior.

---

collect() (or count(), etc..) requests the results to be evaluated (lazy evaluation) and collected to a single cluster node. If the dataset is too big, it will not work.

---

SparkContext (sc) is an entry point to any spark functionality is what we call SparkContext. While it comes to PySpark, SparkContext uses Py4J(library) in order to launch a JVM. In this way, it creates a JavaSparkContext.

---

Computation in RDD is automatically parallelized across the cluster.

---

# Streaming

## Checkpoints

Checkpoint works similar to Checkpoints which stores the state of the systems the same as in the games. Where, in this case, Checkpoints helps in reducing the loss of resources and make the system more resilient to system breakdown. A checkpoint methodology is a better way to keep track of and save the states of the system so that at the time of recovery, it can be easily pulled back.

## Broadcast Variables

Instead of providing the complete copy of tasks to the network Nodes, it always catches a read-only variable which is responsible for acknowledging the nodes of different task present and thus reducing transfer and computation cost by individual nodes. So it can provide a significant input set more efficiently. It also uses advanced algorithms to distribute the broadcast variable to different nodes in the network; thus, the communication cost is reduced.

## Accumulators

Accumulators are variables which can be customized for different purposes. But there also exist already defined Accumulators like counter and sum Accumulators. There is also tracking Accumulators that keeps track of each node, and some extra features can also be added into it. Numeric Accumulators support many digital functions which are also supported by Spark. A custom-defined Accumulators can also be created demanded by the user.

## DStream

DStream means Discretized Stream. Spark Streaming offers the necessary abstraction, which is called Discretized Stream (DStream). DStream is a data which streams continuously. From a source of data, DStream is received. It may also be obtained from a stream of processed data. Transformation of input stream generates processed data stream.

After a specified interval, data is contained in an RDD. Endless series of RDDs represents a DStream.

## Caching

Developers can use DStream to cache the stream’s data in memory. This is useful if the data is computed multiple times in the DStream. It can be achieved by using the persist() method on a DStream.

Duplication of data is done to ensure the safety of having a resilient system that can resist and failure in the system thus having an ability to tolerate faults in the system (such as Kafka, Sockets, Flume etc.)

## Output Modes

* Append Mode: In this mode, Spark will output only newly processed rows since the last trigger.
* Update Mode: In this mode, Spark will output only updated rows since the last trigger. If we are not using aggregation on streaming data (meaning previous records can’t be updated) then it will behave similarly to append mode.
* Complete Mode: In this mode, Spark will output all the rows it has processed so far.


## How does Spark Streaming work?
The data in the stream is divided into small batches which are called DStreams in the Spark Streaming. It is a sequence of RDDs internally. The data that flows in the stream is processed within a time frame. This time frame is to be specified by the developer, and it is to be allowed by Spark Streaming. The time window is the time frame within which the work should be completed. The time window is updated within a time interval which is also known as the sliding interval in the window. 

---

# Airflow On K8S VS Airflow K8S Executor
## Airflow On K8S
기존에 프로세스로 작동되는 Scheduler, Webserver, Executor (worker)를 K8S pod으로 생성한다.\
구성이 간단하기 때문에, 큰 K8S 클러스터를 가지고 있는 회사의 경우 각 조직에게 각각 Airflow를 배정해서 사용할 수 있다.\
하지만 인스턴스에서 동작하던 프로세스를 POD으로 수정한게 전부이기 때문에, 자원 소요 및 관리 포인트 역시 그대로 유지된다.\
또한 워커 및 스케쥴러 POD에서 사용되는 컨테이너가 유즈케이스가 많아질수록 유지 보수가 어려워진다는 점이 있다.

## Airflow K8S Executor
Airflow K8S Executor를 사용하는 경우 K8S Operator는 각각의 task에 worker pod을 생성하고, 이 worker pod이 해당 task를 실행하게 된다. 만약 Operator가 KubernetesPodOperator라면 K8S Executor는 worker pod으로부터 또 다른 POD을 생성하고, 생성된 새로운 pod 안에서 task를 수행하게 된다.

각각의 worker가 사용할 image를 설정하기 쉽고, 관리 측면에서 Airflow ON K8S보다 용이하다는 장점이 있다.\
하지만 K8S Executor에 대한 reference가 상대적으로 적다.

---

# Data Discovery
Data의 pattern을 찾기위해서 사용되는 프로세스로 Raw Data로부터 BI 관련 데이터를 추출하고, 제공하는 Google의 Data Catalog, Analytics를 생각하면 편리하다.\
Lyft에서 개발한 Amundsen 역시 Data Discovery 용도로 사용되는 Open-Source 툴이다.

## Without it
```
Work is given
Trying to find data source -- need to get permission, connection...
Trying to understand the data schema -- increase db loads

According to Lyft, data scientists spend up to 1/3 of their work time in data discovery:
  What data we have
  Where the data is
  How to use it
  ...
```

## Data Discovery Answers 3 Questions
```
1. Search Based
  Where is the table, dash board for data x? What data does it contain?
  -> Does this analysis already exist?

2. Lineage Based
  I make modification on data, who owns the data and who uses the data the most?
  -> I need to notify anybody related to this data table/stream.

3. Network Based
  I want to follow a power user (a senior / manager) in my team.
  -> i want to bookmark some tables and get notified when changes are made.
```

---

# Fields of Interest in Data Engineering
1. Programming - Mostly to write ETL scripts (python, scala, etc...)
2. DB(SQL) - Fundamental to have a look at SQL/NoSQL data stores
3. Cloud - Many DE solutions are cloud-based
4. ETL Orchestration - Airflow, AWS Data Pipeline, etc..
5. BigData Frameworks - Hadoop, Flink, Spark, Hive, Presto....
6. Data Warehouse - RedShift, Big Query, etc...

---
