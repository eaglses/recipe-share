steps = [
    [
        # "Up" SQL statement
        """
        CREATE TABLE user_group (
            id SERIAL PRIMARY KEY,
            owner_id INT REFERENCES users (id) ON DELETE CASCADE NOT NULL,
            group_name VARCHAR(150)         
        );
        """,
        # "Down" SQL statement
        """
        DROP TABLE user_group;
        """,
    ],
    [
        # "Up" SQL statement
        """
        CREATE TABLE group_members (
            group_id INT REFERENCES user_group(id) ON DELETE CASCADE NOT NULL,
            user_id INT REFERENCES users(id) ON DELETE CASCADE NOT NULL,
            approved BOOL NOT NULL
            
        );
        """,
        # "Down" SQL statement
        """
        DROP TABLE group_members;
        """,
    ],
    [
        # "Up" SQL statement
        """
        CREATE TABLE type (
            id SERIAL PRIMARY KEY,
            name VARCHAR(150)
           
        );
        """,
        # "Down" SQL statement
        """
        DROP TABLE type;
        """,
    ],
    [
        # "Up" SQL statement
        """
        CREATE TABLE recipe (
            id SERIAL PRIMARY KEY,
            user_group_id INT REFERENCES user_group (id),
            typ_id INT REFERENCES type (id),
            upload_id  INT REFERENCES users (id),
            public BOOL NOT NULL,
            uploaded TIMESTAMPTZ NOT NULL
           
        );
        """,
        # "Down" SQL statement
        """
        DROP TABLE recipe;
        """,
    ],
    [
        # "Up" SQL statement
        """
        CREATE TABLE ingredient (
            id SERIAL PRIMARY KEY,
            recipe_id INT REFERENCES recipe (id),
            mesurement VARCHAR(150),
            amount INT,
            name VARCHAR(150)
        );
        """,
        # "Down" SQL statement
        """
        DROP TABLE ingredient;
        """,
    ],
]
