# <scripts/server-up.ps1>
# Raises the server.


# Stop on errors
$ErrorActionPreference = "Stop"


# Running the Django server
python src/backend/manage.py runserver
