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

보조 index (secondary index)를 사용하는 경우도 일반적이다.\
RDB에서는 보통 CREATE INDEX ... 명령을 통해서 보조 index를 생성한다.\
보조 index와 primary index의 주요 차이점은 키가 고유하지 않다는 점이다.

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

### Advantages

```
Organizing by column allows for better compression, as data is more homogenous. The space savings are very noticeable at the scale of a Hadoop cluster.

I/O will be reduced as we can efficiently scan only a subset of the columns while reading the data. Better compression also reduces the bandwidth required to read the input.

As we store data of the same type in each column, we can use encodings better suited to the modern processors’ pipeline by making instruction branching more predictable.
```

### model

```
required: exactly one occurrence

optional: 0 or 1 occurrence

repeated: 0 or more occurrences
```

---

# LSM Tree (Log-Structured Merge Tree)

Key-Value 형태의 데이터를 저장할 때 좋은 성능을 보인다. (High update rates compared to retrieval rates)
일반적으로 Key-Value 형태의 데이터를 저장할 때는 B-Tree를 많이 사용하지만, disk에 저장되는 경우 B-Tree는 많은 random-access를 발생시켜 성능이 저조해진다. (disk header가 이 블럭 저 블럭 옮겨다니며 시간을 소모함)
하지만 LSM Tree는 write를 append only(sequential) 방식으로 처리하기 때문에, 더 나은 성능을 보인다.

```
Log-Structured Merge-tree (LSM-tree) is a disk-based data structure designed to provide
low-cost indexing for a file experiencing a high rate of record inserts (and deletes) over an
extended period.

The algorithm has greatly reduced disk arm
movements compared to a traditional access methods such as B-trees, and will improve costperformance in domains where disk arm costs for inserts with traditional access methods
overwhelm storage media costs. The LSM-tree approach also generalizes to operations other
than insert and delete. However, indexed finds requiring immediate response will lose I/O efficiency in some cases, so the LSM-tree is most useful in applications where index inserts are
more common than finds that retrieve the entries.
```

Motivation
```
As systems take on responsibility for more complex activities, the
duration and number of events that make up a single long-lived activity will increase to a point
where there is sometimes a need to review past transactional steps in real time to remind users
of what has been accomplished. At the same time, the total number of active events known to a
system will increase to the point where memory-resident data structures now used to keep
track of active logs are no longer feasible, notwithstanding the continuing decrease in memory
cost to be expected.
```

```
The LSM-tree uses an algorithm that defers and batches index
changes, migrating the changes out to disk in a particularly efficient way reminiscent of merge
sort. As we shall see in Section 5, the function of deferring index entry placement to an ultimate disk position is of fundamental importance, and in the general LSM-tree case there is a
cascaded series of such deferred placements. 
```

Structure
```
An LSM-tree is composed of two or more tree-like component data structures.
C0 tree resides on the memory, whilst C1 tree sits on the disk. (Frequently accessed data in C1 will also remain in memory buffers)

As each new History row is generated, a log record to recover this insert is first written to the
sequential log file in the usual way. The index entry for the History row is then inserted into
the memory resident C0 tree, after which it will in time migrate out to the C1 tree on disk; any
search for an index entry will look first in C0 and then in C1. There is a certain amount of latency (delay) before entries in the C0 tree migrate out to the disk resident C1 tree, implying a
need for recovery of index entries that don't get out to disk prior to a crash. 

... whenever the C0 tree as a result of an insert reaches a threshold size near the maximum allotted, an ongoing rolling merge process serves to delete some contiguous segment of entries from the C0 tree and merge it into the C1
tree on disk.

The C1 tree has a comparable directory structure to a B-tree, but is optimized for sequential
disk access, with nodes 100% full, and sequences of single-page nodes on each level below the
root packed together in contiguous multi-page disk blocks for efficient arm use.

Multi-page block I/O is used during the rolling
merge and for long range retrievals, while single-page nodes are used for matching indexed
finds to minimize buffering requirements


```

---

# Shortened LSM Tree

먼저, LSM Tree에는 총 0~L까지의 레벨이 존재합니다. 0번 레벨은 메모리에 위치하고, 1~L번 레벨은 디스크에 존재합니다. 0번 레벨에 위치한 buffer는 데이터가 저장되며, buffer의 크기가 가득 차면 그 때부터 한 칸씩 아래 레벨로 flush됩니다.

Buffer에 key와 value를 모두 저장할 수도 있고, value는 다른 곳에 저장하고 key와 value에 대한 포인터만 저장하는 방법도 사용할 수 있습니다. (key-value separation)

또, Size ratio T가 존재하여 각 레벨별로 사이즈가 T배씩 커집니다. 만약 T = 3이고, 0번 레벨에 최대 2개의 key-value pair가 존재할 수 있다면, 1번 레벨에는 최대 6개, 2번 레벨에는 최대 18개, …의 key-value pair들이 존재할 수 있습니다.

