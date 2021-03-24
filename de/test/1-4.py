# build a pipeline

from pyspark.ml import Pipeline
from pyspark.ml.linalg import DenseVector
from pyspark.ml.classification import LogisticRegression

## use the df_removed DF from before

CATE_FEATURE = ['workclass', 'education', 'marital-status', 'occupation', 'relationship', 'race', 'gender', 'native-country']
stages = []

for categoricalCol in CATE_FEATURE:
    stringIndexer = StringIndexer(inputCol = categoricalCol, outputCol=categoricalCol + 'Index')
    encoder = OneHotEncoder(inputCols=[stringIndexer.getOutputCol()], outputCols=[categoricalCol+'classVec'])
    stages += [stringIndexer, encoder]

assemblerInputs = [c + 'classVec' for c in CATE_FEATURE] + CONTI_FEATURES

assembler = VectorAssembler(inputCols=assemblerInputs, outputCol='features')
stages += [assembler]

pipeline = Pipeline(stages=stages)
pipelineModel = pipeline.fit(df_remove)
model = pipelineModel.transform(df_remove)

input_data = model.rdd.map(lambda x: (x['newlabel'], DenseVector(x['features'])))

df_train = sqlContext.createDataFrame(input_data, ['label', 'features'])

train_data, test_data = df_train.randomSplit([.8, .2], seed=42)

lr = LogisticRegression(labelCol='label',
                        featuresCol='features',
                        maxIter=10,
                        regParam=0.3)

linearModel = lr.fit(train_data)
predictions = linearModel.transform(test_data)

selected = predictions.select('label', 'prediction', 'probability')

# evaluate the model

cm = predictions.select('label', 'prediction')

cm.filter(cm['label'] == cm['prediction']).count() / cm.count() # 0.~~~~

