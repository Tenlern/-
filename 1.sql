SELECT gt.goods_type_id, gt.goods_type_name FROM orders o
    JOIN goods g on g.goods_id = o.goods_id
    JOIN goods_type gt on gt.goods_type_id = g.goods_type_id
GROUP BY gt.goods_type_id
ORDER BY count(gt.goods_type_id) DESC
LIMIT 1