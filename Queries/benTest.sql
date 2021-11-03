select backd, class, AVG(price) as avgprice, count(backd) as sales from sales
group by backd, class
order by avgprice desc