#!/usr/bin/env python
"""This code assists ExperimentServer.py with HTTP requests."""

import sqlite3
import bleach

db_name = "posts_db"


def get_posts():
    """Retrieve posts from database in response to GET request."""

    conn = sqlite3.connect(database=db_name)
    c = conn.cursor()
    c.execute("select date, post from posts order by post_id")
    posts = c.fetchall()
    conn.close()
    return posts


def new_post(post, date):
    """
    Store a new post in the database.

    Arguments:
        post_content: A list with the content of a new post, including post and date.
    """

    # Sanitize the post.
    post_content = [post, date]
    post_content[0] = bleach.clean(post_content[0])

    conn = sqlite3.connect(database=db_name)
    c = conn.cursor()
    c.execute("select max(post_id) from posts")
    max_id = c.fetchall()
    new_id = str(max_id[0][0] + 1)
    post_content.append(new_id)
    # values = "('" + post_content[0] + "','" + post_content[1] + "'," + post_content[2] + ")"
    # values = "(" + post_content[2] + ",'" + post_content[0] + "','" + post_content[1] + "')"
    values = tuple(post_content)
    print(values)
    c.execute("INSERT INTO posts (post,date,post_id) VALUES (?,?,?)", values)
    conn.commit()
    conn.close()