각각의 레벨에는 run이라 불리는 객체가 있습니다. 하나의 레벨에 여러 개의 run을 유지할 수도 있고, 하나의 run만을 유지할 수도 있습니다. 여러 개의 run을 유지하는 경우 Tiered LSM Tree, 단 하나의 run만을 유지하는 경우 Leveled LSM Tree라 하는데 여기서는 Leveled LSM Tree만을 살펴보도록 하겠습니다. (각 run 내부에는 key들이 정렬된 상태로 유지되어 있습니다.)

한 레벨의 run이 가득 찰 때마다, 해당 데이터를 아래의 레벨로 내려주는데, 이 때 run 내부에서 정렬된 상태를 유지하여야 하기 때문에 원래 아래 레벨에서 가지고 있던 데이터들과 합쳐 다시 한 번 정렬을 하게 됩니다. 이 과정에서 merge sort 방식이 들어가기 때문에, LSM Tree라는 이름이 붙게 되었습니다.

이제 key를 이용하여 저장된 데이터를 찾는 방법에 대해 알아보겠습니다. 레벨이 높아질수록 run의 크기가 커지기 때문에, 하나의 run이 disk 내의 여러 page에 거쳐있는 경우가 발생하게 됩니다.

따라서, 먼저 key가 주어졌을 때 이 key가 어떤 범위에 속해있는지(즉, 어떤 page에 들어있을 가능성이 있는지)를 판단할 수 있어야 합니다. 이를 위해 메모리에 fence pointer를 유지하여 각 page의 위치와, 해당 page에 저장된 key의 min/max값을 저장합니다. 이제 하나의 key에 대한 lookup 요청이 왔을 때, fence pointer를 binary search하여 page를 찾아낸 뒤, 해당 page를 읽어 실제로 key가 들어있는지를 확인하면 됩니다.

추가적으로, 각 레벨에 bloom filter를 유지하기도 합니다.

먼저 lookup에 대한 시간 복잡도를 확인해보겠습니다. 하나의 lookup에 대해, worst한 경우는 실제 key가 저장되어있지 않은데 lookup을 하게 되는 경우입니다. 이 경우, 모든 레벨을 다 찾아보아야 하므로 I/O는 최대 O(L)번 발생하게 됩니다.

다음은 write 연산입니다. Write의 경우 맨 처음에 메모리에 있는 buffer에 쓰이기 때문에 추가적인 I/O를 발생시키지 않지만, 이후 buffer가 가득 차며 한 레벨씩 아래로 내려갈 때 계속해서 I/O가 발생하기 때문에, 해당 I/O를 계산해야 합니다.

이에 대한 평균적인 update 비용을 Amortized하게 계산해볼 수 있습니다. 결국 모든 key들은 가장 아래의 레벨로 내려가게 되는데, 이 때까지 해당 key에 의한 update가 몇 번 발생했는지를 따져보면 쉽게 유추할 수 있습니다.

먼저 한 레벨이 내려갈 때마다 해당 key를 write를 해주어야 한다는 것을 알 수 있습니다.

둘째로 해당 level에 존재할 때, 윗 레벨이 가득 차서 compaction이 발생하면 정렬된 상태를 유지하기 위해 merge를 해준 뒤 데이터를 다시 저장해주어야 하기 때문에 추가적인 I/O가 발생합니다. 각 레벨별로 크기는 T배 차이가 나므로, 한 레벨이 존재할 때 compaction은 최대 T번 발생하게 됩니다.

따라서 최종적으로, update 비용은 O(TL/B)임을 알 수 있습니다. 여기서 B는 하나의 단위에 저장되는 key의 개수입니다.

보통 B는 T와 L에 비해 굉장히 큰 값이므로, write의 경우 그리 큰 write amplification을 발생하지 않는 것을 알 수 있습니다. 하지만, read의 경우 성능이 크게 저하될 수 있습니다.

---

# Bloom Filter

Bloom Filter 는 집합내에 특정 원소가 존재하는지 확인하는데 사용되는 자료구조입니다.
이러한 “membership test” 용도로 사용되는 자료구조들은 Bloom Filter 외에도 다양합니다. 대표적이고 널리 알려진 것으로는 Balanced Binary Search Tree (AVL, red-black tree 등) 과 해시 테이블등이 있습니다. 이 자료구조들의 특징은 100% 정확도로 membership test 를 수행할 수 있다는 것입니다.
Bloom Filter 는 이러한 정확도를 희생해서 메모리 사이즈를 최소화하는 것을 목표로 합니다.

간단한 예
```
byte[128]의 비트맵을 만든다.
A, B 해쉬 함수를 준비한다.
key가 입력되면 A, B 해쉬 함수를 통과한 값에 마킹을 한다.
어떤 키가 있는지 확인하기 위해서 A, B 해쉬 함수를 통과시켰을 때, 두 비트 모두 마킹이 되어있다면 그 키는 Maybe 존재할 수도 있다.
```

The bigger the size, the less false positives.

