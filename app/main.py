from fastapi import Depends, FastAPI, HTTPException, UploadFile, Form, File
from fastapi.middleware.cors import CORSMiddleware
from app.settings.database import Database
from . import CRUD, models, schemas
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import boto3
import boto3.session




app = FastAPI()
db = Database()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

session = boto3.session.Session()
s3 = session.resource('s3',
    aws_access_key_id=db.access_key,
    aws_secret_access_key=db.secret_key,
    aws_session_token = db.session_token
)



@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/role/create")
async def create_role(role: models.RoleCreate, db: Session = Depends(db.get_db)):
    return CRUD.create_role(db, role)

@app.get("/role/{role_id}", response_model=models.Role)
async def get_role(role_id: int, db: Session = Depends(db.get_db)):
    response = CRUD.get_role(db, role_id)
    return response

@app.post("/login", response_model=models.User)
async def login(user: models.Login, db: Session = Depends(db.get_db)):
    user_retrieve =  CRUD.get_user(db, user.username, user.password)

    if user_retrieve is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    usr = models.User
    role = CRUD.get_role(db, user_retrieve.role_id)
    usr.id = user_retrieve.id
    usr.username = user_retrieve.username
    usr.role_id = role.id
    usr.name = role.name
    return usr

@app.post("/register")
async def register(user: models.Login, db: Session = Depends(db.get_db)):
    f_user = models.UserCreate
    f_user.username = user.username
    f_user.password = user.password
    f_user.role_id = 2
    return CRUD.create_user(db, f_user)


@app.get("/posts")
async def get_posts(popular:bool = False, db: Session = Depends(db.get_db)):
    posts = CRUD.get_posts(db, popular)
    results = []
    for post in posts:
        p = {}
        p['id'] = post.id
        p['title'] = post.title
        p['s3_img'] =  post.s3_img
        p['content'] = post.content
        p['post_datetime'] =  post.post_datetime
        p['is_active'] = post.is_active
        p['n_like'] = post.n_like
        p['username'] = post.username
        p['user_id'] = post.user_id
        if p['n_like'] is None:
            p['n_like'] = 0
        results.append(p)
    return results

@app.get("/user/posts/{user_id}")
async def user_post(user_id:int, db: Session = Depends(db.get_db)):
    posts = CRUD.get_user_posts(db, user_id)
    results = []
    for post in posts:
        p = {}
        p['id'] = post.id
        p['title'] = post.title
        p['s3_img'] =  post.s3_img
        p['content'] = post.content
        p['post_datetime'] =  post.post_datetime
        p['is_active'] = post.is_active
        p['n_like'] = post.n_like
        p['username'] = post.username
        p['user_id'] = post.user_id
        if p['n_like'] is None:
            p['n_like'] = 0
        results.append(p)
    return results


@app.get("/post/{post_id}", response_model=models.PostComment)
async def get_post(post_id: int, db: Session = Depends(db.get_db)):
    post =  CRUD.get_post(db, post_id)
    comments = CRUD.get_comment(db, post_id)
    post_comment = models.PostComment
    post_comment.id = post.id
    post_comment.title = post.title
    post_comment.s3_img = post.s3_img
    post_comment.content =  post.content
    post_comment.post_datetime =  post.post_datetime
    post_comment.is_active =  post.is_active
    post_comment.n_like =  post.n_like
    post_comment.user_id = post.user_id

    if post_comment.n_like == None:
        post_comment.n_like = 0
    result = []
    for i in range(0,len(comments)):
        comment = comments[i]
        com = {}
        com['id'] = comment[0]
        com['message'] = comment[1]
        com['msg_datetime'] = comment[2]
        com['user_id'] = comment[3]
        com['username'] = comment[4]
        result.append(com)
    post_comment.comments = result
    return post_comment

@app.post("/post/create")
async def create_post(title: str = Form(...), file: UploadFile = File(...), content: str = Form(...), user_id: int =Form(...), dbb: Session = Depends(db.get_db)):
    print("asdasdasasdasdasdasd")
    file_name = file.filename
    bucket = s3.Bucket(db.bucket_name)
    bucket.upload_fileobj(file.file, file_name)
    url = f"https://{db.bucket_name}.s3.amazonaws.com/{file_name}"
    post_final = models.PostCreate
    post_final.title = title
    post_final.s3_img = url
    post_final.content = content
    post_final.user_id = user_id
    post_final.post_datetime = datetime.now()
    posts =  CRUD.create_post(dbb, post_final)
    return models.SUCCESS

