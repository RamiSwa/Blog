13. `git checkout -b "main-1"`
14. `git push --set-upstream origin main-1`
15. `pip install python-decouple`
16. `pip install celery`
17. `pip install redis`
18. `pip install psycopg2-binary celery[redis] django-celery-results django-celery-beat` :

-----------------------------------
- The command `pip install psycopg2-binary celery[redis] django-celery-results django-celery-beat` installs several Python packages crucial for building asynchronous tasks in Django applications using Celery, with Redis as the message broker. Let's break down each package:

**1. `psycopg2-binary`**

* **Purpose:** This package provides a PostgreSQL database adapter for Python. It allows your Django application to interact with a PostgreSQL database for tasks like storing and retrieving data.
* **Example:**
    * **Result:** Enables your Django application to connect to and interact with a PostgreSQL database. 
    * **Usage:** You'll use this package in your Django project's settings to configure the database connection.

**2. `celery[redis]`**

* **Purpose:** This installs the Celery library with the Redis backend. Celery is an asynchronous task queue that allows you to offload time-consuming operations (like sending emails, processing images, etc.) from your main application thread, improving performance and responsiveness. 
    * `[redis]` in the installation command specifies that Redis should be used as the message broker for Celery. Redis is a fast, in-memory data store that's well-suited for handling messages efficiently.
* **Example:**
    * **Result:** Enables you to define and execute asynchronous tasks within your Django application.
    * **Usage:** You'll use Celery to define tasks that can be executed asynchronously. For example:
        ```python
        from celery import shared_task

        @shared_task
        def send_welcome_email(user_id):
            # Logic to send a welcome email to the user with the given ID
            pass
        ```

**3. `django-celery-results`**

* **Purpose:** This package provides a backend for storing the results of Celery tasks within your Django database. This allows you to track the status, progress, and results of tasks.
* **Example:**
    * **Result:** Enables you to store and retrieve the results of your Celery tasks within your Django database.
    * **Usage:** You'll configure `django-celery-results` in your Django settings to use your database for storing task results.

**4. `django-celery-beat`**

* **Purpose:** This package provides a scheduler for periodic tasks in Celery. You can define schedules for your tasks (e.g., every hour, every day) and Celery Beat will automatically execute them at the specified intervals.
* **Example:**
    * **Result:** Enables you to schedule recurring tasks to be executed by Celery.
    * **Usage:** You'll define schedules for your tasks in a `celerybeat_schedule` dictionary within your Django project.

**In Summary:**

These packages work together to enable asynchronous task processing within your Django application:

- `psycopg2-binary` provides database connectivity.
- `celery[redis]` allows you to define and execute asynchronous tasks using Celery with Redis as the message broker.
- `django-celery-results` stores the results of your tasks in the Django database.
- `django-celery-beat` schedules the execution of your tasks at specified intervals.

By using these packages, you can improve the performance and responsiveness of your Django application by offloading time-consuming operations to background workers, making your application more efficient and scalable.

-------------------------------------

19. `pip freeze > requirements.txt`
20. in settings.py add:

--------------------------------------------------------
```
from decouple import config

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',   
    'django_celery_results', #3rd app
    'examples', # our app
]


delete sqlite3 and add
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', default=5432, cast=int),
    }
}

STATICFILES_DIRS = [BASE_DIR / 'static']


# Media settings (for file uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


    # Email server configuration
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = config('EMAIL_HOST_USER') # EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD') # EMAIL_HOST_PASSWORD
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='default-email@example.com') # DEFAULT_FORM_EMAIL


CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'



# Celery settings
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

# Celery Results Backend
CELERY_RESULT_BACKEND = 'django-db'

```
---------------------------------------------------------

21. add .env
```
DEBUG=True
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER =
EMAIL_HOST_PASSWORD =
DEFAULT_FROM_EMAIL=admin@localhost
## -----------------------
DB_NAME= myblogdb
DB_USER=myuser
DB_PASSWORD=mypassword
DB_HOST=db
DB_PORT=5432
```