Size를 정하기 위해서
```
1. Choose a ballpark value for n (num of elements that have been inserted)
2. Choose a value for m (bits in filter)
3. Calculate the optimal value of k (num of hash functions)
4. Calculate the false positive error rate (1 - e ^ (-kn/m)) ^ k using previously defined values, if unacceptable, modify m, k.
```

---

# Raft shortened

```
Node는 세 가지 state를 갖는다. [Follower, Candidate, Leader]
처음 시작할 때 node 는 모두 follower 이다.
node 는 leader 로 부터 heartbeat 을 주기적으로 받는데,
이때 각 노드는 election timeout (follower 가 candidate 가 되기까지 걸리는 시간, 300ms 내)을 리셋한다.

각 노드가 election timeout 이전에 이 Vote 요청을 받으면 다시 election timeout 을 초기화 하고
먼저 요청이 온 노드에 Vote 한다. (요청을 받은 노드의 로그가 candidate보다 앞서있는 경우 Vote하지 않는다.)

그리고 Candidate 노드가 과반 이상의 Vote 를 받으면 이 노드가 Leader 노드가 된다.
이제 이 leader 는  election timeout 을 초기화 시키는 heartbeat timeout 을 다른 노드에 보낸다.

이렇게 선출된 노드는 모든 의사 결정권을 가지며 Client 와 통신하게 된다.
그리고 이 노드에 문제가 생겨 heartbit timeout 이 오지 않으면 위 동작을 반복해 새로운 리더를 뽑는다.


Log Replication

일단 leader node  가 Client 로 부터 command 를 받으면 그것을 바로 수행하지 않고,
그 command 를 log 에 적는다.
그리고 이 변경 사항을 다음 heart bit 때 다른 node 들에게 그 command 를 날려준다.
그럼 다른 node 들도 그 command 를 받고 log 에 적은 후에 log 를 적었다고 node A 에게 응답을 준다.
그럼 node A 가 응답들을 보고 과반수 이상이 command 를 log 에 적었다는 것을 확인하면,
node A 는 log 에 적어놓은 그 command 를 실제로 수행 한다. (commit)
그리고 client 에게 응답을 준다.
그 다음 다른 node 들에게 자신(leader) commit 했다고 알려준다.
그럼 다른 node 들도 log 에 적어놓은 comand 를 commit 하게 된다.


client 가 처음에 cluster 에 접근하게 되거나 leader 가 crash 되었거나 하면, 여러 node 중에 아무 node 에나 접근하게 된다. 이 때 node 는 이 client 를 무조건 reject 하고 leader 정보를 준다. 그럼 client 가 이 정보를 가지고 다시 leader 로 접근하게 된다.

원래 node 가 leader node 로 부터 AppendEntries message 를 주기적으로 받는데, 이 녀석에 leader 의 network 주소도 같이 있어서 redirect 시켜주는 것은 어렵지 않다.

```

---

# LSM Tree basics
## Structure
1. Memtable (memory)
2. SortedString Tables (storage)

## SSTables (Sorted String Tables)
```
Simplest and fastest way to write is linked-list. Just append at the end. O(1)
But to read, it takes O(n)

What if the log is sorted?
Then it can be access O(log n) using binary search
```

## Memtable
```
Instead of writing data directly to database, accumulate the data in memory and flush it when the buffer is full.
Less I/O calls (faster) at the price of additional memory
```

## Compaction
```
Worst case read time from disk: O(n log n) # n is the number of SStables
As the number of SSTables increases, the worse case read time increases.
Also, there may be multiple duplicate keys in multiple SSTables, so a compactor that runs in the background merges SSTables by removing redundant & deleted keys and creating compacted/merged SSTables
```

## Need of Bloom Filters
```
To avoid redundancy between compactions, implement Bloom filter
```

---

# Algorithms behind database

## Why log structured key-value storage?
* fast writes

```
memory: fast, expensive, byte-addressable
storage: slow, cheap, block-addressable

## Historically...
Databases would write entries in a block in memory, then write the block onto the storage
But, by doing so, there is going to be a lot more work to do. (eg indexing in B-tree)

## Now (Log-structured writes)
Databases buffer writes in memory. When it's full, persist it in storage.

fast writes, fast reads, massive data

-> LSM tree (used by modern databases)
buffer full -> sort / flush in storage -> when the a run gets too long, LSM tree sort-merges similarly sized runs and it organises them into levels of exponentially increasing capacities.

simplest way to look up is to first find if the element is in buffer, if not, look for the element using binary search from the first (smallest) run to the larger ones. -> But this will require a lot of I/Os to storage for each read.

So modern databases use something called a fence pointer to keep the min/max key in each block of every run.
Then we only have to do one binary search in memory, and one I/O in storage.
In addition to the fence pointers, modern systems also typically have a set of Bloom filters (one for each run) to see if the chosen run MIGHT have the key.

The critical point of this system is the merging frequency. The more merging, the higher the cost of a write is going to be, but at the same time, it give a better read performance.

There are two production ways to sort out this issue, tiering and leveling.

Tiering is more write-optimized (default in Cassandra), on the other hand, leveling is more read-optimized (default in RocksDB).

In tiering, only when the previous level is full, the runs are sorted / flushed onto the next level.
In leveling, as soon as a run comes in, db merges, if the merged run is big enough flush.

As the runs are not merged in tiering, the maximum number of runs is R, on the other hand, in leveling only 1.

The problem is as the db grows in size, the graph is pushed upwards, which results in worse read-write performances.

There are 3 papers that show better curves than the original LSM tree.

1. Monkey (Monkey: Optimal Navigable Key-Value Store)
As the data volume increases, increase the memory size and assign more bits to bloom filters on lower levels(?)

2. Dostoevsky
Lazy Leveling (mixed-optimized): tiering for smaller levels, leveling for the largest level 

```

