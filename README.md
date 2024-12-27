# Blog


1. virtualenv env
2. env\scripts\activate
3. pip install django~=5.0.4
4. git clone https://github.com/RamiSwa/Blog.git
5. rename Blog core
6. cd core
7. admin startproject myproject .
8. code .
9. git add .
11. git commit -m "Merged changes from remote branch and resolved conflicts in README.md"
[main 1ed553c] Merged changes from remote branch and resolved conflicts in README.md
12. git push

13. git checkout -b "main-1"
14. git push --set-upstream origin main-1
15. pip install python-decouple
16. pip install celery
17. pip install redis
18. pip install psycopg2-binary celery[redis] django-celery-results django-celery-beat:

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


19. pip freeze > requirements.txt
20. in settings.py add:

--------------------------------------------------------
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

---------------------------------------------------------

21. add .env
22. add gitignore:
    `
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

    `
--------------------------------------------------

  23. create file docker-compose.yml:
      `

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

      `

    ------------------------------------

24. create Dockerfile:
    `
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

    `

------------------------------------------------------

25. in Folder project near settings.py create celery.py:
    `
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

    `
  -----------------------------------------------

  26. create 2 folders static and media
  27. Now run `docker-compose up --build -d`
      this is rusults:
      ![image](https://github.com/user-attachments/assets/7c085606-58b1-4491-b7e7-4ac85085df27)

-------------------------------------
  28. `docker-compose exec web python manage.py startapp examples`
  29. add examples in INSTALLED_APPS
  30. `docker-compose exec web python manage.py makemigrations`

  31. compose exec web python manage.py migrate
  32. in examples add tasts.py:

      `
from celery import shared_task

@shared_task
def trial_task(x, y):
    return x + y

      `

  33. run `docker-compose exec web celery -A myproject worker --loglevel=info`
  34. run with another cmd `docker-compose exec web python manage.py shell`
  35. >>> from examples.tasks import trial_task
  36. >>> trial_task.delay(4, 5)
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
    
