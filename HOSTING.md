# Hosting — quickest demo path

The project includes a single Docker image that builds the React frontend and runs FastAPI. Render supports Docker web services and requires the app to listen on `0.0.0.0`; this project's Dockerfile does that and uses the platform `PORT` value. A Render service gets an `onrender.com` URL after deployment.

## Render
1. Push this folder to a GitHub repository.
2. In Render, create **New → Web Service** and connect the repository.
3. Set the runtime/language to **Docker** so Render builds the included Dockerfile.
4. Set health check path to `/health` if it is not detected automatically.
5. Deploy.

The Docker command automatically seeds the 20 demo services before starting FastAPI.

For a persistent public deployment, configure `DATABASE_URL` to a managed PostgreSQL database and set a strong `SECRET_KEY`. The included SQLite database is intended for the hackathon demo.
