import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
import random

from api import create_app
from models import setup_db, Movie, Actor

project_dir = os.path.dirname(os.path.abspath(__file__))

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "movies_test.db"
        self.database_path = "sqlite:///{}".format(os.path.join(project_dir, self.database_name))
        self.castingDirectorToken = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFaazYyLWRPWWo0NE1IaGpyYW9RcSJ9.eyJpc3MiOiJodHRwczovL2Rldi1xb3I4MnV2MC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYwMjVkY2RhMTViN2IwMDEzNjFkYzdlIiwiYXVkIjoibW92aWVzIiwiaWF0IjoxNTk0MTI4NDkyLCJleHAiOjE1OTQyMTQ4OTAsImF6cCI6IkthM0hyOWZrWjRaME8yaUpwazM1NURBNjZScEpKMnZ2Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJnZXQ6YWN0b3ItZGV0YWlsIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZS1kZXRhaWwiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiXX0.C1zlgwmlIs-Q-lIwscyOLHnYGpmBf3iEoVaevRaP2DKu6tQqU3mqNBGktnHprEosZ5KMCiysal8noDwqwSiwoc8kP-oIY0sqfAKFUTOJgfdeXWThYhsZKbBWwzQB9J8iseSQoVSmMh1o7oivFF-yG2aNu1BBZUBz7Qkf-PjJLCUDqdOES630aivMB2PZs2FFizZQIKO7XLmc6OzAOOBa89Ikc29IdnC4qhbcid1SM26kezap_wPC9EVYIySBkc7THeaomiZgYyZEjUxWrKcTri-gAQpWqLt8MpcVytoM_RrSmdRxuQfmq9iegC8FebuJBxO4lDWO2-PKPj0uJIZk8w"
        self.executiveDirector = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFaazYyLWRPWWo0NE1IaGpyYW9RcSJ9.eyJpc3MiOiJodHRwczovL2Rldi1xb3I4MnV2MC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYwMjVkZWQyZWIzMDMwMDE5YzgzMGZhIiwiYXVkIjoibW92aWVzIiwiaWF0IjoxNTk0MTMyMDIyLCJleHAiOjE1OTQyMTg0MjAsImF6cCI6IkthM0hyOWZrWjRaME8yaUpwazM1NURBNjZScEpKMnZ2Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJkZWxldGU6bW92aWUiLCJnZXQ6YWN0b3ItZGV0YWlsIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZS1kZXRhaWwiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.XXZt33-dXMRk1gK4ccr5XEU-lrpWwbB1kKVIiHQziiWO4qf9zq_O1zk1pvAPtWi8VCF2Q0Z0pHiRFYSXO43r_uN7_xlE5g6IuTjQ0yZn-l1kfgPLQdffw1jBHbOhXTsLOV_eqhIL6ff8U8iZnteCFL4QN2uoFipze7nF6AXKKR_LAdiCkj5UH0W_nS0NFbiKQ8nrSClUECo9_Qn22r-n_yhzguaIXq6GJDi7vEYdmE-72-MWAPU6h4VTEVjiFYKuXD51nxCH-nwFcGXiV6GZoAt9ZJcCKnD94EZNib6yWOR6r9MHTzv5O4hSnncJQNBtnEsvSRi5TXg7LTVR6HJ8pg"
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass


    ## Movie Endpoint Tests 

    def test_get_movies_fail_unauthorized(self):
        res = self.client().get("/movies")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_get_movies_success(self):
        headers = {"Authorization": self.castingDirectorToken}
        res = self.client().get("/movies", headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(type(data["movies"]), list)


    def test_post_movie_fail_403(self):
        headers = {"Authorization": self.castingDirectorToken}
        body = {"title": "test movie", "release_date": "2000-01-12"}
        res = self.client().post("/movies", headers=headers, json=body)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
    
    def test_post_movie_fail_401(self):
        body = {"title": "test movie", "release_date": "2000-01-12"}
        res = self.client().get("/movies", json=body)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_pacth_movie_fails(self):
        body = {"title": "test movie"}
        res = self.client().patch("/movies/1", json=body)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_delete_movie_unauthorized(self):
        headers = {"Authorization": self.castingDirectorToken}
        res = self.client().delete(f"/movies/1", headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)

    def test_patch_movie_fail(self):
        body = {"title": "test movie"}
        res = self.client().patch("/movies/1", json=body)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    
    
    ## Actor Endpoint Tests 
    def test_get_actors_fail_unauthorized(self):
        res = self.client().get("/actors")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_get_actors_success(self):
        headers = {"Authorization": self.castingDirectorToken}
        res = self.client().get("/actors", headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(type(data["actors"]), list)


    def test_post_actor_success(self):
        headers = {"Authorization": self.castingDirectorToken}
        name = "test actor" + str(random.randint(1,1000))
        body = {"name": name, "gender": "male"}
        res = self.client().post("/actors", headers=headers, json=body)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
    
    def test_patch_actor_success(self):
        actor = Actor.query.first() 
        if actor:
            headers = {"Authorization": self.castingDirectorToken}
            name = "test actor" + str(random.randint(1,1000))
            body = {"name": name, "gender": "male"}
            res = self.client().patch(f"/actors/{actor.id}", headers=headers, json=body)
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
    def test_patch_actor_fail(self):
            headers = {"Authorization": self.castingDirectorToken}
            name = "test actor" + str(random.randint(1,1000))
            body = {"name": name, "gender": "male"}
            res = self.client().patch(f"/actors/{444333}", headers=headers, json=body)
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 422)
    
    def test_delete_actor_success(self):
        actor = Actor.query.first() 
        if actor:
            headers = {"Authorization": self.castingDirectorToken}
            res = self.client().delete(f"/actors/{actor.id}", headers=headers)
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)

    def test_delete_actor_fails_422(self):
        actor = Actor.query.first() 
        headers = {"Authorization": self.castingDirectorToken}
        res = self.client().delete(f"/actors/{5654654}", headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)

    def test_delete_actor_fails_401(self):
        res = self.client().delete(f"/actors/{1}")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)


    def test_post_movie_success(self):
        headers = {"Authorization": self.executiveDirector}
        title = "test movie" + str(random.randint(0,2000))
        body = {"title": title, "release_date": "2000-01-12"}
        res = self.client().post("/movies", headers=headers, json=body)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)


    def test_post_movie_fails_exuciti(self):
        headers = {"Authorization": self.executiveDirector}
        title = "test movie" + str(random.randint(0,2000))
        body = {"release_date": "2000-01-12"}
        res = self.client().post("/movies", headers=headers, json=body)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)


        

if __name__ == "__main__":
    unittest.main()