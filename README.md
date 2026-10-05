# ImageManager
ImageManager is a simple image upload and gallery server built with Python, Docker and Nginx.


## Features
- Upload JPG, PNG and GIF images
- Maximum file size: 5 MB
- Automatically generates a unique filename for each uploaded image
- Image gallery
- Direct image access through Nginx
- Image preview in a modal window
- Logging of successful uploads and errors
- Persistent storage using Docker volumes
- Nginx reverse proxy
- Background music on web pages


## Project Structure
```ImageManagerProject/
├── app.py
├── server.py
├── handlers.py
├── pages.py
├── responses.py
├── upload.py
├── config.py
├── logger.py
├── nginx.conf
├── compose.yaml
├── Dockerfile
├── requirements.txt
├── .dockerignore
├── README.md
├── images/
├── logs/
└── static/
    ├── style.css
    └── music.mp3
```

## Requirements
Python 3.12+
Docker
Docker Compose


## Running the Project
Build and start the application with:

docker compose up --build

The application will be available at:

http://localhost:8080/

The Python backend runs on:

http://localhost:8000/


## Available Routes
Method	Route	Description
GET	/	Home page
GET	/upload	Image upload page
POST	/upload	Upload an image
GET	/images/	Image gallery
GET	/images/<filename>	View an uploaded image


## Image List
The `/images-list` page displays all uploaded images stored in the PostgreSQL database.

The table contains:

- Filename
- Original filename
- File size
- Upload date and time
- File type
- Delete button

Images are sorted by upload time, with the newest images displayed first.

The list uses pagination with 10 images per page.

Available navigation:

- Previous
- Next


## Delete Images
Each image in the `/images-list` page has a Delete button.

Before deletion, a confirmation window is displayed.

After confirmation:

- the physical image file is deleted;
- the image metadata is deleted from PostgreSQL;
- the user is redirected to `/images-list`;
- a success message is displayed for a few seconds.

Delete errors are logged in `logs/app.log`.


## Upload Restrictions
Allowed image formats:

JPG
PNG
GIF

Maximum file size:

5 MB

Uploaded files receive automatically generated unique names.


## Logging
Application logs are stored in:

logs/app.log

The application records successful uploads and errors.


## Docker Volumes
Images are stored persistently in:

./images

Logs are stored persistently in:

./logs

The data remains available after containers are stopped and restarted.


## PostgreSQL Backup
The project uses PostgreSQL to store image metadata.

A database backup can be created using the PowerShell script:

backup.ps1

Run the script from the project root:

.\backup.ps1

The backup is saved in the `backups/` directory with a timestamped filename:

backups/backup_YYYYMMDD_HHMMSS.sql

Example:

backups/backup_20261004_142935.sql

The `backups/` directory is excluded from Git using `.gitignore`.


## Restore PostgreSQL Database
To restore the database from a backup, start the Docker containers:

docker compose up -d

Then restore the SQL dump:

Get-Content backups/backup_YYYYMMDD_HHMMSS.sql | docker compose exec -T db psql -U postgres -d images_db

After the restore, the image metadata stored in PostgreSQL will be restored.


## Technologies
Python
Python http.server
Docker
Docker Compose
Nginx
HTML
CSS
JavaScript