---

# Set
* Set is a collection of objects need not to be in any particular order.
## Rule(s)
```
Elements should not be repeated.
```

```
Before data enters set, the data first goes through hash function(s).
In the same way bloom filters tell if duplicate keys exist, if there is no match, the input data enter the data structure.(map, array, bitmap, anything)
```

---

# Column-family DB

## Why?
```
There are 3 basic assumptions that make a column oriented database better for analytical workloads:

1. The slowest thing to do in a database is read & write from disk
2. Analytical workloads scan & write large amounts of data in a table versus OLTP which tends to read and write very small transactions 1 at a time
3. Analytical workloads tend to have a lot of repeating values for each row (dimensions such as department name or product)

Assuming the above, it makes more sense to sotre data in columns rather than rows.
What this basically does is let you greatly compress the repeating values in the columns, hence enhances the IO speed and the read performance.

The trade off here is that it takes a very long time to insert individual records into a table and even longer for updates. This is because you have to split the record into columns and then compress it into the existing table structure. Column oriented databases work best for loading data when performing a "bulk" load.
```

## Example
* In column-family db, each column has a unique identifier and properties (k-v), such as below.
```
{
  "USER":
  {
    "codinghorror": { "name": "Jeff", "blog": "http://codinghorror.com/" },
    "jonskeet": { "name": "Jon Skeet", "email": "jskeet@site.com" }
  },
  "BOOKMARK":
  {
    "codinghorror":
    {
      "http://codinghorror.com/": "My awesome blog",
      "http://unicorns.com/": "Weaponized ponies"
    },
    "jonskeet":
    {
      "http://msmvps.com/blogs/jon_skeet/": "Coding Blog",
      "http://manning.com/skeet2/": "C# in Depth, Second Edition"
    }
  }
}
```

---

# RocksDB
RocksDB is a persistent key-value store implementation library especially suited for storing data on flash drives.\
It has a Log-Structured-Merge-Database (LSM) design with flexible tradeoffs between Write-Amplification-Factor (WAF), Read-Amplification-Factor (RAF) and Space-Amplification-Factor (SAF).

## BlockBasedTable Format
```
BlockBasedTable is the default SST table format in RocksDB.

<beginning_of_file>
[data block 1]
[data block 2]
...
[data block N]
[meta block 1: filter block]                  (see section: "filter" Meta Block)
[meta block 2: index block]
[meta block 3: compression dictionary block]  (see section: "compression dictionary" Meta Block)
[meta block 4: range deletion block]          (see section: "range deletion" Meta Block)
[meta block 5: stats block]                   (see section: "properties" Meta Block)
...
[meta block K: future extended block]  (we may add more meta blocks in the future)
[metaindex block]
[Footer]                               (fixed size; starts at file_size - sizeof(Footer))
<end_of_file>

---

The file contains internal pointers, called BLockHandles, containing the following information:
offset:         varint64
size:           varint64

---

1. The sequence of key/value pairs in the file are stored in sorted order and partitioned into a sequence of data blocks. These blocks come one after another at the beginning of the file.

2. After the data blocks, we store a bunch of meta blocks. The supported meta block types are described below.

3. A metaindex block contains one entry for every meta block, where the key is the name of the meta block and the value is a BlockHandle pointing to that meta block.

4. At the very end of the file is a fixed length footer that contains the BlockHandle of the metaindex and index blocks as well as a magic number.

metaindex_handle: char[p];      // Block handle for metaindex
index_handle:     char[q];      // Block handle for index
padding:          char[40-p-q]; // zeroed bytes to make fixed length
                                // (40==2*BlockHandle::kMaxEncodedLength)
magic:            fixed64;      // 0x88e241b785f4cff7 (little-endian)

* IndexBlock
Index blocks are used to look up a data block containing the range including a lookup key. It is a binary search data structure.

* Filter Meta Block
  * Full filter - In this filter there is one filter block for the entire SST file.
  * Partitioned Filter - The full filter is partitioned into multiple blocks. A top-level index block is added to map keys to corresponding filter partitions.

* Range Deletion Meta Block
This metablock contains the range deletions in the file's key-range and seqnum-range. Range deletions cannot be inlined in the data blocks together with point data since the ranges would then not be binary searchable.

```
---

