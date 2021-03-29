from pyspark.streaming.context import StreamingContext
import time

ssc = StreamingContext(sc, 1)

rddQueue = []
for _ in range(5):
    rddQueue += [sc.parallelize([j for j in range(1, 1001)], 10)]

inputStream = ssc.queueStream(rddQueue)
mappedStream = inputStream.map(lambda x: (x % 10, 1))
reduceStream = mappedStream.reduceByKey(lambda a, b: a+b)
reduceStream.pprint()

ssc.start()
time.sleep(6)
ssc.stop(stopSparkContext=True, stopGraceFully=True)
