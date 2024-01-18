
// HDFS files in spark

// if not in a spark-shell (i.e. in a script), need to define these
  import org.apache.spark.sql.SparkSession

val spark = SparkSession.builder.appName("Count Top Markets").getOrCreate()
val sc = SparkContext.getOrCreate()

def checkIfPathExists(path: String): Boolean = {
    val conf = sc.hadoopConfiguration
    val fs = org.apache.hadoop.fs.FileSystem.get(conf)
    val p = new org.apache.hadoop.fs.Path(path)
    fs.exists(p)
}

def checkIfDirExists(path: String): Boolean = {
    val conf = sc.hadoopConfiguration
    val fs = org.apache.hadoop.fs.FileSystem.get(conf)
    val p = new org.apache.hadoop.fs.Path(path)
    fs.exists(p) && fs.getFileStatus(p).isDirectory
}