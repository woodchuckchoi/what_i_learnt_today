# Database
데이터 베이스의 특징은 아래와 같다.
* 실시간 접근성: 데이터베이스는 실시간으로 서비스된다. 사용자가 데이터를 요청하면 수 초 내에 결과를 서비스한다.
* 계속적인 변화: 데이터베이스에 저장된 내용은 한 순간의 상태이지만, 데이터 값은 시간에 따라 항상 바뀐다.
* 동시 공유: 데이터베이스는 서로 다른 업무, 여러 사용자에게 동시에 공유된다.
* 내용에 따른 참조: 데이터베이스에 저장된 데이터는 물리적인 위치가 아니라 값에 따라 참조된다.

스키마는 아래와 같이 정의 할 수 있다.
* 외부 스키마: 사용자가 보게되는 정보에 대한 스키마
* 개념 스키마: 전체 데이터베이스에 대한 정의, 사용자가 다루지 않는 데이터에 대한 스키마를 포함한다. 개념 스키마에 변화가 생겨도 외부 스키마가 직접 다루는 테이블이 아니라면 외부에서 볼 때는 영향이 없다.
* 내부 스키마: 실제 데이터가 저장되는 방식(Type, Size)를 명시한 스키마. 물리적인 Type이나 Size에 변화가 생겨도 개념 스키마에 영향을 끼치지 않는다.

RDB, 관계형 데이터는 행과 열로 표현되는, 테이블형 데이터이다.\
특정 Tuple(Row)를 식별하기 위해서 키를 가지며, 이 키는 반드시 Unique해서 다른 Tuple들과 구분할 수 있어야 한다. 또 키는 Foreign Key처럼 Relation간의 관계를 맺는데도 사용된다. 키를 단일 속성으로 지정할 수 없는 경우 여러 Column을 묶어서 키로 사용할 수 있다.

Database의 필수적이 조건인 무결성을 유지하기 위해서 다음과 같은 조건이 필요하다.
* 데이터 무결성: 데이터베이스에 저장된 데이터의 일관성을 유지하는 제약
* 도메인 무결성: Relation 내의 Tuple이 각 Domain에 맞는 값만 가지는 제약
* 개체 무결성: 기본키는 NULL이 될 수 없으며, 반드시 Tuple을 구분할 수 있어야 한다.
* 참조 무결성: Foreign Key가 참조하는 / 참조받는 데이터를 삽입, 수정할 때 필요한 제약

---

# Indexing
Database에 저장된 데이터에 접근하는데에는 탐색 시간 + 회전 지연 시간 + 데이터 전송 시간이 필요하다.\
데이터가 많아지면 Query에 시간이 많이 소요되므로 Table에서 한 개 이상의 속성을 이용하여 Index를 설정한다. Binary Tree 형태로 이루어진 Index를 설정하면 검색이 빠르고 효율적으로 레코드를 관리할 수 있다. Index는 WHERE와 JOIN에서 자주 등장하는 속성일 때 효과적이다. 하지만 Table에 Index가 너무 많다면 오히려 Index 추가, 정리 등의 Overhead가 발생해서 효율이 낮아질 수 있다. 따라서 적당한 수의, 가공하지 않는 Domain을 Index로 설정하는 것이 중요하다.\
Index를 선택할 때는 위의 조건들을 이용하여 직접 선택하거나, InnoDB 등의 DB 엔진에서 제공하는 Optimizer를 사용하여 Indexing을 한다.

* In Depth: 일반적으로 B-Tree와 LSM-Tree로 인덱스를 설정한다.
Index와 Table은 서로 다른 data structure로 서로 다른 곳에 저장된다.

