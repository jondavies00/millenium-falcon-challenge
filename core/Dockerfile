FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11


COPY ./falcon_solver ./falcon_solver

CMD ["uvicorn", "falcon_solver.server.app:create_app", "--host", "0.0.0.0"]