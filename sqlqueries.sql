select backd, hornd, mouthd, taild, class, avg(price) as avgprice, count(mouthd) as sales from sales
group by backd, hornd, mouthd, taild, class
having avg(price) >= 0.11
order by sales desc



