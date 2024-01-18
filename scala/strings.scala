

// String interpolation
// https://docs.scala-lang.org/overviews/core/string-interpolation.html

    // done by prepending `s` to any string literal
val name = "James"
println(s"Hello, $name")

    // passing in arbitrary expressions: `${expr}`
println(s"The total is ${1+1}")