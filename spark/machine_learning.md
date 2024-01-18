from pyspark.ml.feature import (
    Normalizer, StandardScaler, OneHotEncoderEstimator,
    VectorAssembler, VectorIndexer
)
from pyspark.ml.regression import (
    LinearRegression, DecisionTreeRegressor
)
from pyspark.ml.evaluation import RegressionEvaluator


# LinearRegression
- elasticNetParam corresponds to α
    - α is the ratio / mixing param
- regParam corresponds to λ
    - λ is the regularization factor

"elasticNetParam = Param(parent='undefined', name='elasticNetParam', doc='the ElasticNet mixing parameter, in range [0, 1]. For alpha = 0, the penalty is an L2 penalty. For alpha = 1, it is an L1 penalty.')"

regression_model = LinearRegression(
    #  
    labelCol="fare",
    maxIter=20,
    # will need to tune these
    regParam=0.1,
    elasticNetParam=0.5
)

## RegressionEvaluator
"metricName",
    """metric name in evaluation - one of:
    rmse - root mean squared error (default)
    mse - mean squared error
    r2 - r^2 metric
    mae - mean absolute error.""",


# Retrieving best params from CrossValidator

```python
cv_results = list(zip(
    cv_model.getEstimatorParamMaps(), 
    cv_model.avgMetrics
))

cv_results.sort(key=lambda x: x[1])
best_result = cv_results[0]
best_metric = best_result[1]
best_param_dict = best_result[0]
params = [x.name for x in list(best_param_dict.keys())]
param_vals = best_param_dict.values()
best_params = dict(z    ip(params, param_vals))
```

# VectorAssembled features in spark --> pandas / sklearn
in the format expected by sklearn

tx_assembler = VectorAssembler(
    inputCols= [
        <output from other transformation steps>
    ],
    outputCol='features'
)

tx_pipeline = Pipeline(stages=[
    scale_assembler,
    norm_assembler,
    ohe, 
    scaler,
    normer,
    tx_assembler
])

tx_model = tx_pipeline.fit(train)
train_tx = tx_model.transform(train)
test_tx = tx_model.transform(test)

train_pdf = train_tx.select(key_cols + [target_col + 'features']).toPandas()

y_train = train_pdf[target_col]

**HERE**
<!-- I tried combining the following two steps, but could never get the shape or data type right -->
x_train_s = train_pdf['features'].apply(lambda x: x.toArray())
X_train = [e.astype(np.float64) for e in x_train_s]

