# 1. Synchronize Django model with DB schema
python manage.py makemigrations

# 2. Delete migration history all
python manage.py migrate --fake account zero
python manage.py migrate --fake habits zero

# 3. Migrate in a fake way as initial migrate
# (create tables, etc. ) 
python manage.py migrate --fake-initial