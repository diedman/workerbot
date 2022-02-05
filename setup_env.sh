#!/bin/bash

echo TOKEN=$TOKEN >> .env
echo TOKEN_DEV=$TOKEN_DEV >> .env

#Add.gitlab-ci.yml. to before_script:
# - chmod +x ./setup_env.sh
# - ./setup_env.sh
