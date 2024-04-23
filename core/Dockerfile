FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11


COPY ./falcon-solver ./falcon-solver

CMD ["uvicorn", "falcon-solver.server.app:create_app", "--host", "0.0.0.0"]