# Redis
In-memory data structure store used as database || cache || message broker\
Redis provides data structures such as strings, hashes, lists, sets, sorted sets, etc.

```
To achieve top performance, Redis works with an in-memory dataset. Depending on your use case, you can persist your data either by periodically dumping the dataset to disk or by appending each command to a disk-based log.


```

## Replication

1. When a master and a replica instances are well-connected, the master keeps the replica updated by sending a stream of commands to the replica, in order to replicate the effects on the dataset happening in the master side due to: client writes, keys expired or evicted, any other action changing the master dataset.
2. When the link between the master and the replica breaks, for network issues or because a timeout is sensed in the master or the replica, the replica reconnects and attempts to proceed with a partial resynchronization: it means that it will try to just obtain the part of the stream of commands it missed during the disconnection.
3. When a partial resynchronization is not possible, the replica will ask for a full resynchronization. This will involve a more complex process in which the master needs to create a snapshot of all its data, send it to the replica, and then continue sending the stream of commands as the dataset changes.

Every Redis master has a replication ID: it is a large pseudo random string that marks a given story of the dataset. Each master also takes an offset that increments for every byte of replication stream that it is produced to be sent to replicas, in order to update the state of the replicas with the new changes modifying the dataset.

## How Redis Replicas deal with expire on keys

Redis does not have a synchronised clock over all replicas, since it would result in race conditions and diverging data sets.\
Redis uses instead:

1. Replicas don't expire keys, instead they wait for masters to expire the keys. When a master expires a key (or evict it because of LRU), it synthesizes a DEL command which is transmitted to all the replicas.

2. However because of master-driven expire, sometimes replicas may still have in memory keys that are already logically expired, since the master was not able to provide the DEL command in time. In order to deal with that the replica uses its logical clock in order to report that a key does not exist only for read operations that don't violate the consistency of the data set (as new commands from the master will arrive). In this way replicas avoid reporting logically expired keys are still existing. In practical terms, an HTML fragments cache that uses replicas to scale will avoid returning items that are already older than the desired time to live.

3. During Lua scripts executions no key expiries are performed. As a Lua script runs, conceptually the time in the master is frozen, so that a given key will either exist or not for all the time the script runs. This prevents keys expiring in the middle of a script, and is needed in order to send the same script to the replica in a way that is guaranteed to have the same effects in the data set.

## Redis Sentinel
Redis Sentinel provides high availability for Redis. In practical terms this means that using Sentinel you can create a Redis deployment that resists without human intervention certain kinds of failures.

Redis Sentinel watches Redis master.\
When the master fails (or seems to have failed), sentinels vote to check if the master has indeed failed.\
For instance, if sentinel1 thinks master has failed, then it sends a vote to the other sentinels to check if they agree.\
The status of the master depends on the consensus (majority of the sentinels), hence the number of sentinels should always be odd.

## Simple comparison between sentinel and cluster
```
Sentinel is a kind of hot standby solution where the slaves are kept replicated and ready to be promoted at any time. However, it won't support any multi-node writes. Slaves can be configured for read operations. It's NOT true that Sentinel won't provide HA, it has all the features of a typical active-passive cluster ( though that's not the right term to use here ).

Redis cluster is more or less a distributed solution, working on top of shards. Each chunk of data is being distributed among masters and slaves nodes. A minimum replication factor of 2 ensures that you have two active shards available across master and slaves. If you know the sharding in Mongo or Elasticsearch, it will be easy to catch up.
```

---

# Multi-master vs Master-slave

## Multi-master
```
Multi Master is similar to the Master/Slave topology, with the difference that both nodes are both master and replica at the same time. This means there will be circular replication between the nodes. It is advisable to configure both servers to log the transactions from the replication thread (log-slave-updates), but ignore its own already replicated transactions (set replicate-same-server-id to 0) to prevent infinite loops in the replication. This needs to be configured even with GTID enabled.

Multi master topologies can be configured to have either a so called active/passive setup, where only one node is writable and the other node is a hot standby. Then there is the active/active setup, where both nodes are writable.

Caution is needed with active/active as both masters are writing at the same time and this could lead to conflicts, if the same dataset is being written at the same time on both nodes. Generally this is handled on application level where the application is connecting to different schemas on the two hosts to prevent conflicts. Also as two nodes are writing data and replicating data at the same time they are limited in write capacity and the replication stream could become a bottleneck.
```

## Master-slave
```
Consistency is not too difficult because each piece of data has exactly one owning master. But then what do you do if you can't see that master, some kind of postponed work is needed.
```

## Summary
```
1. Master-Slave Replication

* Pros

Analytic applications can read from the slave(s) without impacting the master
Backups of the entire database of relatively no impact on the master
Slaves can be taken offline and sync back to the master without any downtime

* Cons

In the instance of a failure, a slave has to be promoted to master to take over its place. No automatic failover
Downtime and possibly loss of data when a master fails
All writes also have to be made to the master in a master-slave design
Each additional slave add some load to the master since the binary log have to be read and data copied to each slave
Application might have to be restarted

---

2. Master-Master Replication

* Pros

Applications can read from both masters
Distributes write load across both master nodes
Simple, automatic and quick failover

* Cons

Loosely consistent
Not as simple as master-slave to configure and deploy
```