@app.post("/post/update")
async def update_post(title: str = Form(...), file: Optional[UploadFile] = File(None), post_id: int =  Form(...), content: str = Form(...), dbb: Session = Depends(db.get_db)):
    post_final = models.PostUpdate
    post_final.title = title
    post_final.content = content
    posts =  CRUD.update_post(dbb, post_id, post_final)
    if file is not None:
        file_name = file.filename
        bucket = s3.Bucket(db.bucket_name)
        bucket.upload_fileobj(file.file, file.filename, ExtraArgs={'ACL': "public-read", 'ContentType': 'image/jpeg'})
        url = f"https://{db.bucket_name}.s3.amazonaws.com/{file_name}"
        s3_img = url
        CRUD.update_post_img(dbb, post_id, s3_img)
    return models.SUCCESS

@app.get("/user/has/like")
async def has_like(post_id: int, user_id:int, dbb: Session = Depends(db.get_db)):
    has_like =  CRUD.post_liked_by_user(db, post_id, user_id)
    if len(has_like) == 1:
        return True
    return False



@app.get("/search")
async def search_posts(keyword: str, db: Session = Depends(db.get_db)):
    posts = CRUD.search_post(db, keyword=keyword)
    results = []
    for post in posts:
        p = {}
        p['id'] = post.id
        p['title'] = post.title
        p['s3_img'] =  post.s3_img
        p['content'] = post.content
        p['post_datetime'] =  post.post_datetime
        p['is_active'] = post.is_active
        p['n_like'] = post.n_like
        p['user_id'] = post.user_id
        p['username'] = post.username
        if p['n_like'] is None:
            p['n_like'] = 0
        results.append(p)
    return results 

@app.post("/post/delete")
async def delete_post(post: models.PostDelete, db: Session = Depends(db.get_db)):
    CRUD.delete_post(db, post.id)
    return models.SUCCESS

@app.post("/post/comment")
async def write_comment(comment: models.CommentBase, db: Session = Depends(db.get_db)):
    com = models.CommentCreate
    com.post_id = comment.post_id
    com.user_id = comment.user_id
    com.message = comment.message
    com.msg_datetime = datetime.now()
    com = CRUD.post_comment(db, com)
    return com


@app.post("/post/like")
async def like_post(like: models.LikeBase, db: Session = Depends(db.get_db)):
    like = CRUD.user_like_post(db, like)
    return models.SUCCESS

@app.post("/post/unlike")
async def like_post(like: models.LikeBase, db: Session = Depends(db.get_db)):
    temp =  CRUD.user_unlike_post(db, like)
    return models.SUCCESS


@app.get("/intializedb")
async def initialize_db(dbb: Session = Depends(db.get_db)):
    schemas.Base.metadata.create_all(bind=db.engine)
    r = models.RoleCreate
    r.name = 'admin'
    admin_role = CRUD.create_role(dbb, r)
    r.name = 'user'
    user_role = CRUD.create_role(dbb, r)
    x = models.UserCreate
    x.username = 'admin'
    x.password = 'admin'
    x.role_id = admin_role.id
    admin = CRUD.create_user(dbb, x)
    x.username = 'user'
    x.password = 'user'
    x.role_id = user_role.id
    user = CRUD.create_user(dbb, x)
    return "done"
    
@app.post("/uploadfile")
async def upload_file(file: UploadFile):
    bucket = s3.Bucket('miebakso')
    bucket.upload_fileobj(file.file, file.filename, ExtraArgs={'ACL': "public-read", 'ContentType': 'image/jpeg'})

    return {"message": "Hello World"}

@app.get("/getimg")
async def get_img():
    object = s3.Object('miebakso','image1.png')
    print(object)
    return "<img src='https://miebakso.s3.amazonaws.com/image1.png' / >"

@app.get("/tables")
async def get_tables():
    # tab = schemas.Base.metadata.tables.keys()
    # print(tab)
    # return { 'table': tab}
    return 'asd'

@app.get("/generatedata")
async def get_tables():
    # tab = schemas.Base.metadata.tables.keys()
    # print(tab)
    # return { 'table': tab}
    return 'asd'

@app.get("/removedb")
async def remove_db():
    schemas.Base.metadata.drop_all(db.get_engine())
    return "delete table"