
/*
Collections -> Sequence -> Map, Sequence, Set, etc

Sequences:
- List = Immutable. Linear/Recursive structure (linked list)
- Array = Mutable. Indexed/Flat structure.

*/

// ARRAYS
// ============================
// Defining
val top_thing: List[String] = List("a", "b", "c")


val TOP_MARKETS: Array[String] = Array(
      "LHR-JFK",
      "LHR-EWR",
      "JFK-LHR",
      "EWR-LHR",
      "EWR-CDG",
      "LHR-LAX",
      "LAX-JFK",
      "LAX-EWR",
      "JFK-LAX",
      "SFO-LAX",
      "LAX-SFO",
      "LGA-MIA",
      "ATL-EWR",
      "OAK-LAS"
    )


// access members using parens, 0-indexed:
println("Top market is: " + TOP_MARKETS(0))


// list comprehension
// in this example we use a UDF from:
import com.tvlp.cco.util.Utils.QueryHelpers._

val pos_list_short: Array[String] = Array("US", "IN", "CA")
val new_arr: Array[Long] = for (pos <- pos_list_short) yield stringToLongNum(pos)

// array objects are mutable
val arr = Array("hello", "new", "world")
arr(2) = "person"

scala> arr.foreach(println)
hello
new
person


// Appending, concatenating

/*
Array's are fixed-length (though elements are mutable)
ArrayBuffer's are variable-length. Choose this if the size of your Seq needs to change
*/

var DERIVED_COLS = ArrayBuffer.empty[String]
// appending a single element
DERIVED_COLS :+= "market"
// appending an array
DERIVED_COLS ++= Array("pcc", "gds")
println(DERIVED_COLS) // market, pcc, gds


// LISTS
// ============================
// immutable sequences.
  // any method that might imply mutation returns a new list object

// concatentaion
  val oneTwo = List(1, 2)
  val threeFour = List(3, 4)
  /// `:::` is concat operand
  val oneTwoThreeFour = oneTwo ::: threeFour

// `::` = "cons". prepend new element, return new List obj
val twoThree = List(2,3)
val oneTwoThree = 1 :: twoThree
  // note here `::` is a method of the right operand
  // any method that ends in a colon operates on the right operand