# Burr + FastAPI + Docker Compose Example

This is a boilerplate configuration of FastAPI and Burr in a docker compose environment, where FastAPI and Burr are running in separate containers with shared burr data. 

This provides a minimal Burr Application with two Actions - enough for demonstrating telemetry between the containers, just focusing on the unique configuration of the docker compose environment.

**FastAPI:** This FastAPI configuration is optimized for a docker compose environment, with poetry for package management, and hot reloading in development mode. See `docker-compose.override.yml` for development target hot reloading. 


#### Dev & Prod

- **FastAPI**:
  - The **FastAPI** Dockerfile.api has development and production builds
  - The development build includes hot reloading for fast development
  - The production build does not include hot reloading
- **Burr**:
  - The **Burr container** has not been tested in a production environment, and running it in production in its current form makes telemetry data public because there is no authentication protection.
  - Recommend running this in development environment only.

## Running It

```bash
# Start the containers
$ docker compose up --build

# Stopping the containers and clearing the volumes (helpful for troubleshooting)
$ docker compose down -v
```

You will see logged messages of the URLs where both the FastAPI and Burr servers are available. 

- Note: The FastAPI server is ready to accept requests from apps / Postman, and is not configured with CORS to handle browser requests.
- Execute the test `GET` request against the FastAPI server to see the flow logged to Burr's web UI

## Docker Compose Explainer

#### Shared Volume

- A shared volume is used between the FastAPI container and the Burr container for burr-data
- In the FastAPI server, a `LocalTrackingClient` is created specifying the storage dir as the burr_path environment variable (set in docker-compose.yml. See [Burr Tracking Docs](https://burr.dagworks.io/reference/tracking/))
- The Burr server also accepts a storage directory path as an environment variable (set in docker-compose.yml. See `LocalBackend` [class comments](https://github.com/DAGWorks-Inc/burr/blob/a1a0b3bcb0f64790615042527c0e173a6c436083/burr/tracking/server/backend.py#L257) for instructions.)
- In `docker-compose.yml` both container's burr_path environment variable is set to the burr-data volume path that both containers are also using.

The burr server automatically updates when the FastAPI server writes new tracking data because they are using the same volume.

#### Dockerfiles

- **Dockerfile.api**: The FastAPI dockerfile configured for burr and poetry requirements, with production and development targets.
- **Dockerfile.burr**: The Burr dockerfile is configured with tini, allowing the burr docker container to properly handle process signals (like shutdown)

#### Host

Hosts for both containers are set to `0.0.0.0` which is optimal for the docker compose setup.