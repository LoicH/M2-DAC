### Question 1

Write a function to compute the max of an integer list.


```scala
val listInt = List(1, 3, 4, 2, 9, 5, 0, 6, 7, 8)

def max(l: List[Int]): Int = l reduce((a, b) => if (a>b) a else b)

max(listInt)
```

Write a function that computes the sum of squares of an int list


```scala
def sumSquares(l: List[Int]): Int = l map(x => x*x) reduce(_ + _)

sumSquares(listInt)
```

Write a function that computes the mean of an int list


```scala
def mean(l: List[Int]): Float = {
    def aux(l: List[Int], sum: Int, len: Int): Float =
        l match {
            case h::t => aux(t, sum+h, len+1)
            case Nil => (sum.toFloat)/len
        }
    aux(l, 0, 0)
}

mean(listInt)
```

### Question 2

Given a list of strings with the format "location,year,month,temperature,zipcode", compute the max and mean of 2009 temperatures.


```scala
val listTemp = List("7,2010,04,27,75", "12,2009,01,31,78", "41,2009,03,25,95", "2,2008,04,28,76", "7,2010,02,32,91")

val filterRecords = listTemp map(_.split(',')) filter(_(1) == "2009") map(_(3).toInt)

val maxTemp = max(filterRecords)

val meanTemp = mean(filterRecords)
```

### Question 3

Given a list of strings that contains two kinds of elements:
- "userID,movieID,rating,timestamp"
- "movieID,title,genre"

Construct two different lists:
- `ratings` that contains (userID: Int, movieID: Int, rating: Int, timestamp: Int)
- `movies` that contains (movieID: Int, title: String, genre: String)


```scala
val scrambled = List("1233,100,3,20171010", "1224,22,4,20171009",
                     "100,buddies,comedy", "22,wolves,documentary")

var (r, m) = scrambled map(_.split(',')) partition(_.length == 4)

val ratings = r map(s => (s(0).toInt, s(1).toInt, s(2).toInt, s(3).toInt))

val movies = m map(s => (s(0).toInt, s(1), s(2)))
```

 ### Question 4

Given `people`, a list of triplets describing people, each triplet is `(name, type, year)` where
- `type` is "stu" for students, "tea" for teachers, or "nan".
- `year` is the year of registration for students, or the number of years of seniority for teachers.


- Define classes  `Student(name: String, registration: Int)` and `Teacher(name: String, seniority: Int)`
- Transform `people` into a list of `Student` and `Teacher` objects. Don't include type `nan`.



```scala
val people = List(("Joe", "stu", 3), ("Lee", "stu", 4), ("Sara", "tea", 10), ("John", "tea", 5), ("Bill", "nan",20))

case class Student(name: String, registration: Int)
case class Teacher(name: String, seniority: Int)

people map(x => x._2 match {
    case "stu" => Some(Student(x._1, x._3))
    case "tea" => Some(Teacher(x._1, x._3))
    case "nan" => None
}) flatten
```