```
	// describe test;
	id INT AUTO INCREMENT NOT NULL PRIMARY KEY // PRIMARY KEY는 Index로 설정된다.
	name VARCHAR(10) NOT NULL 
	
	select id from test where id = 1;
	// 위의 query는 index인 id를 찾은 후, 해당 index value를 반환하므로 소요되는 시간이 적다.
	
	select name from test where id = 1;
	// 위의 query는 index인 id를 찾은 후, table을 뒤져 id = 1인 tuple의 n번째 object인 name을 찾아 반환하므로 시간이 상대적으로 오래 걸린다.
	
	select name from test where id = 1;
	// 위의 query는 db가 query를 인식하고, cache에 저장되어있는 데이터를 불러오므로 소요되는 시간이 적다.
	
	select id from test where name = 'test';
	// index가 아닌 name column을 조건절로 주었기때문에, 모든 데이터에 대해서 sequential search를 수행한다. 시간이 아주 오래 걸린다.
	
	create index INDEX NAME on TABLE(COLUMN);
	// index를 설정한다. 위의 예시에 해당하는 예는 create index test_name on test(name);이다. DB는 내부적으로 b tree(default)를 사용한다.
	
	select id, name from test where name = 'new test';
	// index가 없는 table보다 훨씬 더 빠른 속도를 보인다. 하지만 int형 unique인 PRIMARY KEY id를 조건절로 주는 query보다는 느리다. 또한 일반적으로 PRIMARY KEY는 다른 index와 함께 저장되는 경우가 많으므로, id와 name을 출력하는 것은 다른 column을 query하는 것보다 훨씬 더 빠를 것이다.
```
	
---

# Transaction
Transaction은 데이터를 다루는 작업의 단위로 All-or-Nothing으로 수행되어야 한다. 이는 Database의 ACID 조건을 충족하기 위함이다.
* Atomicity: Transaction에 포함된 작업은 모두 수행되거나 수행되지 않아야 한다.
* Consistency: Transaction을 수행하기 전과 후에 DB는 상태를 유지해야 한다. Transaction과 관계 없는 값에 대한 변경이 있으면 안된다.
* Isolation: 수행 중인 Transaction에 다른 Transaction이 끼어들어 값을 바꾸면 안된다.
* Durability: 수행을 마친 Transaction의 값은 영구적으로 저장되어야 한다.

Transaction의 All-or-Nothing이라는 조건을 위해서 Rollback을 지원하기도 한다.

---

# ORM (Object-Relation Mapping)
SQL 언어를 직접 사용하지 않도록 객체와 DB를 매칭시켜서 사용할 수 있도록 돕는 프레임워크

---

# Connection Pool
데이터베이스 커넥션 캐시를 구현한 것이다.\
보통 Minimum/Maximum Pool Size가 있어서 Maximum Pool Size에 도달하면 사용 가능 한 커넥션이 생길 때까지 기다린다. Time-out 시간 안에 사용 가능한 커넥션이 생기지 않는다면 에러를 발생시킨다.\
데이터베이스는 커넥션 풀의 커넥션들에 주기적으로 헬스 체크를 하여 커넥션이 유지되고 있는지를 확인한다.

---

# MySQL DB Engine
* InnoDB - MyISAM에서 지원하지 않는 커밋, 롤백, 복구 등 다양한 기능을 지원하지만 전체적인 속도는 MyISAM보다 느리다.
* MyISAM - ISAM을 보완한 엔진. 데이터 모델 디자인이 단순하지만 전체적인 속도는 InnoDB보다 빠르다.

---

# NOSQL
기존 SQL과 다른 스키마, 기능을 제공하는 데이터베이스. 테이블 형식으로 데이터를 저장하는 RDB와 다르게 데이터를 저장하며, 확장성이 좋기 때문에 비정형 데이터를 다루는데 널리 사용된다. 대표적으로 MongoDB, Redis가 있다.\
MongoDB의 경우 스키마가 유연한 Document(JSON과 같다)형식으로 데이터를 저장하며, Redis는 Key-Value 스토어로 값을 저장하는 In-Memory 데이터 스토어이다.

---

# Partitioning
Table에 Tuple이 많아짐에 따라 key,  index를 설정하더라도 query의 속도는 느려지게 된다.\
따라서 Table을 partition key를 기준으로 작은 query table로 분리하는 것을 partitioning이라고 한다.\
하지만 partition query를 잘못 설정할 경우, 모든 partition을 탐색하므로 오히려 시간 복잡도가 더 높아질 수 있다.

---

# RDS Engineering by H.N.
## Transaction
Collection of queries\
RDS의 규칙인 ACID를 (일부) 지켜야한다.
Atomicity - Transaction의 query는 모두 실행되거나, 모두 실행되지 않아야 한다.

	SELECT balance FROM Bank WHERE id == 'sender';
	UPDATE Bank SET balance = balance - 100 WHERE id == 'sender';
	// Error!
	UPDATE Bank SET balance = balance + 100 WHERE id == 'receiver';

