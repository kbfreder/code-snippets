

// printing
println(s"Failed to load data. Reason $e")


// function
def doSomething(arg1: String, arg2: Int): Boolean = {
    // there is no "return" keyword. you simply write it
    length(arg1) == arg2
}

    // when return type might depend on something
def load_data(date: String): Option[DataFrame] = {
    val input_dir = data_dir + date // + "/*"
    if (checkIfDirExists(input_dir)) {
        val df = spark.read.parquet(input_dir + "/*")
        Some(df)
    } else {
        println(s"Path $input_dir not found")
        None
    }
}

// match case
doSomething("cat, 3") match {
  case true => println("Correct!")
  case false => println("Incorrect")
}

load_data(date) match {
    // do stuff with what the function returns
  case Success(df) => {
    df.count() 
    ...
  }
  case Failure(e) => println(s"Failed to load data. Reason $e")
}


// for loop
for (i <- 0 to days by 1) {
    var next_dt = start_dt.plusDays(i)
    ///
}


// if-else
    // this is part of a function that returns either a DataFrame or None
if (checkIfDirExists(input_dir)) {
    val df = spark.read.parquet(input_dir + "/*")
    Some(df)
} else {
    println(s"Path $input_dir not found")
    None
}
