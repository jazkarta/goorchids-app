#!/bin/bash

set -e

django-admin.py update_index --remove --settings goorchids.settings
