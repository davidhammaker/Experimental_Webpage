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
