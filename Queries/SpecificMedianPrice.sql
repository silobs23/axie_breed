select PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY price) AS MedianPrice, DATE(timestamp)
FROM (
			select id,
       				backd,
       				hornd,
       				mouthd,
				   taild,
				   class,
				   price,
				   timestamp
			FROM sales
			WHERE timestamp >= '2021-11-15'
			  AND backd = 'back-bidens'
			  AND hornd = 'horn-cactus'
			  AND mouthd = 'mouth-zigzag'
			  AND taild = 'tail-hot-butt'
			  AND breedcount = 3
			order by timestamp desc)
			AS criteria
group by DATE(timestamp)
