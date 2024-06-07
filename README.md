# Geospatial Analysis on the Cabspotting Dataset

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Installation and Setup](#installation-and-setup)
## Introduction

This project is a geospatial analysis on the [Cabspotting](link_here) dataset.

## Prerequisites
- [Docker](https://www.docker.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [PostGIS](https://postgis.net/)
- [PGAdmin](https://www.pgadmin.org/)
  

## Installation and Setup

### Build the Docker Container
1. Download the repo and build the container:

```bash
git clone https://github.com/tonytziorvas/Cabspotting-Analysis.git
cd Cabspotting-Analysis
docker-compose up -d
``` 
2. Download the data from [this link](http://www.lac.inpe.br/~rafael.santos/Docs/CAP394/Data/cabspottingdata/alldata.zip) and extract the zip folder inside the root directory.
3. Inside the terminal paste the following commands:
```bash
poetry shell
python scripts/make_dataset.py
```
### Configure pgAdmin
To create the database in pgAdmin, follow these simple steps:

1. Launch pgAdmin: Open your web browser and go to http://localhost:8080. This is where pgAdmin will be running as specified in your Docker Compose file.

2. Log in to pgAdmin: Enter the email (admin@admin.com) and password (password) that you set in your Docker Compose file.

3. Add a New Server: After logging in, right-click on "Servers" in the Browser panel on the left and select "Create" > "Server..."

4. Configure the New Server: In the "General" tab, enter a name for your server (e.g., PostgreSQL)

5. Switch to the "Connection" tab and fill in the following details:
   - Host name/address: db (this is the service name you used in the Docker Compose file)
   - Port: 5432
   - Maintenance database: CabspottingDB
   - Username: admin
   - Password: password

6. Click "Save". pgAdmin will now attempt to connect to your PostgreSQL server.
   
### Create the Positions table

1. Open `CabspottingDB`, right-click on the "Extensions" tab, and select "Create" > "Extension...". Search for `postgis` and click "Save".

2. Right click on `CabspottingDB`, select "Query Tool" and paste the following command to create the table:
```sql
CREATE TABLE positions (
    id SERIAL PRIMARY KEY,
    taxi_id VARCHAR(25),
    timestamp INTEGER,
    lat REAL,
    lon REAL,
    occupancy BOOLEAN,
    location GEOMETRY(POINT, 4326)
);
```

3. In the "Query Tool", paste the following command to load the data into the table:
```sql
COPY positions (taxi_id, timestamp, lat, lon, occupancy, location)
FROM '/var/lib/postgresql/alldata/cabspotting_full.csv'
DELIMITER ','
CSV HEADER;
```