22. add gitignore:

```
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
#   For a library or package, you might want to ignore these files since the code is
#   intended to run in multiple environments; otherwise, check them in:
# .python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
#Pipfile.lock

# UV
#   Similar to Pipfile.lock, it is generally recommended to include uv.lock in version control.
#   This is especially recommended for binary packages to ensure reproducibility, and is more
#   commonly ignored for libraries.
#uv.lock

# poetry
#   Similar to Pipfile.lock, it is generally recommended to include poetry.lock in version control.
#   This is especially recommended for binary packages to ensure reproducibility, and is more
#   commonly ignored for libraries.
#   https://python-poetry.org/docs/basic-usage/#commit-your-poetrylock-file-to-version-control
#poetry.lock

# pdm
#   Similar to Pipfile.lock, it is generally recommended to include pdm.lock in version control.
#pdm.lock
#   pdm stores project-wide configurations in .pdm.toml, but it is recommended to not include it
#   in version control.
#   https://pdm.fming.dev/latest/usage/project/#working-with-version-control
.pdm.toml
.pdm-python
.pdm-build/

# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# PyCharm
#  JetBrains specific template is maintained in a separate JetBrains.gitignore that can
#  be found at https://github.com/github/gitignore/blob/main/Global/JetBrains.gitignore
#  and can be added to the global gitignore or merged into this file.  For a more nuclear
#  option (not recommended) you can uncomment the following to ignore the entire idea folder.
#.idea/

# PyPI configuration file
.pypirc

```
--------------------------------------------------

  23. create file docker-compose.yml:
```
services:
  db:
    image: postgres:14
    container_name: postgres_db_blog
    environment:
      POSTGRES_USER: myuser
      POSTGRES_PASSWORD: mypassword
      POSTGRES_DB: myblogdb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - blog_network
    ports:
      - "5432:5432"

  redis:
    image: redis:6.2
    container_name: redis_blog
    networks:
      - blog_network
    ports:
      - "6379:6379"

  celery:
    build: .
    container_name: celery_worker_blog
    command: celery -A blog_project worker --loglevel=info
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/0
    depends_on:
      - redis
      - db
    networks:
      - blog_network

  web:
    build:
      context: .
    container_name: django_app_blog
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
    networks:
      - blog_network

volumes:
  postgres_data:

networks:
  blog_network:
    driver: bridge

```

### Explain about 

```

Here’s a breakdown of the `docker-compose.yml` file you provided:

---

### **Services Section**
This section defines individual services that make up your application.

---

#### **`db` Service**
- **Purpose**: This service runs a PostgreSQL database.
- **Details**:
  - **`image: postgres:14`**:
    Specifies that the service uses the official PostgreSQL image, version `14`.
  - **`container_name: postgres_db_blog`**:
    Names the container `postgres_db_blog` for easy identification.
  - **`environment`**:
    Sets the required environment variables for PostgreSQL:
    - `POSTGRES_USER`: Username for the database.
    - `POSTGRES_PASSWORD`: Password for the database.
    - `POSTGRES_DB`: The name of the database to be created on initialization.
  - **`volumes`**:
    - Mounts the host's volume `postgres_data` to `/var/lib/postgresql/data` in the container, ensuring persistent data storage.
  - **`networks`**:
    - Connects the container to the `blog_network` network.
  - **`ports`**:
    - Maps port `5432` on the container (PostgreSQL's default port) to port `5432` on the host.

---

#### **`redis` Service**
- **Purpose**: Runs a Redis server, which acts as a message broker and result backend for Celery.
- **Details**:
  - **`image: redis:6.2`**:
    Uses the official Redis image, version `6.2`.
  - **`container_name: redis_blog`**:
    Names the container `redis_blog`.
  - **`networks`**:
    - Connects to the `blog_network` network.
  - **`ports`**:
    - Maps port `6379` on the container (Redis's default port) to port `6379` on the host.

---

#### **`celery` Service**
- **Purpose**: Runs the Celery worker to execute background tasks.
- **Details**:
  - **`build: .`**:
    Tells Docker to build this service using the Dockerfile in the current directory.
  - **`container_name: celery_worker_blog`**:
    Names the container `celery_worker_blog`.
  - **`command: celery -A blog_project worker --loglevel=info`**:
    Runs Celery with the application `blog_project` and logs activity with the `info` level.
  - **`environment`**:
    - Configures Celery to use Redis as the broker and result backend:
      - `CELERY_BROKER_URL`: Points to the Redis broker at `redis://redis:6379/0`.
      - `CELERY_RESULT_BACKEND`: Points to Redis for storing task results.
  - **`depends_on`**:
    - Specifies that this service depends on the `redis` and `db` services, ensuring they start first.
  - **`networks`**:
    - Connects to the `blog_network` network.

