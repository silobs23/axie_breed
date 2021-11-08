select backd, hornd, mouthd, taild, class,
       AVG(price) as avgprice, PERCENTILE_CONT(0.5) WITHIN GROUP ( ORDER BY price ) AS medianprice,
       count(backd) as sales
FROM sales
WHERE sales.timestamp >= '2021-11-6' AND backd = 'back-garish-worm'
group by backd, hornd, mouthd, taild, class
having avg(price) >= 0.11
order by sales desc;