from pyspark import SparkContext as SC
from pyspark.sql import SQLContext
from pyspark import SparkFiles
from pyspark.sql.types import *
from pyspark.ml.feature import StringIndexer, OneHotEncoder, VectorAssembler

sc = SC()
url = "https://raw.githubusercontent.com/guru99-edu/R-Programming/master/adult_data.csv"
sc.addFile(url)
sqlContext = SQLContext(sc)

# df = sqlContext.read.csv(SparkFiles.get("adult_data.csv"), header=True, inferSchema=True) # with inferSchema=False all values are considered string

df_string = sqlContext.read.csv(SparkFiles.get("adult.csv"), header=True, inferSchema=  False)

def convertColumn(df, names, newType):
    for name in names: 
        df = df.withColumn(name, df[name].cast(newType))
    return df 

CONTI_FEATURES  = ['age', 'fnlwgt','capital-gain', 'educational-num', 'capital-loss', 'hours-per-week']
df_string = convertColumn(df_string, CONTI_FEATURES, FloatType()) # schema casted 

df_string.select('age', 'fnlwgt').show(5) # shows 5 rows of selected columns

df.groupBy('education').count().sort('count', ascending=True).show() # show count of data grouped by education sorted by count ascending

df.describe().show() # show summary

df.crosstab('age', 'income').sort('age_income').show() # shows the descriptive statistics between two pairwise columns.

df.drop('education_num').columns # drop a column and return the remaining columns

df.filter(df.age > 40).count() # filters the dataframe by age

df.groupby('mariatal-status').agg({'capital-gain':'mean'}).show() # group by and compute statistics

df = df.withColumn('age-square', col('age')**2) # add a column named age-square that is the square of age

# df = df.select([...]) # can easily change the order of columns

df.filter(df['native-country'] == 'Holand-Netherlands').count() # count dutch

df.groupby('native-country').agg({'native-country': 'count'}).sort(asc('count(native-country)')).show() # show statistics that shows the count of each native-country ordered by the count asc

df_remove =df.filter(df['native-country'] != 'Holand-Netherlands') # remove dutch cases

stringIndexer = StringIndexer(inputCol='workclass', outputCol='workclass-encoded') # to one-hot-encode, transform a string column
model = stringIndexer.fit(df)
indexed = model.transform(df) # workclass transformed to workclass-encoded (float)

encoder = OneHotEncoder(dropLast=False, inputCol='workclass-encoded', outputCol='workclass-vec')
one_hot_model = encoder.fit(indexed)
encoded_df = encoded.transform(indexed)


