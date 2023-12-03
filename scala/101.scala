
// VARIABLES
// =====================
// val creates an immutable variable -- cannot be reassigned
    // can be reassigned within a loop, however

val b = 4

b = 6 // throws a Type error


// var creates a mutable variable -- can be reassigned
var d = 5
var d = 6 // this is fine

// however we can't change its type
var d = "cat" // Type Mismatch error


// must use double-quotes for strings
// single quote is for char's

var string = "cat"
var letter = 'a'


// Declare default if variable is null
def aMethod(param: String = null) = { 
  val p = 
    if(param == null) {
      "asdf"
    } else {
       param
    }

  println(p) 
}


// DATA TYPES
// =====================

// scala does have type inference
val x = 3 // Scala knows this is an Int

// design decision: whether to "clutter" code with explicit type annotations

/// converting string to Int
var date_str = "20230201"
val date_int = date_str.toInt


// PRINTING
// =====================
    // with a string-formatted variable
println(s"Failed to load data. Reason $e")



// STRING FORMATTING
// =====================

// https://docs.scala-lang.org/overviews/core/string-interpolation.html
    // %s: just the string, ma'am
    // %f: format the string, e.g. %d

val savePath = s"$TMP_DIR/$date_str"


var year = 2023
var month = 1
var hdfs_path: String = f"$BASE_INPUT_DIR/year=$year/month=$month%02d/day=$next_dt_str/hour=19"




// IMPORTING
    // all subpackages
import org.apache.sql.funcions._
    // only some
import org.apache.spark.sql.types.{Long, String}
    // all except
import org.apache.sql.funcions.{col => _, _}
    // with a rename 
import java.sql.{Date => SDate}
import org.apache.sql.{funcions => F}