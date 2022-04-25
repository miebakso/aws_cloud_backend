
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, text
from . import models, schemas



### Role CRUD

def get_role(db: Session, role_id: int):
    return db.query(schemas.Role).filter(schemas.Role.id == role_id).first()

def create_role(db: Session, role: models.RoleCreate):
    db_role = schemas.Role(name = role.name)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

### User CRUD

def get_user(db: Session, username: str, password: str):
    return db.query(schemas.User).filter(and_(
            schemas.User.username == username,
            schemas.User.password == password
        )).first()

def create_user(db:Session, user: models.UserCreate):
    db_user = schemas.User(username=user.username, password=user.password, role_id = user.role_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


### Post CRUD

def get_posts(db: Session, popular: bool):
    sql = ''
    result = None
    if popular:
        sql = text("""
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
                L.likes DESC
        """)
    else:
        sql = text("""
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
                P.post_datetime DESC
        """)
    return db.execute(sql)

def get_post(db: Session, post_id: int):
    sql = text(f"""
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
            P.is_active = True AND P.id = {post_id}
    """)
    return db.execute(sql).first()

def search_post(db: Session, keyword: str):
    search = "%{}%".format(keyword)
    sql = text(f"""
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
                P.is_active = True AND ( P.title LIKE '%{keyword}%' OR  P.content LIKE '%{keyword}%')
            ORDER BY
                posts.post_datetime DESC
        """)
    return db.execute(sql)

def get_user_posts(db: Session, id: int):
    sql = text(f"""
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
                P.is_active = True AND P.user_id = {id}
            ORDER BY
                posts.post_datetime DESC
        """)
    return db.execute(sql)
    # return db.query(schemas.Post).filter(schemas.Post.title.ilike(search)).all()

def get_post_likes(db: Session, post_id: int):
    return db.query(schemas.Like).filter(schemas.Like.post_id == post_id).count()

def post_liked_by_user(db: Session, post_id: int, user_id: int):
    return db.query(schemas.Like).filter(and_(schemas.Like.post_id == post_id, schemas.Like.user_id == user_id)).first()

def create_post(db: Session, post: models.PostCreate):
    db_post = schemas.Post(
        title=post.title, 
        s3_img=post.s3_img, 
        content= post.content, 
        post_datetime = post.post_datetime,
        user_id = post.user_id
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def update_post(db: Session, post_id: int, post: models.PostUpdate):
    db_post = db.query(schemas.Post).filter(schemas.Post.id == post_id).update({
        schemas.Post.title: post.title,
        schemas.Post.content: post.content,
    })
    db.commit()
    return db_post

def update_post_img(db: Session, post_id: int, s3_img: str):
    db_post = db.query(schemas.Post).filter(schemas.Post.id == post_id).update({
        schemas.Post.s3_img: s3_img,
    })
    db.commit()
    return db_post


def delete_post(db: Session, post_id: int):
    db_post = db.query(schemas.Post).filter(schemas.Post.id == post_id).update({
        schemas.Post.is_active: False
    })
    db.commit()
    db.refresh(db_post)
    return db_post

def user_like_post(db: Session, like: models.LikeCreate):
    db_like = schemas.Like(
        post_id = like.post_id,
        user_id = like.user_id
    )
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return db_like

def user_unlike_post(db: Session, like: models.LikeCreate):
    db_like = db.query(schemas.Like).filter(and_(schemas.Like.post_id == like.post_id, schemas.Like.user_id == like.user_id)).first()
    db.delete(db_like)
    db.commit()
    return {"delete": "success"}

def get_comment(db: Session, post_id: int):
    sql = text(f"""
        SELECT
            comments.id,
            comments.message,
            comments.msg_datetime,
            comments.user_id,
            users.username
        FROM comments, users 
        WHERE
            comments.user_id = users.id
            AND comments.post_id = {post_id}
        ORDER BY
            comments.msg_datetime DESC
    """)
    return db.execute(sql).all()

def post_comment(db: Session, comment: models.CommentCreate):
    db_comment = schemas.Comment(
        message=comment.message, 
        user_id=comment.user_id, 
        post_id= comment.post_id, 
        msg_datetime = comment.msg_datetime,
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


