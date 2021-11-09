select id, backd, hornd, mouthd, taild, class, price, timestamp
FROM sales
WHERE sales.timestamp >= '2021-11-7' AND backd = 'back-bidens' AND hornd = 'horn-cactus' AND mouthd = 'mouth-zigzag' AND taild = 'tail-hot-butt' AND breedcount >= 1
order by timestamp desc;