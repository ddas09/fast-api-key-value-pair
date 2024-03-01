# Key-Value Store using Kubernetes and FastAPI

This project implements a scalable key-value store using Kubernetes for orchestration and FastAPI for the web framework.

## Project Structure

- `app/`: Contains the main application code.
  - `models/`: Data models.
  - `services/`: Business logic and services.
  - `helpers/`: Helper classes and functions.
  - `middlewares/`: Middleware components.
- `deployments/`: Kubernetes deployment files.
- `tests/`: Test cases.
- `main.py`: FastAPI application entry point.
- `README.md`: Project documentation.

## Prerequisites

Make sure you have the following tools installed on your system:
- Python 3.x
- FastAPI
- Redis
- Docker
- Kubernetes (minikube for local development)
- kubectl

## Steps

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/ddas09/redis-keyvalue-pair.git
    cd key-value-store
    ```

2. **Start Redis:**

    Ensure Redis is running. If not, you can start it using Docker:

    ```bash
    docker run -d -p 6379:6379 redis
    ```

3. **Start Minikube (if not already running):**

    ```bash
    minikube start
    ```

4. **Deploy Kubernetes Resources:**

    ```bash
    kubectl apply -f kubernetes/
    ```

5. **Build and Run FastAPI Locally:**

    ```bash
    cd app
    pip install -r requirements.txt
    python main.py
    ```

    Access FastAPI at [http://localhost:8000](http://localhost:8000).

6. **Cleanup:**

    To stop and remove local Kubernetes resources:

    ```bash
    kubectl delete -f kubernetes/
    minikube stop
    minikube delete
    ```

## To run the test cases

1. **Navigate to the root directory of your project:**

    ```bash
    cd key-value-store
    ```

2. **Install pytest:**

    ```bash
    pip install pytest
    ```

3. **Run the test cases using pytest:**

    ```bash
    pytest tests/
    ```

The test results will be displayed in the terminal, indicating whether each test passed or failed.
