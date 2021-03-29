from pyspark import SparkContext
from pyspark.streaming.context import StreamingContext

sc = SparkContext()
ssc= StreamingContext(sc, 1) # specify batchDuration, in this case, all data accumulated within 1 second window is going into one batch

rddData = [sc.parallelize([i]) for i in range(1000)] # stream is a sequence of RDDs

inSteram = ssc.queueStream(rddData)
filter1 = inStream.filter(lambda x: x % 2 == 0)
filter2 = filter1.filter(lambda x: x % 3 == 0)
collected = filter2
collected.pprint()

ssc.start() # triggers stream to run until ssc.stop() is run
# > 0
# >
# >
# >
# >
# >
# > 6
# >
# >
# >
# > ... any multiples of 6...
ssc.stop()
