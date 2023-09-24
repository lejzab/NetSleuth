from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)


def session_select():
    stmt = text("SELECT x, y FROM some_table ORDER BY x, y")
    with Session(engine) as session:
        result = session.execute(stmt)
        for row in result:
            print(f"x: {row.x}, y: {row.y}")


def create_table():
    with engine.connect() as conn:
        conn.execute(text("CREATE TABLE some_table (x int, y int)"))
        conn.execute(
            text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
            [{"x": 1, "y": 1}, {"x": 2, "y": 4}],
        )
        conn.commit()


def conn_insert():
    with engine.begin() as conn:
        conn.execute(
            text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
            [{"x": 6, "y": 8}, {"x": 9, "y": 10}],
        )


def conn_select():
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT x, y FROM some_table WHERE y > :y"),
            {"y": 2}
        )
        for x, y in result:
            print(f"x: {x}, y: {y}")


def session_update():
    stmt = text("UPDATE some_table SET y=:y WHERE x=:x")
    with Session(engine) as session:
        session.execute(stmt,
                        [
                            {"x": 9, "y": 14},
                            {"x": 1, "y": 22}
                        ])
        session.commit()


if __name__ == '__main__':
    print("no cześć")
    create_table()
    conn_insert()
    conn_select()

    session_select()
    session_update()
    session_select()