---

#### **`web` Service**
- **Purpose**: Runs the Django web application.
- **Details**:
  - **`build`**:
    - **`context: .`**: Tells Docker to build this service using the Dockerfile in the current directory.
  - **`container_name: django_app_blog`**:
    Names the container `django_app_blog`.
  - **`command: python manage.py runserver 0.0.0.0:8000`**:
    Runs the Django development server, binding to all interfaces on port `8000`.
  - **`volumes`**:
    - Mounts the current directory (`.`) into the container at `/app` for development convenience.
  - **`ports`**:
    - Maps port `8000` on the container to port `8000` on the host.
  - **`depends_on`**:
    - Specifies that this service depends on the `db` and `redis` services, ensuring they start first.
  - **`networks`**:
    - Connects to the `blog_network` network.

---

### **Volumes Section**
- **`postgres_data`**:
  - Creates a named volume to persist PostgreSQL data, ensuring that database content is retained even if the container is restarted or removed.

---

### **Networks Section**
- **`blog_network`**:
  - Defines a custom Docker network named `blog_network`:
    - **`driver: bridge`**: Uses the bridge driver for network isolation and communication between containers.

---

### **How It Works Together**
1. **Database (`db`)**:
   - Provides the backend database (PostgreSQL) for the Django app.
2. **Redis (`redis`)**:
   - Acts as the message broker and task result backend for Celery.
3. **Celery Worker (`celery`)**:
   - Processes background tasks sent by the Django app using Redis as the broker.
4. **Web App (`web`)**:
   - Runs the Django web application and interacts with the database (`db`) and Celery worker (`celery`).

This setup ensures seamless integration and communication between the components using the `blog_network`. It also leverages Docker for containerization, making the system modular and easy to manage.


```
    ------------------------------------

24. create Dockerfile:
```
FROM python:3.10

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install PostgreSQL client
RUN apt-get update && apt-get install -y postgresql-client

# Copy project files
COPY . .

# Default command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

```

------------------------------------------------------

25. in Folder project near settings.py create celery.py:
```
FROM python:3.10

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install PostgreSQL client
RUN apt-get update && apt-get install -y postgresql-client

# Copy project files
COPY . .

# Default command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

```
  -----------------------------------------------

  26. create 2 folders static and media
  27. Now run `docker-compose up --build -d`
      this is rusults:
      ![image](https://github.com/user-attachments/assets/7c085606-58b1-4491-b7e7-4ac85085df27)

-------------------------------------
  28. `docker-compose exec web python manage.py startapp examples`
  29. add examples in INSTALLED_APPS
  30. `docker-compose exec web python manage.py makemigrations`

  31. `compose exec web python manage.py migrate`
  32. in examples add tasts.py:

```
from celery import shared_task

@shared_task
def trial_task(x, y):
    return x + y

