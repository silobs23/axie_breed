select backd, hornd, mouthd, taild, class, AVG(price) as avgprice, count(backd) as sales from sales
group by backd, hornd, mouthd, taild, class
order by avgprice desc