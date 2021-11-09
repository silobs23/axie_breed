select backd,
       hornd,
       mouthd,
       taild,
       class,
       AVG(price)                                           as avgprice,
       PERCENTILE_CONT(0.5) WITHIN GROUP ( ORDER BY price ) AS medianprice,
       count(backd)                                         as sales
FROM sales
WHERE sales.timestamp >= '2021-11-8'
group by backd, hornd, mouthd, taild, class
having avg(price) >= 0.15
order by sales desc;

