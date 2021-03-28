df = spark.readStream\
  .format("socket")\
  .option("host", "localhost")\
  .option("port", "9090")\
  .load()

df = spark.readStream\
        .format("kafka")\
        .option("kafka.bootstrap.servers", "192.168.1.100:9092")\
        .option("subscribe", "json_topic")\
        .option("startingOffsets", "earliest") // From starting\
        .load()\

df.selectExpr("CAST(id AS STRING) AS key", "to_json(struct(*)) AS value")\
   .writeStream\
   .format("kafka")\
   .outputMode("append")\
   .option("kafka.bootstrap.servers", "192.168.1.100:9092")\
   .option("topic", "josn_data_topic")\
   .start()\
   .awaitTermination()\
