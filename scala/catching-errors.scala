// Ref: https://docs.scala-lang.org/overviews/scala-book/functional-error-handling.html
// adapted to load a spark data frame if directory path exists

// needed for either option
import org.apache.spark.sql.{DataFrame, SparkSession}

// these aren't needed if running in spark-shell
val spark = SparkSession.builder.appName("Count Top Markets").getOrCreate()
val sc = SparkContext.getOrCreate()
import spark.implicits._

val data_dir = "/data/estreaming/midt_1_5/"

// ======================================================
// OPTION 1: Optional, Some, None

def checkIfDirExists(path: String): Boolean = {
  val conf = sc.hadoopConfiguration
  val fs = org.apache.hadoop.fs.FileSystem.get(conf)
  val p = new org.apache.hadoop.fs.Path(path)
  fs.exists(p) && fs.getFileStatus(p).isDirectory
}

def load_data(date: String): Option[DataFrame] = {
    val input_dir = data_dir + date 
    if (checkIfDirExists(input_dir)) {
        val df = spark.read.parquet(input_dir + "/*")
        Some(df)
    } else {
        println(s"Path $input_dir not found")
        None
    }
}

load_data(date) match {
    case Some(df: DataFrame) => {
        // do Stuff with df, e.g.:
        df2 = df.withColumnRenamed(...)
    }
    case None => {
        println("Skipping this day")
    }
}

// ======================================================
// OPTION 2: Try, Success, Failure
import scala.util.{Try, Success, Failure}

def load_data(date: String): Try[DataFrame] = Try {
  val input_dir = data_dir + date + "/*"
  val df = spark.read.parquet(input_dir)
  df
}

load_data(date) match {
    case Success(df) => {
        // do stuff with df
        df.count()
    }
    case Failure(e) => {
        println(s"Failed to load data. Reason: $e")
    }