위와 같은 시나리오에서 100은 누구에게도 전달되지 않고 사라진다. 따라서 Rollback을 통해서 모든 query가 실행되지 않도록 관리해야한다.

Isolation - Transaction이 다른 Transaction에 의해 영향을 받을지, 받지 않을지, 받는다면 어떤 Level(isolation level)까지 받을 것인지 설정이 필요하다. 아래와 같은 read phenomena가 발생할 수 있다.

	SELECT quantity, price FROM inventory;
	// UPDATE inventory SET price = price + 10 WHERE id == 'something'; Query run from another connection
	SELECT quantity, price FROM inventory;

위의 시나리오에서 첫번째와 두번째 SELECT는 서로 다른 값을 출력하게 된다. 이를 dirty read라고 한다.

	SELECT quantity, price FROM inventory;
	// UPDATE inventory SET price = price + 10 WHERE id == 'something'; TRANSACTION COMMITTED from another connection
	SELECT quantity, price FRoM inventory;

앞선 시나리오와 같이 서로 다른 값을 출력하게 되지만, 이번엔 transaction의 commit으로 인해 출력된 값이 valid하다는 점에 차이가 있다. 이를 Non-repeatable Read라고 한다.

	SELECT quantity, price FROM inventory;
	// INSERT INTO inventory (id, quantity, price) VALUES ('something', 5, 100); Transaction committed from another connection
	SELECT quantity, price FROM inventory;

새로운 Entry가 생겼을 때 Phantom Read라고 한다.

앞의 시나리오들을 막고, 필요에 따라 조절하기 위해서 Isolation Level이 있다. Level이 높을수록 isolation이 잘 되지만, 그만큼의 cost가 발생한다.

1. Read uncommmitted - Isolation 하지 않는다, 모든 변경은 transaction 중에 확인 가능하다.
2. Read committed - Commited된 transaction이 현재 transaction의 query에 반영된다.
3. Repeatable Read - Transaction이 시작되었을 때 Table의 상태를 Transaction의 모든 query이 기억한다. Versioning, Lock을 통해 구현한다.
4. Serializable - 모든 Transaction이 순서에 따라 실행된다.

## Consistency
* Consistency in Data
User-defined하며 primary key, foreign key 등을 사용하여 정의된다. Atomicity와 Isolation을 통해 지켜진다.

eg) IG에서 query를 통해 합산한 likes와 실제 table의 likes가 다를 수 있다.

* Consistency in Reads
어떤 transaction을 commit하면 새로운 transaction은 즉시 변경을 확인할 수 있는가?\
	RDS, NoSQL 모두 inconsistency in reads 문제를 가지고 있다. (Eventual Consistency)

eg) DB가 한 서버만 있다면, 문제가 생기지 않는다. 하지만 만약 server-replica가 구성되었을 때, server에 commit된 transaction이 바로 다음 순간에 replica로 전송된 transaction에 반영될 수 있는가?

이러한 문제를 해결하기 위해서 각 property 사이의 trade-off를 한다.

*NoSQL은 scalability를 위해서 consistency를 희생한다.*
 
## Durability
Committed Transaction은 persistent해야한다. Redis는 in-memory이므로 durable하지 않다. 

---

# Row-oriented VS Columnar
* Row-oriented
database의 tuple(각 column에 대한 데이터의 집합)을 기본 단위로 저장
하나의 block io read는 여러 row를 fetch하게 된다.
하나의 read를 하는데 더 많은 IO overhead가 발생하지만 한 row를 fetch 했을 때, 모든 column의 데이터를 가져온다.

* Columnar
database table은 각 column별로 저장
하나의 block io read는 한 column의 여러 row를 가져온다.
한 column에 대한 데이터를 fetch 할 때 상대적으로 적은 IO overhead가 발생한다.

*Example*

    SELECT first_name FROM emp WHERE ssn=666;
    # row-oriented - ssn match 할 때까지 모든 row, 모든 column의 데이터를 fetch한다.
    # columnar - ssn column query를 통해서 idx를 탐색한다. first_name의 idx번째 row를 찾는다.
    
    SELECT * FROM emp WHERE id=1;
    # row-oriented - id는 index이므로 바로 id를 찾아서 모든 column의 데이터를 제공한다.
    # columnar - 각 column에 대해서 id가 1인 데이터를 query한다.
    
    SELECT SUM(salary) FROM emp;
    # row-oriented - 모든 row의 모든 column에 대한 query를 수행하고, 그 중에서 salary만 집계한다.
    # columnar - salary column의 모든 데이터를 가져온 후 집계한다.

