Go Orchids
==========

Go Orchids is a Django application built on top of the vendored
Go Botany codebase in `external/gobotany-app`. The current development
and deployment workflow uses Docker Compose.

Repository setup
----------------

Clone the repository and initialize the Go Botany submodule:

    git clone git@github.com:jazkarta/goorchids-app.git
    cd goorchids-app
    git submodule update --init --recursive

Install Docker Engine or Docker Desktop with Docker Compose v2 support.
The project has been run with Docker 20.10+.

Local development with Docker
-----------------------------

Build the application image:

    docker compose build goorchids

Start the local stack:

    docker compose up -d

The local stack includes:

* `goorchids`: Django development server on `http://localhost:8000/`
* `worker`: RQ worker for background jobs
* `postgres`: PostgreSQL database named `gobotany`
* `solr`: Solr 6.6.5 on `http://localhost:8983/`
* `redis`: Redis for background jobs

Create the Solr core the first time a local volume is created:

    docker compose run --rm solr bash -c "bin/solr start && bin/solr create -c gobotany_solr_core -d /opt/solr/server/solr/configsets/basic_configs/"

Update the Solr schema from Django:

    docker compose up -d solr
    docker compose run -v goorchids-app_solr_data:/opt/solr/ --rm goorchids python manage.py build_solr_schema --configure-directory=/opt/solr/gobotany_solr_core/conf --reload-core=gobotany_solr_core

Run database migrations:

    docker compose exec goorchids python manage.py migrate

Create an admin user if you are using an empty database:

    docker compose exec goorchids python manage.py createsuperuser

Rebuild the search index after loading or restoring data:

    docker compose exec goorchids python manage.py rebuild_index --noinput

Visit the site at:

    http://localhost:8000/

Visit the admin at:

    http://localhost:8000/admin/

Using a staging database locally
--------------------------------

For realistic local testing, ask a maintainer for a current staging
PostgreSQL custom-format dump. Do not commit database dumps to this
repository.

To create a dump from the staging server, run this on the server from the
`goorchids-app` directory:

    docker compose exec -T postgres pg_dump -Fc -U postgres gobotany > goorchids-staging-$(date +%Y%m%d).dump

Copy the dump to your workstation, place it in the repository root, and
restore it into the local Docker database:

    docker compose stop goorchids worker
    docker compose exec -T postgres dropdb -U postgres --if-exists gobotany
    docker compose exec -T postgres createdb -U postgres gobotany
    docker compose exec -T postgres pg_restore -U postgres --no-owner --no-acl -d gobotany < goorchids-staging-YYYYMMDD.dump
    docker compose up -d
    docker compose exec goorchids python manage.py migrate --check
    docker compose exec goorchids python manage.py rebuild_index --noinput

If the dump contains server-specific extensions that do not exist in the
local container, inspect the dump table of contents before restoring:

    docker compose exec -T postgres pg_restore -l < goorchids-staging-YYYYMMDD.dump

Then create a filtered restore list and pass it to `pg_restore` with
`-L`. Ask a maintainer before filtering anything other than known
environment-specific extensions.

Common development commands
---------------------------

Open a Django shell:

    docker compose exec goorchids python manage.py shell

Run the Python tests:

    docker compose exec -e PYTHONDONTWRITEBYTECODE=1 goorchids python manage.py test

Run tests for one app:

    docker compose exec -e PYTHONDONTWRITEBYTECODE=1 goorchids python manage.py test goorchids.core

Run a management command:

    docker compose exec goorchids python manage.py <command>

Watch logs:

    docker compose logs -f goorchids

Restart the app containers after changing dependencies or environment:

    docker compose restart goorchids worker

Stop the local stack:

    docker compose down

Remove local Docker volumes and all local data:

    docker compose down -v

S3 and media
------------

Content images are stored in S3 when AWS credentials and
`AWS_STORAGE_BUCKET_NAME` are configured. Local development can run
without those credentials, but features that read or write production-like
media will not work.

Keep AWS credentials out of the repository. Use shell environment
variables, a local `.env` file that is not committed, or the deployment
vaults managed outside this public documentation.

Deployment
----------

Current deployment uses Docker Compose overlays and Ansible. Public,
non-secret deployment notes live in:

    docs/deployment.md

Deployment credentials, vault passwords, AWS access keys, DNS account
access, and any destructive cleanup procedure must be kept in the private
project runbook or password manager, not in this public repository.

Testing and adjusting search
----------------------------

The Go Orchids search feature uses Haystack and Solr.

Ranking relies mostly on Haystack document boosts in `search_indexes.py`.
Some hidden repeated keywords are also included in the `search_*.txt`
templates.

When adjusting ranking, rebuild the index and use the Solr admin
interface to inspect results:

    docker compose exec goorchids python manage.py rebuild_index --noinput

Solr admin:

    http://localhost:8983/solr/
