select backd, hornd, mouthd, taild, class, AVG(price) as avgprice, count(backd) as sales
FROM sales
group by backd, hornd, mouthd, taild, class
having avg(price) >= 0.11
order by sales desc