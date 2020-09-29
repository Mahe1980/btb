docker build --rm --build-arg UID=`id -u` --build-arg GID=`id -g` --no-cache --network=host -t dw-airflow .

# --rm
#    Remove intermediate containers
# --build-arg UID=`id -u` --build-arg GID=`id -g`
#    assign GID/UID of the host for permission
# --no-cache
#    Do not use cache when building the image
# --network=host
#    pickup host network by default instead of bridge network, to stop pip failing to download added
# -t dw-airflow
#    give container a tag
# .
#   Looks for DockerFile in current location for customisation in the container. i.e. lib install etc