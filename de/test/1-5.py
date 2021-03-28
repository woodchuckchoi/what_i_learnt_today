from pyspark import SparkContext
from pyspark.sql import SparkSession

sc = SparkContext()
spark = SparkSession(sc)

data = [('James','','Smith','1991-04-01','M',3000),
  ('Michael','Rose','','2000-05-19','M',4000),
  ('Robert','','Williams','1978-09-05','M',4000),
  ('Maria','Anne','Jones','1967-12-01','F',4000),
  ('Jen','Mary','Brown','1980-02-17','F',-1)
]
columns = ["firstname","middlename","lastname","dob","gender","salary"]

df = spark.createDataFrame(data, columns)
df.createOrReplaceTempView('PERSON_DATA') # create a temp sql table named 'PERSON_DATA' from df
df2 = spark.sql("SELECT * FROM PERSON_DATA")
groupDF = spark.sql("SELECT gender, count(*) FROM PERSON_DATA GROUP BY gender')

# Spark df can be modified with SQL like above
