from pyspark import SparkContext as SC
from pyspark.sql import Row
from pyspark.sql import SQLContext

sc = SC()
sqlContext = SQLContext(sc)

list_p = [('John',19),('Smith',29),('Adam',35),('Henry',50)]
rdd = sc.parallelize(list_p)
ppl = rdd.map(lambda x: Row(name=x[0], age=int(x[1])))
DF_ppl = sqlContext.createDataFrame(ppl)

# DF_ppl == DataFrame