## Pros & Cons
* Row-based
읽기/쓰기에 optimal (OLTP)\
Inefficient Compression
Inefficient Aggregation
Efficient Queries on multiple columns

* Columnar
쓰기가 느리다 (OLAP)
Efficient Compression
Efficient Aggregation
Inefficient Queries on multiple columns

---

# Locking
일반적으로 Database에서 locking을 구현하는데는 3가지 방법이 있다.
1. Table-based Locking
Commit이나 Rollback이 발생하기 전까지 Table 전체를 Lock하는 방식이다. Read와 Write Lock이 나눠지는 경우가 대부분이다.

2. Row-based Locking
Commit이나 Rollback이 발생하기 전까지 해당 Row를 Lock하는 방식이다. Read와 Write Lock이 나눠지는 경우가 대부분이다. Deadlock이 발생하지 않도록 주의한다. (Table-based Lock은 deadlock이 발생하지 않는다.)

3. Optimistic Locking
\"Lock\"과 같은 Column을 두고 해당 Column이 0이 아닐 때는 접근 금지 등의 Logic을 통해서 Lock을 구현하는 방식이다. 한 Transaction 내에서 Lock의 설정과 Logic에 대한 Query가 동시에 발생하도록 Query를 짜야한다.

---

# Check Indexes and Partitioning Information

```
    SHOW INDEXES FROM table_name
    // Check table's index information
    
    SHOW CREATE TABLE table_name
    // Check table's partitioning information and other data
```

---

# 7 Database Paradigms
1. Key-Value: redis, memcached와 같이 key-value로 구성된 간단한, 주로 in-memory에 구성된 database. 속도가 빨라서 cache, pub/sub에 주로 사용된다.
2. Wide Column: Cassandra, HBase와 같이 key-columns로 구성된 database. Schema가 없어서 Join이 불가능하지만, scalable하여 time-series 등 write를 집중적으로 사용하는 usage에 적합하다.
3. Document: MongoDB, FireStore 등 key-value pair를 저장하는 documents를 모아서 collection을 구성하는 database. Schema가 없어서 join이 안되지만, scalable하며 relational db의 sql과 유사한 query가 가능하다. read가 빠르지만 writing, updating이 느리다.
4. Relational DB: MySQL, Postgres 등 가장 일반적인 형태의 database. Schema, ACID 등의 특징을 가지고 있다.
5. Graph: neo4j 등 data 사이의 관계를 정의하는 database. Edge를 구성하고 다른 Table과 relationship을 구성해서 관계를 표현한다. Join이 많은 engine 구현에 뛰어나다.
6. Search DB: Solr, Elastic Search 등 대용량 문서에서 특정 텍스트를 찾아내는데 특화된 DB. Document DB와 같은 구성이지만, index를 효과적으로 구성해서 대용량 데이터를 분석한다. Overhead가 높아서 일반적인 app 구성에 사용하기 어렵지만 검색, 추천 시스템 등에 효율적이다.
7. Multi Model: Fauna DB 등 여러 database paradigm을 합쳐서 만든 database. ACID를 지원하며, graphql을 통해서 query와 payload를 조작할 수 있다. 속도가 빠르고 유연하다.

---

# Partitioning's Effects on DB
Partitioning은 Partitioning Scheme이 Query에 맞게 적용되었을때, Query Performance에 영향을 준다.\
Partition은 Single Column에 적용할 수 밖에 없고 (Partitioning Key) 이를 통해서 Partition Elimination을 실행한다.\
Partition Elimination이 발생하는지, 발생했을 때 Performance에 영향을 미치는지에는 두 가지 Factor가 존재한다.

1. Partition Key - Query가 Partition Key를 반드시 포함해야 한다.
2. Granularity - Partition이 너무 크면 Data를 불러들이는데 기존과 같이 오랜 시간이 소요된다. 반면에 Partition의 크기가 너무 작으면 Manageable 하지 않다.

