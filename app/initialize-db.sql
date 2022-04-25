CREATE DATABASE IF NOT EXISTS stockforum
mysql -h stockforum.ca1viqidbj5j.us-east-1.rds.amazonaws.com -u admin -P 3306 -p

SELECT
    P.id,
    P.title,
    P.content,
    P.s3_img,
    P.post_datetime,
    P.is_active,
    P.user_id,
    P.username,
    L.likes AS n_like
FROM (
    SELECT
        posts.id,
        posts.title,
        posts.content,
        posts.s3_img,
        posts.post_datetime,
        posts.is_active,
        posts.user_id,
        users.username
    FROM posts
    JOIN users on posts.user_id = users.id
) as P
LEFT JOIN (
    SELECT
        post_id,
        count(user_id) as likes
    FROM likes
) AS L 
ON 
    L.post_id = P.id
WHERE
    P.is_active = True
ORDER BY
    L.likes DESC;