#!/bin/bash

# Define variables
SUPERVISOR_CONF_DIR=/etc/supervisor/conf.d

# Copy Supervisor configuration file to the appropriate directory
sudo cp /home/icat-api/configs/conf.d/celerybeatd.conf $SUPERVISOR_CONF_DIR/
sudo cp /home/icat-api/configs/conf.d/celeryd.conf $SUPERVISOR_CONF_DIR/

# Update Supervisor configurations
sudo supervisorctl reread
sudo supervisorctl update

# Start Celery worker and beat processes
sudo supervisorctl restart celerybeat celery