---

# Column-family vs Document

```
In "insert", to use rdbms words, Document-based is more consistent and straight foward. Note than cassandra let you achieve consistency with the notion of quorum, but that won't apply to all column-based systems and that reduce availibility. On a write-once / read-often heavy system, go for MongoDB. Also consider it if you always plan to read the whole structure of the object. A document-based system is designed to return the whole document when you get it, and is not very strong at returning parts of the whole row.

The column-based systems like Cassandra are way better than document-based in "updates". You can change the value of a column without even reading the row that contains it. The write doesn't actualy need to be done on the same server, a row may be contained on multiple files of multiple server. On huge fast-evolving data system, go for Cassandra. Also consider it if you plan to have very big chunk of data per key, and won't need to load all of them at each query. In "select", Cassandra let you load only the column you need.
```

---

# Database

## Simple DB
```
#!/bin/bash

db_set() {
  echo "$1,$2" >> database
}

db_get() {
  grep "^$1," database | sed -e "s/^$1,//" | tail -n 1
}
```
db_set을 호출할 때 마다 파일의 끝에 추가하므로 키를 갱신해도 값의 예전 버젼을 덮어쓰지 않는다.

---

많은 데이터베이스는 내부적으로 추가 전용 (append-only) 데이터 파일인 로그를 사용한다.\
반면에 db_get은 데이터베이스에 많은 레코드가 있으면 성능이 좋지 않다.\
매번 키를 찾을 때마다 db_get은 key가 있는지 확인하기 위해서 전체 데이터베이스를 fullscan 해야한다. O(n)\
이렇듯 DB에서 특정 key를 효율적으로 찾기 위해서 필요한 데이터구조가 index다.

## Index
index는 기본 데이터에서 파생된 추가 구조로 질의 성능에 영향을 준다.\
추가적인 구조의 유지보수는 쓰기 과정에서 오버헤드가 발생한다.\
쓰기의 경우 append보다는 항상 성능이 떨어진다.\
이것이 DB에서 중요한 trade-off다.\
indexing을 사용하면 읽기 속도가 향상된다. 하지만 모든 indexing은 쓰기 속도를 떨어뜨린다.

## Index in k-v
가장 간단한 indexing 방법은 바이트 오프셋이다.\
특정 k-v의 값이 시작되는 offset을 memory / disk에 저장해두고, 이를 빠르게 접근하는 방식이다.\

```
key | value | byte-offset
123 | test  | 0
123 | oi    | 8 123,"oi"\n (append)
456 | hi    | ...

해당 segment가 다 찼다면, 해당 segment를 디스크에 flush하고 새로운 segement에 append-only를 시작한다.
또한 flush한 segment에는 compaction을 수행한다.

# segment
123: test | 123: oi | 456: hi | 789: something | ... | 123: haha | 456: lol

# compacted sgement
123: haha | 456: lol | 789: something

Compaction은 세그먼트를 더 작게 만들기 때문에, 컴팩션을 수행할 때 동시에 여러 세그먼트를 병합할 수 있다.
또한 compaction과 병합은 background에서 수행되며, 수행되는 동안에는 이전 (컴팩션&병합 되지 않은) 세그먼트를 사용해 읽기와 쓰기를 정상적으로 계속 수행한다.
새로 병합한 세그먼트로 전환한 후에는 세그먼트 파일을 삭제한다.

# etc
k-v를 삭제하기 위해서는 데이터 파일에 특수한 삭제 레코드 (tombstone)을 추가한다.
Segment가 병합될 때, tombstone은 병합 과정에서 삭제된 키의 이전 값을 무시하게 한다.
Tombstoning(delete)에 사용되는 시간은 아래에 따라 결정된다.
(i) the file picking policy followed by the compaction routine.
(ii) the rate of ingestion of entries to the database.
(iii) the size ratio of the LSM-tree, and (iv) the number of levels in the tree.

DB가 재시작되면 인메모리 해시 맵은 손실된다. 모든 세그먼트를 읽고 각 세그먼트의 해시 맵을 복원할 수 있지만, resource가 많이 소요되므로, snapshot을 디스크에 저장해서 복구 속도를 높인다.

DB가 log를 추가하는 도중에 죽는다면, 체크섬을 포함해서 로그의 손상된 부분을 탐지할 수 있다.

쓰기를 strictly sequential하게 로그에 추가할 때 일반적인 구현 방법은 하나의 쓰기 스레드만 사용하는 것이다.

디스크에 해시 맵을 유지할 수 있지만, 메모리와는 다르게 좋은 성능을 기대하기 어렵다.
무작위 접근 IO가 많이 필요하며, 디스크가 가득 찼을 때 확장하는 비용이 비싸며, 해시 충돌을 위한 로직 구현이 필요하다.

해시 테이블은 범위 스캔에 효과적이지 않다.
```