Partitioning은 Indexing과 거의 비슷하게 작동하지만, Partitioning이 주는 장점은 Data가 일정 크기 (250GB~)를 넘지 않을 때에는 그 장점을 거의 실감하지 못한다.

---

# Why Uber Engineering Switched from Postgres to MySQL
* Uber의 초기 Service Settings: Postgres & Python Monolithic
* 현재: MySQL(+Schemaless) & MicroService (Polyglot)

Uber가 발견한 Postgres의 문제점
* Inefficient Architecture for Writes
* Inefficient Data Replication
* Issues with Table Corruption
* Poor Replic MVCC Support (Multiversion Concurrency Control)
* Difficult Upgrade

---

# Avoid LEFT JOIN whenever possible
MySQL을 기준으로 INNER JOIN을 한다면 가장 적은 ROW를 가지고 있는 TABLE을 기준으로 JOIN이 이루어진다.\
하지만 LEFT JOIN은 가장 왼쪽의 TABLE부터 시작해서 모든 ROW에 대해서 FULL SCAN을 실시하며 순서대로 JOIN을 하게된다.\
반드시 필요한 것이 아니라면 되도록 LEFT JOIN을 사용하지 않는 것이 좋다.

---

# Query Optimisation tips
```
// Inefficient
select * from movie;

// Efficient
select id from movie;
```

```
// Inefficient
select m.title
from movie m
inner join rating r
on m.id = r.movie_id
where floor(r.value/2) = 2

// Efficient
select m.title
from movie m
inner join rating r
on m.id = r.movie_id
where r.value between 4 and 5
```

```
// Inefficient
select g.value
from rating r
inner join genre g
on r.movie_id = g.movie_id
where g.value like '%Comedy'

// Efficient
select g.value
from rating r
inner join genre g
on r.movie_id = g.movie_id
where g.value in ('Romantic Comedy', 'Comedy')
```

```
// Inefficient
select distinct m.id
from movie m
inner join genre g
on m.id = g.movie_id

// Efficient
select m.id
from movie m
where exists (select 'X' from rating r where m.id = r.movie_id)
```

```
// Inefficient
select m.id
from movie m
inner join rating r
on m.id = r.movie_id
group by id
having m.id > 1000;

// Efficient
select m.id
from mvoie m
inner join rating r
on m.id = r.movie_id
where m.id > 1000
group by id;
```

FROM에 크기가 큰 테이블을, JOIN에 작은 순서대로 테이블 배치
```
// Inefficient
select m.title
from rating r
inner join genre g
on g.movie_id = r.movie_id
inner join movie m
on m.id = r.movie_id

// Efficient
select m.title
from rating r
inner join movie m
on r.movie_id = m.id
inner join genre g
on r.movie_id = g.movie_id
```

자주 사용하는 데이터에 대해서는 전처리된 테이블을 따로 보관/관리한다.

---

# Redis being the most popular DB on AWS
Redis가 memory cache로써 더 빠른 response time을 돕지만, 기본적으로 Database의 query를 optimise하는 것이 더 효율적이다.\
또한 Kafka, RabbitMQ가 강세를 가지던 Message Broker Area에서도 Redis가 떠오르고 있다.\
DB, Message Broker, Cache는 일반적인 App이 사용하는 3가지 feature이기 때문에 Redis라는 하나의 solution으로 모든 문제를 해결할 수 있다는 점이 강점이다.\
pub, sub, rpush 등 간단한 API 역시 redis의 강점 중 하나겠지..

---

# Caching
* Spatial - Access한 데이터의 주변에 있는 데이터를 caching한다. Sequential한 데이터 접근이 예상되는 시나리오에 적합하다.
* Temporal - 주로 Access되는 데이터를 caching한다.
* Distributed - Main DataStore와 sync되도록 한다. Redis에 데이터가 없거나 expired 됐을 경우 DataStore에서 retrieve, 있을 경우 retrieve.\
Sync를 맞추기 위해 cache를 거쳐 데이터를 저장하고, 불러오는 write-through 방식과 cache에 데이터를 저장하면, cache가 이를 DataStore에 저장하고 값을 retrieve하는 write-back 방식이 있다.

---

