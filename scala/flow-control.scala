

// if/then
    // must enclose boolean expression in parens
    // if block only has one statement, curly brackets option
if (i != 0)
    print(" ")

    // >1 block, so must use curly brackets
if (a == b) {
    doSomething()
} else if (test2) {
    doY()
} else {
    doZ()
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


// for loop
val days = 30
for (i <- 0 to days by 1) {
    // note, this is end-inclusive. That is, the last value of `i` will be `days` (not days-1 as in Python)
    var next_dt = start_dt.plusDays(i)
    // ...
}

for (args <- args):
    println(arg)


// foreach + function literal (lambda function)
    // data type inferred from array
args.foreach(arg => println(arg))
    // explicitly define param data type
args.foreach((arg: String) => println(arg))
    // if function literal only takes one statement with a single arg:
args.foreach(println)

