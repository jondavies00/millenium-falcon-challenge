import logging
import sqlite3
from pathlib import Path


def parse_universe(db_path: str) -> dict[dict[str, int]]:
    """
    Given a universe database file path, parse the data into a dictionary,
    indexed by planet -> reachable planet -> autonomy to get there.
    """
    full_path = str(Path.cwd()) + db_path
    logging.info("Path of universe db: %s", str(Path.cwd()) + db_path)
    connection = sqlite3.connect(full_path)
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
