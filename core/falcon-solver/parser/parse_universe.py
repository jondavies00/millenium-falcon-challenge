import logging
import sqlite3


def parse_universe(db_path: str) -> dict[dict[str, int]]:
    connection = sqlite3.connect(db_path)
    cur = connection.cursor()
    res = cur.execute("SELECT * FROM routes;")
    results = res.fetchall()
    graph = {}
    for r in results:
        if r[0] not in graph:
            graph[r[0]] = {}
        if r[1] not in graph:
            graph[r[1]] = {}
        graph[r[0]][r[1]] = r[2]
        graph[r[1]][r[0]] = r[2]
    return graph