```

  33. run `docker-compose exec web celery -A myproject worker --loglevel=info`
  34. run with another cmd `docker-compose exec web python manage.py shell`
  35. >>> `from examples.tasks import trial_task`
  36. >>> `trial_task.delay(4, 5)`
      this is results:
      ![image](https://github.com/user-attachments/assets/d810fc2b-1862-4ed2-81fd-65b02bdfb495)
      ![image](https://github.com/user-attachments/assets/66111eb2-8336-4f10-84ea-6a15cc9c8528)

# Now all the settings work

37. Now Run: ` docker-compose exec web python manage.py createsuperuser  `
38. open browser in ` http://127.0.0.1:8000/admin/ `
    this is results:
    ![image](https://github.com/user-attachments/assets/55e6d5c4-680d-4cc3-8caa-073accd60a9b)
    ![image](https://github.com/user-attachments/assets/207edf3f-50b6-4205-9936-fef1f07c03b5)

39. Now Go to create app acooounts
    


-------------------------

The error now indicates an inconsistency within the `admin` app migrations. Specifically, `admin.0002_logentry_remove_auto_add` is applied before its dependency `admin.0001_initial`. This indicates deeper migration history issues in your database.

Let’s address it step by step:

---

### **Step 1: Reset Migration History for the `admin` App**
We need to clean up the migration history for the `admin` app.

1. Open the PostgreSQL shell:
   ```bash
   docker-compose exec db psql -U myuser myblogdb
   ```

2. Delete all migration history for the `admin` app:
   ```sql
   DELETE FROM django_migrations WHERE app = 'admin';
   ```

3. Exit the PostgreSQL shell:
   ```sql
   \q
   ```

---

### **Step 2: Fake Reapply `admin` Migrations**
1. Reapply the initial migration for the `admin` app without running it:
   ```bash
   docker-compose exec web python manage.py migrate admin 0001 --fake
   ```

2. Reapply all subsequent `admin` migrations:
   ```bash
   docker-compose exec web python manage.py migrate admin
   ```

---

### **Step 3: Reapply `accounts` Migrations**
Once the `admin` migrations are fixed, apply the `accounts` migrations:
```bash
docker-compose exec web python manage.py migrate accounts
```

---

### **Step 4: Apply Remaining Migrations**
Finish applying all other migrations:
```bash
docker-compose exec web python manage.py migrate
```

---

### **Additional Notes**
- This solution resets the migration history for `admin`, which resolves dependency mismatches.
- The `--fake` option ensures that the database schema remains intact if the migrations have already been applied previously.

---

### Summary of Commands
Run these commands in sequence:

```bash
# Step 1: Reset admin migration history
docker-compose exec db psql -U myuser myblogdb
DELETE FROM django_migrations WHERE app = 'admin';
\q

# Step 2: Fake reapply admin migrations
docker-compose exec web python manage.py migrate admin 0001 --fake
docker-compose exec web python manage.py migrate admin

# Step 3: Apply accounts migrations
docker-compose exec web python manage.py migrate accounts

# Step 4: Apply remaining migrations
docker-compose exec web python manage.py migrate
```

---

This should resolve the migration inconsistencies. Let me know how it goes!


----------------------------


The error persists because Django is trying to recreate the `django_admin_log` table, which already exists in the database. This happens when migration history and the actual database state are out of sync.

To resolve this, we need to fake the migration for the `admin` app to mark it as applied without reapplying it.

---

### **Step-by-Step Solution**

#### **1. Fake Apply the `admin` Migration**
Mark the `admin` migration as applied to avoid attempting to recreate existing tables.

Run the following command:
```bash
docker-compose exec web python manage.py migrate admin --fake
```

---

#### **2. Apply All Remaining Migrations**
After faking the `admin` migration, apply any other unapplied migrations:
```bash
docker-compose exec web python manage.py migrate
```

---

#### **3. Verify the Database**
Check if all migrations are properly applied and the database is in sync.

1. Access PostgreSQL:
   ```bash
   docker-compose exec db psql -U myuser myblogdb
   ```

2. Check the migration history:
   ```sql
   SELECT * FROM django_migrations ORDER BY applied;
   ```

Ensure the `admin` migration (`0001_initial`) is listed as applied.

---

#### **4. Restart the Django Development Server**
Restart the Django server to ensure all changes are loaded properly:
```bash
docker-compose restart web
```

---

### Recap of Commands

1. Fake apply the `admin` migration:
   ```bash
   docker-compose exec web python manage.py migrate admin --fake
   ```

2. Apply all migrations:
   ```bash
   docker-compose exec web python manage.py migrate
   ```

3. Verify the database:
   ```bash
   docker-compose exec db psql -U myuser myblogdb
   SELECT * FROM django_migrations ORDER BY applied;
   ```

4. Restart the server:
   ```bash
   docker-compose restart web
   ```

---

This should resolve the issue by ensuring Django does not attempt to recreate existing tables. If you encounter further problems, let me know!


----------------------------------------------

### **Summary of the Problem**

The core issue was an **inconsistent migration history**, where Django's migration records did not align with the actual state of the database. Here’s a breakdown of what went wrong and how it was resolved:

---

### **Key Issues**

1. **Inconsistent Migration Dependencies**
   - The `admin` app migration (`0001_initial`) was applied before its dependency on the `accounts` app migration (`0001_initial`), violating Django's migration dependency rules.

2. **Existing Tables Conflicting with Migrations**
   - Some tables, like `django_admin_log`, already existed in the database, but Django attempted to recreate them during migration, causing `ProgrammingError: relation "django_admin_log" already exists`.

3. **Mismatched Migration Records**
   - Migration records in the `django_migrations` table did not reflect the true state of the database. For example:
     - Django thought the `accounts` migration was applied, but the `accounts_customuser` table didn’t exist.
     - The `admin` migration was trying to create tables that already existed.

4. **Manual Database Operations**
   - Some manual interventions (e.g., clearing `django_migrations` records for `accounts`) temporarily resolved issues but led to additional dependency conflicts.

---

### **Steps Taken to Resolve**

1. **Cleared and Reapplied Migrations**
   - Removed conflicting migration records from the `django_migrations` table for both `accounts` and `admin` apps.
   - Regenerated migration files for `accounts` to ensure they were correct.
   - Reapplied the `accounts` migration successfully.

2. **Faked Migrations for Existing Tables**
   - Used the `--fake` flag to mark migrations as applied without executing them for tables like `django_admin_log` that already existed.

3. **Synchronized Migration History**
   - Ensured all migration records in `django_migrations` matched the actual state of the database.
   - Applied all remaining migrations cleanly.

4. **Tested the Application**
   - Verified that key functionalities, such as creating a superuser and accessing the admin panel, worked correctly.

---

### **Root Cause**
The problem originated from:
- Clearing or modifying migration history without resetting the database schema entirely.
- Dependencies between apps (`accounts` and `admin`) not being respected during migration, leading to order-of-operations issues.

---

### **Lessons Learned**

1. **Respect Migration Dependencies**
   - Ensure dependent migrations (e.g., `accounts.0001_initial` before `admin.0001_initial`) are applied in the correct order.

2. **Avoid Partial Database Resets**
   - If clearing migration history, reset the entire database (`DROP DATABASE` + `CREATE DATABASE`) to ensure a clean state.

3. **Use `--fake` Judiciously**
   - Use the `--fake` flag to mark migrations as applied only when tables already exist and match the expected schema.

4. **Test Incrementally**
   - Regularly test migrations and database state after changes to avoid compounding issues.

---

### **Outcome**
After aligning migration history, cleaning up inconsistencies, and applying all migrations, the application now works as expected. The admin panel and `accounts_customuser` functionality are fully operational. 🎉
