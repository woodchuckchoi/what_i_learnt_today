from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import desc
---

superhero = spark.read.csv('file:///home/jovyan/superhero.csv', inferSchema=True, header=True)
superhero.filter(superhero.Gender != 'Male').filter(superhero.Gender != 'Female').show() # check potentially faulty data
superhero_race = superhero.groupBy('race').count() # racial composition # 304 heroes are of - race
superhero_race.orderBy(desc('count')).take(10) # == superhero_race.sort(superhero_race['count'].desc()).take(10)

superhero = superhero.withColumnRenamed('Eye color', 'eye_color') # space causes cancer, replace it with underscore
superhero.registerTempTable('superhero_table')
spark.sql('select distinct(eye_color) from superhero_table').show() # now it can be dealt with SQL commands

