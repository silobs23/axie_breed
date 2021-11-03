select backd, class, AVG(price) as avgprice from sales
group by backd, class
order by avgprice desc