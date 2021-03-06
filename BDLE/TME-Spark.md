
# Exercice 1
## Question 1   

Définir la fonction maxEntiers qui retourne le plus grand des entiers 
d'une liste fournie en entrée.

````scala
def max(l: List[Int]) = l reduce((a,b) => if (a>b) a else b)
````

Définir la fonction scEntiers qui calcule la somme des carrés des entiers 
d'une liste fournie en entrée.

````scala
def scEntiers(l: List[Int]) = l map(x => x*x) reduce(_+_)
````
Définir la fonction moyEntiers qui calcule la moyenne des entiers d'une 
liste fournie en entrée.

````scala
def moyEntiers(l: List[Int]) = {
def aux(l: List[Int], sum: Int, len: Int) : Float = {
if (l.isEmpty) (sum.toFloat)/len
else aux(l.tail, (sum + l.head), (len + 1))
}
aux(l, 0, 0)
}
````

Tester au fur et à mesure ces fonctions sur listeEntiers construit 
comme suit :

````scala
val listeEntiers = List.range(1,11)
````

## Question 2   

Soit une liste chaine de caractères construite à l'aide de 
l'instruction suivante

````scala
val listeTemp = List("7,2010,04,27,75", "12,2009,01,31,78", "41,2009,03,25,95", "2,2008,04,28,76", "7,2010,02,32,91")
````
Chaque élément représente un enregistrement fictif de températures 
avec le format (station, année, mois, température, code_département).

Calculer pour l'année 2009 le maximum de ses températures.

````scala
max(listeTemp map(_.split(',')) map(_(3).toInt))
````


Idem pour la moyenne de ces température.

````scala
moyEntiers(listeTemp map(_.split(',')) map(_(3).toInt))
````

Bien entendu, il faudra faire les transformations et les conversions de 
type nécessaires!

## Question 3   

Soit une liste chaine de caractères construite à l'aide de l'instruction
 suivante

````scala
val melange = List("1233,100,3,20171010", "1224,22,4,20171009",
			 "100,lala,comedie", "22,loup,documentaire")
````
Deux types d'éléments existent : ceux de la forme 
(userID, movieID, rating, timestamp) et ceux de la forme 
(movieID, title, genre). 
Le domaine des userID est [1000, 2000] et 
celui des movieID est [0, 100].

Il est demandé de construire à partir de melange deux listes distinctes :

notes contenant les éléments de la forme 
(userID, movieID, rating, timestamp) et dont le type est 
(Int, String, Int, Int) ;
films contenant les éléments de la forme (movieID, title, genre) et 
dont le type est (Int, String, String).
## Question 4   

Soit une liste personnes contenant des tuples ayant trois attributs décrivant des personnes :

le premier attribut est le nom de la personne;
le second attribut est le type de la personne : etudiant (etu), enseignant (ens) ou inconnu (nan);
la troisième attribut est l'année d'inscription (s'il s'agit d'un étudiant) ou les années d'ancienneté pour
les enseignants.

````scala
val personnes = List(("Joe", "etu", 3), ("Lee", "etu", 4), ("Sara", "ens", 10), ("John", "ens", 5), ("Bill", "nan",20))
````
Définir une classe Etu(nom:String, annee:Int) et une classe Ens(nom:String, annee:Int)
Transformer personnes en une liste d'objets de la classe Etu ou Ens encapsulant les information des tuples
en entrée. Par exemple, le tuple (“Joe”, “etu”, 3) devra être transformé en un objet Etu(“Joe”, 3).

Attention : Les personnes de type inconnu ne doivent être dans le résultat!

Astuce : Utiliser le pattern matching


# Exercice 2 :

````scala
val data = sc.textFile("M2-DAC/BDLE/wordcount.txt")
val q1 = data map(arr => (arr.split(' '))(3).toDouble)
val q2 = q1 filter(a=>1000<a && a<1300)
val q33 = q2 filter(_%3 == 0)
val q34 = q2 filter(_%4 == 0)
val q4 = q33 map(_/10)
q4 toSet
val q5 = q33.intersection(q34)
val q6 = q33.subtract(q34)
val q8 = q2 filter(a => a%3 == 0 || a%10 == 0)
val q9 = q8 map(_.toDouble)
val q9min = q9 reduce((a,b) => if (a<b) a else b)
val q9max = q9 reduce((a,b) => if (a<b) b else a)
val q9sum = q9.fold(0)(_+_)
````
ou
````scala
val q9sum = q9 reduce(_+_)
val q9avg0 = q9.aggregate((0.0,0)) ((x,y) => (x._1 + y, x._2+1), (x,y)=>(x._1+y._1, x._2+y._2))
val q9avg = q9avg0._1/q9avg0._2
````
