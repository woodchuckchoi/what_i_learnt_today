from pyspark import SparkContext
from pyspark.sql import SparkSession

sc    = SparkContext()
spark = SparkSession(sc)

textDF  = spark.read.text('file:///home/jovyan/test.txt')
rdd     = textDF.rdd.flatMap(lambda x: x[0].lower().split())

rdd_group = rdd.map(lambda x: (x, 1)).groupByKey()
rdd_freq  = rdd_group.mapValues(sum).map(lambda x: (x[1], x[0])).sortByKey(False)


