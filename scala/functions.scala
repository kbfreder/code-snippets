

// function literal
(x: Int, y: Int) => x + y


// FUNCTIONS
def multiplyInt(d: Int, f: Int): Int = { var result: Int = 0; result = d * f; return result}

// lambda format
val myMultiply = (d: Int, f: Int) => d * f


// vanilla 
def doSomething(arg1: String, arg2: Int): Boolean = {
  // note there is no "return" keyword. you simply write it
  length(arg1) == arg2
}

doSomething("cat, 3") match {
  case true => println("Correct!")
  case false => println("Incorrect")
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

load_data(date) match {
    // do stuff with what the function returns
  case Success(df) => {
    df.count() 
    ...
  }
  case Failure(e) => println(s"Failed to load data. Reason $e")
}