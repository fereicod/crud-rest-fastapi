# Product Catalog System

## Propose General Picture / System Design
![](https://github.com/fereicod/crud-rest-fastapi/blob/main/system-design_v1.png)

## Description
This is a basic catalog system to manage products. Each product has the following information:
- SKU
- Name
- Price
- Brand

The system supports two types of users:
1. **Admin Users**: Can create, update, and delete products, as well as manage other admin users.
2. **Anonymous Users**: Can only retrieve product information.

### Special Features
- When an admin updates a product (e.g., changes the price), all other admins are notified via email or another mechanism.
- The system tracks how many times each product is queried by anonymous users for future reporting.

## Technology Stack
- **API**: REST
- **Uvicorn**: ASGI server
- **Database**: MySQL
- **Containerization**: Docker
- **Security**: JWT with Bearer Tokens


## Getting Started with Docker
To run the project using Docker:

1. Clone the repository:
```bash
git clone https://github.com/fereicod/crud-rest-fastapi.git
cd crud-rest-fastapi
```

2. Build and start the containers:
```bash
docker-compose up --build
```

3. The API will be available at:
```bash
http://localhost:8000
```

4. API documentation can be accessed at:
```bash
http://localhost:8000/docs
```

## ▶️ Makefile Commands
This project includes a `Makefile` to simplify common development tasks.

- Usage:
  - `make`: Shows a list of all available commands.

- Dependencies
  - `make install` : Install all requirements to run the service.

- Testing
  - `make test` : Runs the automated test suite.

- Service Management
  - `make run` : Starts all services (API and database) in detached mode.
  - `make down` : Stops and removes the containers of the running services.
  - `make clean` : Stops the services, and removes associated containers and volumes.


## API Usage
- Anonymous Users: Retrieve product info (GET /product)
- Admin Users: **CRUD** operations on products and admins

## Notes
The system is designed to scale by adding more API instances behind a load balancer.

Future improvements can include:
- More automated tests
- Deployment to a cloud provider
- Enhanced notification mechanisms.

## References
- [Astral UV Docker Integration Guide](https://docs.astral.sh/uv/guides/integration/docker/)
- [Deep Dive into UV Dockerfiles: Image Size & Performance](https://medium.com/@benitomartin/deep-dive-into-uv-dockerfiles-by-astral-image-size-performance-best-practices-5790974b9579)
- [Uvicorn Docker Deployment](https://www.uvicorn.org/deployment/docker/)
- [FastAPI Security: OAuth2 JWT with Bearer Tokens](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/?h=bearer#hash-and-verify-the-passwords)
- [SQLmodel](https://sqlmodel.tiangolo.com/)
- [SQLAlchemy - Dialect](https://docs.sqlalchemy.org/en/20/dialects/index.html)

## MYSQL
You can use the next file **init_catalog.sql**
