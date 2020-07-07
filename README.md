# FSND - Capstone: Casting Agency

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. 
You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

There three(3) Roles in the application: 
    -Casting Assistant
        -Can view actors and movies
    -Casting Director
        -All permissions a Casting Assistant has and…
        Add or delete an actor from the database
        Modify actors or movies
    -Executive Producer
       - All permissions a Casting Director has and…
        Add or delete a movie from the database

# Auth0 application and Api is set up and configured for handling authentication and authorization 
---------------------------------------------------------------------------------------------------------------------------

Initial Setup:
    App is running on: # https://castingagency2020.herokuapp.com/ 
        - go to this url and click login button 
        - you will be redirected to Auth0 login page where you need provide credentials 
        # Casting Assistant Credentials:
           username: assistant@gmail.com
           password: 2020Assistant 
        # Casting Director Credentials:
            username: director@gmail.com
            password: 2020Director 
        # Casting Executive Credentials:
            username: executive@gmail.com  
            password: 2020Executive 
        - once you enter desired role credentials, you will be redirected to dashboard page 
        - on dashboard page you get copy the Active JWT and try Postman or Curl on endpoints 
    # API Endpoints: 
        GET # https://castingagency2020.herokuapp.com//movies    - to get movies: role has to have get:movies permission 
        GET # https://castingagency2020.herokuapp.com//actors    - to get actors: role has to have get:actors permission 
        POST # https://castingagency2020.herokuapp.com//movies   - to create a movie. Body = {"title": "string", "release_date": "2020-07-07} 
                                                                    format and role has to    have post:movie permission 
        POST # https://castingagency2020.herokuapp.com//actors   - to create a actor. Body = {"name": "string", "gender": "string"} 
                                                                    format and role has to have post:actor permission 
        PATCH # https://castingagency2020.herokuapp.com//movies/{id}  - to update a movie. role has to have patch:movie permission 
        PATCH # https://castingagency2020.herokuapp.com//actors/{id}    - to update an actor. role has to have patch:actor permission 
        DELETE # https://castingagency2020.herokuapp.com//movies/{id}   - to delete a movie. role has to have delete:movie permission 
        DELETE # https://castingagency2020.herokuapp.com//actors/{id}   - to delete an actor. role has to have delete:actor permission 
        


