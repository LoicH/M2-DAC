

connect bdwa22/bdwa22@ora11


@etu-synonym



-- requete R0

--set autotrace trace explain
set autotrace off

set sqlbl on
set timing off
set linesize 100

define D = '01-01-1993'


select *
from lineitem
;

select
	l_linestatus,
	l_returnflag,
	sum(l_quantity) as nb_articles,
	sum(l_extendedprice) ,
	sum(l_extendedprice*(1-l_discount)),
	sum(l_extendedprice*(1-l_discount)*(1+l_tax)) as prix_final,
	avg(l_quantity),
	avg(l_extendedprice),
	avg(l_discount),
	count(*)	
from lineitem
where l_receiptdate <=  '01-01-1993'
group by l_linestatus, l_returnflag
;

select s_acctbal,
       s_name,
       n_name,
       p_partkey,
       p_brand,
       s_address,
       s_phone,
       ps_supplycost
from partsupp
join supplier
     on s_suppkey = ps_suppkey
join part
     on p_partkey = ps_partkey
join nation
     on n_nationkey = s_nationkey
join region
     on r_regionkey = n_regionkey
where r_name='EUROPE' and
      p_type like '%COPPER' and
      p_size=26 and
      ps_supplycost = (select min(ps_supplycost)
from partsupp
join supplier
     on s_suppkey = ps_suppkey
join part
     on p_partkey = ps_partkey
join nation
     on n_nationkey = s_nationkey
join region
     on r_regionkey = n_regionkey
where r_name='EUROPE' and
      p_type like '%COPPER' and
      p_size=26)
order by s_acctbal desc
;

--C1
select
	l_partkey,
	o_custkey,
	o_orderdate,
	sum(l_extendedprice) as total
from lineitem, orders
where l_orderkey = o_orderkey
group by cube(l_partkey,o_custkey,o_orderdate);

/* Question 1)
a)
- Slice pour jour > 1/6/98
- Remonter dans dimension produit : rollup
- Slice sur dimension produit (*type*)
- Enlever dimension : proj aggreg sur (produit, client)
*/
select
	l_partkey,
	o_custkey,
	--o_orderdate,
	sum(l_extendedprice) as total
from lineitem, orders,part
where l_orderkey = o_orderkey
and p_partkey = l_partkey
and o_orderdate >= to_date('01/06/1998', 'DD/MM/YYYY')
and p_type like '%COPPER'
group by cube( l_partkey,o_custkey); --peut-être enlever 'cube'


--question 2, T2R
select
	p_type,
	c_name,
	n_name,
	r_name,
	sum(l_extendedprice) as total
from lineitem, orders,part, customer, nation, region
where l_orderkey = o_orderkey
and p_partkey = l_partkey
and c_custkey = o_custkey
and n_nationkey = c_nationkey
and r_regionkey = n_regionkey
and o_orderdate >= to_date('01/06/1998', 'DD/MM/YYYY')
and p_type like '%COPPER'
GROUP BY ROLLUP (p_type,r_name,n_name,c_name);

--question 2, T2U
-- Toutes les infos
select
	p_type,
	c_name,
	n_name,
	r_name,
	sum(l_extendedprice) as total
from lineitem, orders,part, customer, nation, region
where l_orderkey = o_orderkey
and p_partkey = l_partkey
and c_custkey = o_custkey
and n_nationkey = c_nationkey
and r_regionkey = n_regionkey
and o_orderdate >= to_date('01/06/1998', 'DD/MM/YYYY')
and p_type like '%COPPER'
GROUP BY (p_type,r_name,n_name,c_name)
UNION
select -- On enlève le nom du client
	p_type,
	'NULL' as c_name,
	n_name,
	r_name,
	sum(l_extendedprice) as total
from lineitem, orders,part, customer, nation, region
where l_orderkey = o_orderkey
and p_partkey = l_partkey
and c_custkey = o_custkey
and n_nationkey = c_nationkey
and r_regionkey = n_regionkey
and o_orderdate >= to_date('01/06/1998', 'DD/MM/YYYY')
and p_type like '%COPPER'
GROUP BY (p_type,r_name,n_name)
UNION
select  p_type, --on enlève le nom du pays
	'NULL' as c_name,
	'NULL' as n_name,
	r_name,
	sum(l_extendedprice) as total