# SS Table & LSM Tree
위의 해시테이블 indexing 방식을 발전시켜서 key로 정렬된 문자열 테이블을 SSTable(Sorted String Table)이라고 한다.\
이름 그대로 key가 순서대로 정렬되어 있을 뿐만 아니라, 각 key는 세그먼트 파일 내에서 한번만 나타나야한다. (Compaction은 이미 이를 보장한다.)\
SS Table은 해시테이블을 사용하는 Log Segment와 비교했을 때, 아래의 장점이 있다.

1. Segment 병합을 Merge sort를 사용해서 할 수 있다. 여러 입력 Segment에 동일한 키가 있다면 가장 최신 Segment의 값을 유지하고 오래된 Segment의 값은 버린다.
2. 파일의 특정 Key를 찾기위해서 모든 키의 index를 유지할 필요가 없다. 이전과 이후의 Key index를 안다면  수 kb는 빠르게 full scan 할 수 있다. k-v가 고정 크기라면 binary search를 통해서 빠르게 키를 검색할 수도 있다.
3. 여러 k-v 레코드를 블록으로 그룹화하고 디스크에 압축 저장할 수 있으므로 IO의 사용을 줄일 수 있다.

임의 순서로 키를 삽입하고 정렬된 순서로 해당 키를 읽어오기 위해서 저장소는 RedBlackTree와 같은 데이터 구조를 사용하는 Memtable을 가진다.\
Memtable이 임계값보다 커지면 SStable로 디스크에 저장한다. Memtable(red-black tree)가 이미 정렬되어 있기 때문에 효율적으로 수행할 수 있다. 새로운 SStable은 DB의 가장 최신 Segment가 된다. SSTable을 저장하는 동안 쓰기는 새로운 Memtable 인스턴스에 기록한다.\
읽기 요청이 들어오면 먼저 Memtable에서 키를 찾고, 그 후 최신에서 오래된 순으로 SSTable Segment를 검색한다.\
Background에서 Segment 병합, 컴팩션이 수행된다.

위 Flow의 문제는 DB가 고장나면 Memtable의 가장 최신 데이터는 손실된다는 점이다.\
이런 문제를 피하기 위해서 이전과 같이 매번 쓰기를 즉시 추가하는 분리된 Log를 디스크에 유지해야 한다.\
이 Log는 손상 후, Memtable 복원시에만 필요하기 때문에 AOF로 보관해도 괜찮다.\
Log의 정보가 입력된 Memtable을 SSTable로 디스크에 저장한 후에는 해당 Log를 버려도 괜찮다.

## Optimisation
LSM Tree를 기반으로 한 데이터베이스에서 존재하지 않는 key를 검색하는 경우 모든 segment에 대한 스캔이 이루어져야하므로 낮은 performance를 보인다.\
이런 종류의 접근을 최적화하기 위해서 저장소는 보통 Bloom Filter를 사용한다. (Bloom Filter는 True Negative를 알려주므로 이 경우에 효과적이다.)

또한 SS Table을 압축하고 병합하는 순서와 시기를 결정하는데 tier와 level compaction 전략을 사용할 수 있다.\
LevelDB, RocksDB는 Level, HBase는 Tier, Cassandra는 모두 지원한다.\
Level Compaction은 이전 Level이 Upper Limit에 도달했을 때,  SSTables를 병합하여 다음 Level로 넘기는 방식이다.\
Write에 대한 overhead가 적지만, Read Overhead가 높고 Disk Storage를 상대적으로 많이 사용하게 된다.\
이와 반대로 Tier Compaction의 경우 각 Level에서 Indexing을 한다. 이전 Level이 Upper Limit에 도달하면, Indexing된 각 구간을 다음 Level의 동일 구간과 병합한다.\
Read의 overhead가 적고 Disk Storage를 적게 사용하지만, Write시에 구간 설정이 필요하며, 병합시에 더 많은 Disk IO가 발생할 수 있다.

일반적으로 B트리가 LSM트리보다 구현 성숙도가 더 높지만 LSM트리는 쓰기 속도가 (일반적으로) 더 빠르며, B트리는 읽기가 더 빠르다는 차이가 있다.\
LSM 트리의 읽기가 더 느린 이유는 컴팩션 단계에 있는 여러 데이터 구조와 SS테이블을 확인해야 하기 때문이다.

## LSM트리의 장점

```
B-Tree 인덱스는 모든 데이터 조각을 최소한 두 번 기록해야 한다. 쓰기 전 로그 한 번과 트리 페이지에 한 번(페이지가 분리되면 다시 기록)이다. 해당 페이지 내 몇 바이트만 바뀌어도 한 번에 전체 페이지를 기록해야 하는 오버헤드도 있다.

LSM Tree 인덱스 역시 컴팩션과 병합을 거쳐 여러 번 데이터를 다시 쓴다. 데이터베이스에 쓰기 한번이 데이터베이스 수명 동안 여러 번의 디스크 쓰기를 야기하는 것을 Write Amplification이라고 한다.
SSD는 블록 덮어쓰기 횟수가 제한되기 때문에 SSD 사용 시 Write Amplification은 특별히 주의해야한다.

쓰기가 많은 애플리케이션에서 병목은 DB의 DISK IO일 수 있다. 이 경우에 Write Amplification은 성능 비용이다. 저장소 엔진이 디스크에 기록한다면 디스크 대역폭 내에서 처리할 수 있는 IO는 줄어든다.

LSM트리는 압출률이 높다. 일반적인 B트리보다 디스크에 더 적은 파일을 생성하기 때문에, B트리에서 발생하는 파편화로 인한 남는 디스크의 공간 대한 오버헤드가 더 낮다.
```