# FROM Subquery
SQL Query를 작성할 때, FROM [TABLE] WHERE 를 작성하는 경우가 많다.\
하지만 FROM (SELECT * FROM TABLE WHERE )의 Performance가 더 높을 수 있다.\
상식적으로 생각했을 때, TABLE을 선택하고 그 중에서 조건을 선택하는 것과 조건을 선택한 TABLE을 가지고 Query를 수행하나 차이가 없을 것 같지만 이런 문제점이 있으니 주의하도록 하자.\
물론 FULL JOIN이나 LEFT JOIN을 사용하게 된다면 두번째의 Performance가 더 높게 나와야겠지만, 다른 경우에도 PERFORMANCE가 더 높게나오는 건 CPU register 문제인걸까?

---

# Hash Index vs B-tree Index
HASH function을 통해서 주소를 찾음 vs Binary Tree를 통해서 주소를 찾음

# Index Scan vs Seek
Seek uses an index to pin-point a record. Index Scan has to scan the data or index pages to find the appropriate records.

# Indexing NULL
MySQL can perform the same optimization on col_name IS NULL that it can use for col_name = constant_value. For example, MySQL can use indexes and ranges to search for NULL with IS NULL.

# Inserting big data into Database
Should use batch insert instead of looping over every single record
```
INSERT INTO Table (Columns...)
VALUES
  (Record 1 values...),
  (Record 2 values...),
  ...
  (Record n values...)
```

# Char vs Varchar

* Char = fixed length, fastest to store and retrieve, but waste storage
* Varchar = variable length string, is slower to store and retrieve, but does not waste space

# Shared-Nothing

Each node should be able to satisfy each update request in distributed-computing.

--- 

# ElasticSearch

## Inverted Index
ES에서 document를 indexing하면 ES는 document가 어떤 shard에 속해야하는지를 아래 식을 통해 계산한다.
```
shard = hash(routing) % number_of_primary_shards
```
Routing의 default값으로 ES는 document의 id를 사용한다. \_id는 ES가 부여하는 unique identifier이며 아래와 같은 방식으로 직접 설정하거나, ES가 자동으로 정해주는 값을 사용한다.

Inverted Index는 Document를 query해서 그 내용에 대한 값을 전달받는게 아닌, 미리 indexing된 내부의 내용을 조회하고 그에 맞는 document를 전달받는 방식이다.\
예를 들어 "The brown fox jumps over the lazy dog"이라는 document가 indexing 된다면 {"The", "brown", "fox", "jumps", "over", "the", "lazy", "dog"}이라는 index의 mapping(schema)를 먼저 생성하고, 입력된 document는 이 데이터를 가지고 있다라는 map을 만드는 방식이다.\
Text SearchEngine으로 적합한 방식이지만, indexing의 overhead로 데이터 입력 후 indexing이 완료되기까지 약 ~1초의 delay가 있어서 eventual consistency를 제공한다.

```
# create index with 3 shards
curl -XPUT localhost:9200/so -d `
{
  "settings" : {
    "index": {
      "number_of_shards": 3,
      "number_of_replicas": 0
    }
  }
}`

# index document
curl -XPUT localhost:9200/so/question/1 -d `
{
  "number": 123456,
  "title": "elastic search index sharding"
}

# query without routing
curl -XGET localhost:9200/so/question/_search?pretty
# 모든 shard(3개)를 탐색하고 결과를 리턴한다.

# query with correct routing
curl localhost:9200/so/question/_search?explain=true&routing=1&pretty
# routing(id)를 1로 설정해서 그에 속하는 shard에 query를 보낸다.

# query with uncorrect routing
curl localhost:9200/so/question/_search?explain=true&routing=2&pretty
# routing(id)를 2로 설정(!=1)해서 틀린 결과를 얻게 된다.
```

---

# Why Parquet?

Apache Parquet is a self-describing data format that embeds the schema or structure within the data itself. Hence, it is optimized for query performance and minimizing IO.

We often use Hadoop as a place to denormalise data from relational formats. But it becomes much easier since all the joins are worked out.

In row-based, the DB has to query every single row (and parse the data) to find matches. On the other hand, in columnar data (like Parquet) DB only has to read a few byte for each record and fetch the i'th elements if match.

```
Columnar storage format인 parquet는 row-based storage format (CSV 등)에 비해 더 나은 성능을 보인다.
Apache Parquet is built from the ground using the Google shredding and assembly algorithm.
Main-stream data solutions like Amazon Athena, RedShift, etc are built to utilise Parquet's effective encoding.
```
