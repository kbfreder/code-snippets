// Ref: https://www.baeldung.com/java-8-date-time-intro


// ELAPSED TIME
import java.time.{LocalDateTime, Duration}

val now = LocalDateTime.now()

// ... time elapses

val later = LocalDateTime.now()

val secs_elapsed = Duration.between(now, later).getSeconds()
val min_elapsed = secs_elapsed / 60


// DATE PARSING & INCREMENTING

import java.time.format.DateTimeFormatter
import java.time.{LocalDate, Period}


val start_dt_str = args(0)
val end_dt_str = args(1)
// string to datetime object
val start_dt = LocalDate.parse(start_dt_str)
val end_dt = LocalDate.parse(end_dt_str)
// date math
val days = Period.between(start_dt, end_dt).getDays()
for (i <- 0 to days by 1) {
    var next_dt = start_dt.plusDays(i)
    // datetime object to string
    var next_dt_str = next_dt.format(DateTimeFormatter.ofPattern("yyyyMMdd"))
    // extracting date components
    var year = next_dt.getYear
    var month = next_dt.getMonthValue
    var hdfs_path: String = f"$BASE_INPUT_DIR/year=$year/month=$month%02d/day=$next_dt_str/hour=19"
    println(hdfs_path)
}


// DATES
scala> import java.time.format.DateTimeFormatter
                                                                                                                                                                                                                                    
scala> import java.time.{LocalDate, Period}

val input_date_str = "2023-02-01"

scala> val date_dt = LocalDate.parse(date_str)
val date_dt: java.time.LocalDate = 2023-02-01

scala> date_dt.getYear
val res1: Int = 2023

scala> date_dt.getMonth
var res2: java.time.Month = FEBRUARY

scala> var month = date_dt.getMonthValue
var month: Int = 2


// SLEEPING
sleep_msec = 5000
Thread.sleep(sleep_msec)
