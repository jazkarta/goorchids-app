Go Orchids Deployment Notes
===========================

This document describes the public, non-secret parts of the Go Orchids
deployment. Keep credentials, vault passwords, AWS keys, DNS account
access, and destructive maintenance runbooks outside this public
repository.

Architecture
------------

The deployed stack is Docker Compose:

* `goorchids`: Django served by Gunicorn
* `worker`: RQ worker for background jobs
* `postgres`: PostgreSQL database
* `solr`: Solr search index
* `redis`: Redis for background jobs
* `httpserver`: Traefik reverse proxy in staging and production overlays

Base services are defined in `docker-compose.yml`.

Deployment overlays:

* `docker-compose.staging.yml`: Traefik, HTTPS, Gunicorn, AWS-backed media
* `docker-compose.production.yml`: production host routing override

Ansible playbooks:

* `ansible/development.yml`: development host bootstrap and deploy
* `ansible/production.yml`: staging and production bootstrap and deploy

Inventory and public host settings:

* `ansible/inventory`
* `ansible/host_vars/development.yml`
* `ansible/host_vars/staging.yml`
* `ansible/host_vars/production.yml`

Required private material
-------------------------

A deployer needs access to the private operational materials for the
environment:

* SSH access to the target host
* Ansible vault password
* AWS access key and secret key for the relevant S3 bucket
* `GOBOTANY_DJANGO_SECRET_KEY`
* DNS provider access for hostname changes
* Any private runbook for database import/export and media cleanup

Do not add those values to this repository.

Environment variables
---------------------

The deployment playbooks write a `.env` file on the target host. The
Compose stack reads these variables:

* `COMPOSE_FILE`: compose files to combine
* `SERVER_NAME`: primary hostname
* `WWW_SERVER_NAME`: production `www` hostname
* `AWS_ACCESS_KEY_ID`: S3 access key
* `AWS_SECRET_ACCESS_KEY`: S3 secret key
* `AWS_STORAGE_BUCKET_NAME`: S3 bucket for media/static files
* `GOBOTANY_DJANGO_SECRET_KEY`: Django secret key
* `LETSENCRYPT_EMAIL`: optional Traefik ACME contact email

Staging currently uses:

    COMPOSE_FILE=./docker-compose.yml:./docker-compose.staging.yml

Production currently uses:

    COMPOSE_FILE=./docker-compose.yml:./docker-compose.staging.yml:./docker-compose.production.yml

DNS and SSL
-----------

Traefik terminates HTTPS and requests certificates from Let's Encrypt
using the TLS challenge configured in `docker-compose.staging.yml`.

Before deploying a new public hostname:

1. Point DNS for `SERVER_NAME` to the target host.
2. For production, point `WWW_SERVER_NAME` to the same host.
3. Confirm ports 80 and 443 are open to the public internet.
4. Start the Compose stack and check Traefik logs.

Useful commands on the server:

    docker compose logs -f httpserver
    docker compose ps

Deploy with Ansible
-------------------

Install Ansible dependencies locally:

    python -m pip install -r ansible/requirements.txt

Run Ansible from the `ansible/` directory so `ansible.cfg` is loaded and
the inventory and vault password file paths resolve as expected:

    cd ansible

Deploy the branch currently checked out on your workstation. The
playbooks determine the current branch with `git rev-parse --abbrev-ref
HEAD` and clone that branch on the server.

Deploy to staging:

    ansible-playbook production.yml --limit staging

Deploy to production:

    ansible-playbook production.yml --limit production

The playbook installs Docker, creates the deployment user, clones the
repository, writes `.env`, and runs:

    docker compose up -d

Manual deploy commands
----------------------

If you are already on a server in `/home/goorchids/goorchids-app`, common
manual checks are:

    git status
    git pull
    docker compose pull
    docker compose build goorchids
    docker compose up -d
    docker compose ps

Run migrations when application changes include database migrations:

    docker compose exec goorchids python manage.py migrate

Rebuild the Solr index after data imports, dump restores, or search
schema changes:

    docker compose exec goorchids python manage.py rebuild_index --noinput

Check the site:

    docker compose logs -f goorchids
    docker compose logs -f worker
    docker compose logs -f httpserver

Database backup and restore
---------------------------

Create a PostgreSQL custom-format dump on the server:

    docker compose exec -T postgres pg_dump -Fc -U postgres gobotany > goorchids-$(date +%Y%m%d).dump

Before restoring over an existing environment, confirm:

* which environment is the source of truth
* whether staging and production data are expected to match
* whether media cleanup or S3 audits depend on the database state
* that a fresh backup exists

Restore into an environment only after following the private operational
runbook for that environment.

S3 media
--------

The database stores references to content images. Deleting a
`ContentImage` record removes the database reference but does not
automatically delete the S3 object.

Do not delete S3 objects unless the private project runbook confirms that
the database and S3 bucket are in sync and the keys are safe to remove.
Any S3 cleanup should start with a read-only comparison of database image
references against bucket keys.

Post-deploy checklist
---------------------

After a deployment:

1. Confirm all containers are running:

       docker compose ps

2. Confirm the homepage responds.
3. Confirm the admin login page responds.
4. Check application, worker, and Traefik logs.
5. Run migrations if required by the release.
6. Rebuild the Solr index if data or search configuration changed.
7. Smoke test image pages and search.

Troubleshooting
---------------

If the site returns 502 or 503, check the app and Traefik logs:

    docker compose logs --tail=200 goorchids
    docker compose logs --tail=200 httpserver

If search fails, check Solr and rebuild the index:

    docker compose logs --tail=200 solr
    docker compose exec goorchids python manage.py rebuild_index --noinput

If background jobs fail, check Redis and the worker:

    docker compose logs --tail=200 redis
    docker compose logs --tail=200 worker

If S3 media fails, confirm the environment has the expected AWS variables
and that the IAM user has access to the configured bucket.
