#!/usr/bin/env bash
# Exit on error

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Make new migrations

# Apply any outstanding database migrations
python manage.py migrate