from lineitem, orders,part, customer, nation, region
where l_orderkey = o_orderkey
and p_partkey = l_partkey
and c_custkey = o_custkey
and n_nationkey = c_nationkey
and r_regionkey = n_regionkey
and o_orderdate >= to_date('01/06/1998', 'DD/MM/YYYY')
and p_type like '%COPPER'
GROUP BY (p_type,r_name);


-- Question 3) Requête T3
(select p_type,
       r_name,
       extract(year from o_orderdate) as annee,
       sum(l_extendedprice) as total
from lineitem, orders,part, customer, nation, region
where l_orderkey = o_orderkey
and p_partkey = l_partkey
and c_custkey = o_custkey
and n_nationkey = c_nationkey
and r_regionkey = n_regionkey
and o_orderdate > to_date('01/06/1998', 'DD/MM/YYYY')
and p_type like '%COPPER'
group by cube(p_type, r_name, extract(year from o_orderdate));

--question : alias ?


-- Q3) Ventes en Afrique, sans cube :
select sum(l_extendedprice) as total
from lineitem, orders,part, customer, nation, region
where l_orderkey = o_orderkey
and p_partkey = l_partkey
and c_custkey = o_custkey
and n_nationkey = c_nationkey
and r_regionkey = n_regionkey
and r_name = 'AFRICA';

-- Q3) Ventes en Afrique avec cube :

select *
from (select p_type,
       r_name,
       extract(year from o_orderdate) as annee,
       sum(l_extendedprice) as total
from lineitem, orders,part, customer, nation, region
where l_orderkey = o_orderkey
and p_partkey = l_partkey
and c_custkey = o_custkey
and n_nationkey = c_nationkey
and r_regionkey = n_regionkey
and r_name = 'AFRICA'
group by cube(p_type, r_name, extract(year from o_orderdate)))
where r_name = 'AFRICA'
and annee  IS NULL
and p_ is NULL;

/* c) Si stockage de T3 dans une vue, R2 est plus rapide
   d) EZ
   e) À partir de T3 on ne peut pas retrouver des infos sur les
clients ou les pays
     (on a aggrégé par région)

   Question 4)
   a) Definir vue Date_commande (orderdate, numMois, numAnnée)
*/
with Date_commande
as
    (select distinct
    	    o_orderdate as orderdate,
    	    extract(month from o_orderdate) as numMois,
	    extract(year from o_orderdate) as numAnnee
    from orders
)
select * from Date_commande
;

/* b) Écrire T4 avec Date_commande
Avec Date_commande et la BDD TPCH on peut faire union pour avoir le cube C1
Def de C1 : (produits: nom < type, clients: nom < pays < continent,
date: jour < mois < année)
Requête juste avec TPCH pour avoir (nom produit & nom client & date (jour près))
+ union (en utilisante Date_commande) pour avoir (nom prod & nom
client & date mois)
+ union ______________________________________________________________________
année)
+ Même chose avec type produit au lieu de nom produit
+ Même chose avec pays client au lieu de nom client
+ Même chose avec continent client au lieu de pays client
+ Même chose avec type produit & pays client & (3 types de date)
+ Même chose avec type produit & continent client & (3 types de date)
(bcp de requêtes...)

*/

-- T2R :
select
	p_type,
	c_name,
	n_name,
	r_name,
	1 - grouping(c_name) as STC,
	grouping(c_name) as STP,
	grouping(n_name) as STR,
	grouping(r_name) as TM,
	sum(l_extendedprice) as total
from lineitem, orders,part, customer, nation, region
where l_orderkey = o_orderkey
and p_partkey = l_partkey
and c_custkey = o_custkey
and n_nationkey = c_nationkey
and r_regionkey = n_regionkey
and o_orderdate >= to_date('01/06/1998', 'DD/MM/YYYY')
and p_type like '%COPPER'
GROUP BY ROLLUP (p_type,r_name,n_name,c_name);

