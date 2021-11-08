select backd, hornd, mouthd, taild, class, AVG(price) as avgprice, count(backd) as sales
FROM sales
WHERE sales.timestamp >= '2021-11-7'
group by backd, hornd, mouthd, taild, class
having avg(price) >= 0.11
order by sales desc;
