#!/bin/bash

set -e

django-admin.py update_index --remove --noinput --settings gobotany.settings