## LSM트리의 단점

```
컴팩션 과정이 때로는 진행 중인 읽기와 쓰기의 성능에 영향을 준다.
저장소 엔진은 컴팩션을 점진적으로 수행하고, 동시 접근의 영향이 없게 수행하려 하지만, 디스크 자원의 한계가 있는만큼 컴팩션 연산이 끝날 때까지 요청이 대기해야 하는 상황이 발생하기 쉽다.
이에 따라서 LSM트리 성능 분석표의 스파이크가 발생한다.

Logging과 Memtable, Compaction이 디스크 IO Bandwidth를 공유하므로 데이터베이스의 수명이 길어질수록 Compaction에 사용되는 overhead가 늘어나서 가용 IO Bandwidth는 줄어들게 된다.

B Tree의 장점은 각 키가 index의 한 곳에만 존재한다는 점이다. 반면에 LSM트리는 같은 키의 다중 복사본이 존재할 수 있어서 사용하고자 하는 usecase에 따라 퍼포먼스의 문제가 발생할 수 있다.
```

---

## Index의 값

Index의 키는 Query가 검색하는 대상이며, 값은 다음 두 가지 중 하나이다.
1. Query의 실제 Row.
2. 다른 곳에 저장된 Row를 가리키는 Pointer.

일반적으로 Pointer를 많이 사용한다. 여러 보조 색인이 존재할 때 데이터의 중복을 피할 수 있기 때문이다.\
또한 Pointer를 사용하는 방식은 새로운 값이 이전 값보다 많은 공간을 필요로 하지 않을때 쉽게 갱신할 수 있다는 장점이 있다.\
만약 새로운 값이 많은 공간을 필요로 한다면 새로운 위치로 Row를 이동시키고, 1. 모든 Index가 새로운 위치를 바라보도록 갱신하거나, 2. Pointer가 가리키는 값을 Row가 아닌 Row가 저장된 주소를 가리키는 새로운 Pointer로 교체한다.

Index에서 Pointer를 사용해서 읽는 것은 읽기 성능에 불이익이 많기 때문에 (DISK Read IO) 어떤 상황에서는 Index 안에 바로 Index의 값을 저장하는 편이 바람직하며 이를 clustered index라고 한다.\
MySQL의 InnoDB는 PK가 언제나 clustered index, secondary indexes는 pk를 참조한다.

---

## Multi-column Index
(성, 이름)처럼 여러 column에 대한 indexing을 하는 것을 concatenated index라고 한다.\
순서에 따라 정렬되어있기 때문에, 성 혹은 (성, 이름)에 대해 Query를 할 수 있지만, 이름에 대한 Query를 할 수 없다.

다차원 Index는 한 번에 여러 column에 Query를 하는 더 일반적인 방법이며, 특히 GIS 데이터에 중요하게 사용된다.\
예를 들어 아래와 같은 Query가 있다면:
```
SELECT * FROM geo WHERE lat > 1 AND lat < 2 AND lng > 5 AND lng < 6;
```
B-Tree나 LSM-Tree의 index는 이렇게 여러 column에 대한 query에 효과적으로 응답할 수 없다.\
특정 lat 혹은 lng 범위 내의 query는 효과적으로 처리하지만, 둘 다에 대해서는 효과적이지 않은 것이다.\
한 가지 방법은 space-filling curve 등의 방법을 사용해서 여러 column에 대한 값을 한 값으로 만들어서 indexing하는 것이다.

---

## 

---

# SILK

## Intro
```
LSM claims to be effective for write-intensive workloads, but is it really true?
Actually, LSM implementations might show latency spikes that go up to ~1 second, which is much higher than non-LSM based implementations.
```

## SILK
```
Reduces the latency spikes without negative side-effects.
```

## Why spikes?
```
In LSM, there are 3 types of internal operations as well as client ops:
  1. Flushing (Memtable -> SSTable)
  2. L0 -> L1 Compaction
  3. Higher-level Compactions

Flushing: Incoming writes are written in memory (buffer), when the buffer is full, it gets flushed into the disk.
L0 -> L1 Compaction: Merges one level-0 SSTable with the existing level-1 SSTables, makes space for an L0 SSTable.
Higher-level Compaction: is GC in LSM, discards duplicates, delete values. Less urgent than L0 -> L1 compactions. Can have multiple of them in parallel.
```

## HOW
```

```
