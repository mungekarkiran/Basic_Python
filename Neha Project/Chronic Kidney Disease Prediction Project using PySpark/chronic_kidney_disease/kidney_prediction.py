import logging
from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.feature import (StringIndexer, VectorAssembler, Imputer)
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.tuning import ParamGridBuilder, CrossValidator
from pyspark.sql.functions import col, when
from pyspark.sql.types import DoubleType
import os
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/kidney_prediction.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('ChronicKidneyDiseasePrediction')

class KidneyDiseasePredictor:
    def __init__(self):
        """Initialize the Kidney Disease Predictor with Spark session"""
        try:
            self.spark = SparkSession.builder \
                .appName("ChronicKidneyDiseasePrediction") \
                .config("spark.executor.memory", "4g") \
                .config("spark.driver.memory", "4g") \
                .getOrCreate()
            # self.spark = SparkSession.builder.appName("ChronicKidneyDiseasePrediction").getOrCreate()
            
            logger.info("Spark session initialized successfully")
            
            # Create necessary directories if they don't exist
            os.makedirs('models', exist_ok=True)
            os.makedirs('logs', exist_ok=True)
            
        except Exception as e:
            logger.error(f"Failed to initialize Spark session: {str(e)}")
            raise

    def load_data(self, file_path):
        """Load data from CSV file"""
        try:
            logger.info(f"Loading data from {file_path}")
            df = self.spark.read.csv(
                file_path, 
                header=True, 
                inferSchema=True
                # na_values=["?", " ", "NA", "notpresent"]
            )
            
            # Log basic info about the dataset
            logger.info(f"Data loaded successfully. Shape: ({df.count()}, {len(df.columns)})")
            logger.info(f"Columns: {df.columns}")
            df.printSchema()
            
            return df
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise

    def preprocess_data(self, df):
        """Preprocess the raw data"""
        try:
            logger.info("Starting data preprocessing")
            
            # Convert string columns to numeric where appropriate
            for column in df.columns:
                if df.schema[column].dataType == "string":
                    # Check if column contains numeric values stored as strings
                    if column in ['age', 'bp', 'sg', 'al', 'su', 'bgr', 'bu', 
                                 'sc', 'sod', 'pot', 'hemo', 'pcv', 'wbcc', 'rbcc']:
                        df = df.withColumn(column, col(column).cast(DoubleType()))
            
            # Convert target variable to binary (0/1)
            df = df.withColumn(
                "classification",
                when(col("classification") == "ckd", 1).otherwise(0)
            )
            
            # Identify numeric and categorical columns
            numeric_cols = [col_name for col_name, dtype in df.dtypes 
                           if dtype in ['int', 'double'] and col_name != "classification"]
            categorical_cols = [col_name for col_name, dtype in df.dtypes 
                              if dtype == 'string']
            
            logger.info(f"Numeric columns: {numeric_cols}")
            logger.info(f"Categorical columns: {categorical_cols}")
            
            # Create imputers for missing values
            numeric_imputer = Imputer(
                inputCols=numeric_cols,
                outputCols=[f"{col}_imputed" for col in numeric_cols],
                strategy="mean"
            )
            
            # String indexers for categorical columns
            indexers = [
                StringIndexer(
                    inputCol=column,
                    outputCol=f"{column}_indexed",
                    handleInvalid="keep"
                ) for column in categorical_cols
            ]
            
            # Assemble all features
            all_features = [f"{col}_imputed" for col in numeric_cols] + \
                         [f"{col}_indexed" for col in categorical_cols]
            
            assembler = VectorAssembler(
                inputCols=all_features,
                outputCol="features"
            )
            
            # Create preprocessing pipeline
            preprocessing_pipeline = Pipeline(stages=[numeric_imputer] + indexers + [assembler])
            
            logger.info("Fitting preprocessing pipeline")
            preprocessor_model = preprocessing_pipeline.fit(df)
            processed_df = preprocessor_model.transform(df)
            
            # Select only needed columns
            processed_df = processed_df.select("features", "classification")
            
            logger.info("Data preprocessing completed successfully")
            return processed_df, preprocessor_model
            
        except Exception as e:
            logger.error(f"Error during data preprocessing: {str(e)}")
            raise

    def train_model(self, train_df):
        """Train the Random Forest model with cross-validation"""
        try:
            logger.info("Starting model training")
            
            # Initialize classifier
            rf = RandomForestClassifier(
                labelCol="classification",
                featuresCol="features",
                seed=42
            )
            
            # Create parameter grid
            param_grid = ParamGridBuilder() \
                .addGrid(rf.numTrees, [50, 100, 150]) \
                .addGrid(rf.maxDepth, [5, 10, 15]) \
                .build()
            
            # Create evaluator
            evaluator = BinaryClassificationEvaluator(
                labelCol="classification",
                rawPredictionCol="rawPrediction",
                metricName="areaUnderROC"
            )
            
            # Create cross-validator
            cv = CrossValidator(
                estimator=rf,
                estimatorParamMaps=param_grid,
                evaluator=evaluator,
                numFolds=5,
                seed=42
            )
            
            logger.info("Running cross-validation")
            cv_model = cv.fit(train_df)
            
            # Get best model
            best_model = cv_model.bestModel
            logger.info(f"Best model parameters: {best_model.extractParamMap()}")
            
            # Evaluate on training data
            train_predictions = best_model.transform(train_df)
            train_auc = evaluator.evaluate(train_predictions)
            logger.info(f"Training AUC: {train_auc:.4f}")
            
            logger.info("Model training completed successfully")
            return best_model
            
        except Exception as e:
            logger.error(f"Error during model training: {str(e)}")
            raise

    def save_model(self, model, preprocessor, model_dir="models"):
        """Save the trained model and preprocessor"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            model_path = f"{model_dir}/kidney_model_{timestamp}"
            
            # Save the complete pipeline (preprocessor + model)
            pipeline = Pipeline(stages=[preprocessor, model])
            pipeline.write().overwrite().save(model_path)
            
            logger.info(f"Model saved successfully at {model_path}")
            return model_path
        except Exception as e:
            logger.error(f"Error saving model: {str(e)}")
            raise

    def run(self, data_path):
        """Run the complete pipeline"""
        try:
            # Step 1: Load data
            df = self.load_data(data_path)
            
            # Step 2: Preprocess data
            processed_df, preprocessor = self.preprocess_data(df)
            
            # Step 3: Split data
            train_df, test_df = processed_df.randomSplit([0.8, 0.2], seed=42)
            logger.info(f"Train size: {train_df.count()}, Test size: {test_df.count()}")
            
            # Step 4: Train model
            model = self.train_model(train_df)
            
            # Step 5: Evaluate on test set
            evaluator = BinaryClassificationEvaluator(
                labelCol="classification",
                rawPredictionCol="rawPrediction",
                metricName="areaUnderROC"
            )
            test_predictions = model.transform(test_df)
            test_auc = evaluator.evaluate(test_predictions)
            logger.info(f"Test AUC: {test_auc:.4f}")
            
            # Step 6: Save model
            model_path = self.save_model(model, preprocessor)
            
            return model, preprocessor, test_auc
            
        except Exception as e:
            logger.error(f"Error in pipeline execution: {str(e)}")
            raise
        finally:
            self.spark.stop()
            logger.info("Spark session stopped")

if __name__ == "__main__":
    try:
        predictor = KidneyDiseasePredictor()
        model, preprocessor, auc = predictor.run("data/chronic_kidney_disease.csv")
        logger.info(f"Pipeline completed successfully with test AUC: {auc:.4f}")
    except Exception as e:
        logger.error(f"Fatal error in main execution: {str(e)}")