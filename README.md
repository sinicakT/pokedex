# Pokédex Django App

A web application for browsing and managing Pokémon data, built with Django and TailwindCSS.

---

## 🚀 Quick Start

### 1. Start the application using Docker Compose

```bash
docker compose up -d
```
This will build and start the required containers (e.g. webapp, database).

### 2. Enter the web application container

```bash
docker compose exec webapp bash
```
This gives you access to the webapp container's shell.

### 3. Initialize the application

```bash
make init_app
```
This will apply migrations, create superuser and sync data needed to start the app ()
