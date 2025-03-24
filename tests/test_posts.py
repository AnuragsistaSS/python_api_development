import pytest
from app import schema

def test_get_all_posts(tests_posts,authorized_client):
    res = authorized_client.get("/posts/")
    
    def validate(post):
        return schema.PostWithVotes(**post)
    
    post_list = list(map(validate,res.json()))
    assert len(post_list) == len(res.json())
    assert res.status_code == 200

def test_unauthorized_get_all_posts(client,tests_posts):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_get_post(tests_posts,authorized_client):
    print(" test post id",tests_posts[0].id)
    res = authorized_client.get(f"/posts/get_posts/{tests_posts[0].id}")
    post = schema.PostWithVotes(**res.json())
    assert post.Post.id == tests_posts[0].id
    assert post.Post.title == tests_posts[0].title
    assert post.Post.content == tests_posts[0].content
    assert res.status_code == 200

def test_unauthorized_get_post(client,tests_posts):
    res = client.get(f"/posts/get_posts/{tests_posts[2].id}")
    assert res.status_code == 401

@pytest.mark.parametrize
def test_authorized_add_post(authorized_client,test_user):
    res = authorized_client.post("/posts/add_post",json={"title":"New Post","content":"Content of new post"})
    assert res.status_code == 201
    assert res.json()["title"] == "New Post"

def test_unauthorized_add_post(client,test_user):
    res = client.post("/posts/add_post",json={"title":"New Post","content":"Content of new post"})
    assert res.status_code == 401

def test_authorized_delete_post(authorized_client,tests_posts):
    res = authorized_client.delete(f"/posts/delete_post/{tests_posts[0].id}")
    assert res.status_code == 204

def test_unauthorized_delete_post(client,tests_posts):
    res = client.delete(f"/posts/delete_post/{tests_posts[0].id}")
    assert res.status_code == 401

def test_authorized_update_post(authorized_client,test_user,tests_posts):
    res = authorized_client.put(f"/posts/update_post/{tests_posts[0].id}",json={"title":"Updated Post","content":"Updated content","id":tests_posts[0].id})
    assert res.status_code == 201

def test_unauthorized_update_post(client,test_user,tests_posts): 
    res = client.put(f"/posts/update_post/{tests_posts[0].id}",json={"title":"Updated Post","content":"Updated content","id":tests_posts[0].id})
    assert res.status_code == 401

def test_update_post_of_another_user(authorized_client,test_user, test_user2, tests_posts):
    data = {"title":"Updated Post","content":"Updated content","id":tests_posts[1].id}
    res = authorized_client.put(f"/posts/update_post/{tests_posts[1].id}",json=data)
    assert res.status_code == 403
    assert res.json()["detail"] == "You are not authorized to update this post"