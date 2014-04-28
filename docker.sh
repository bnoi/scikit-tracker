###########
# How to use docker.sh
# $ export AUTO_TEST=true  # false will prompt you to a shell inside the container
# $ export DOCKER_IMAGE="hadim/py3-env"  # or hadim/py2-env
# $ export BRANCH="master"  # branch to build
###########

# If AUTO_TEST=true then scikit-tracker will be automatic
# If AUTO_TEST=false you will be prompted to a shell inside the container
AUTO_TEST=${AUTO_TEST:-true}
BRANCH=${BRANCH:-master}

DOCKER_IMAGE=${DOCKER_IMAGE:-hadim/py3-env}
DOCKER_CONTAINER="py-env"

TMP_BUILDER="/tmp/docker_builder_script"
CURRENT_DIR=$(pwd)

mkdir -p $TMP_BUILDER

builder="export PATH=/miniconda/bin:$PATH;
export BRANCH="$BRANCH";

cd /
git clone https://github.com/bnoi/scikit-tracker.git;
cd scikit-tracker/;
git checkout $BRANCH;

make init;

python setup.py build_ext --inplace;
python setup.py install;
python setup.py bdist_wheel;

nosetests sktracker --with-coverage --cover-package=sktracker -v;
make doc;"

printf "$builder" > $TMP_BUILDER/builder.sh

docker pull $DOCKER_IMAGE

docker rm -vf $DOCKER_CONTAINER 2> /dev/null

if [ "$AUTO_TEST" = true ] ; then
    docker run --name $DOCKER_CONTAINER -v $TMP_BUILDER:/builder:ro $DOCKER_IMAGE sh /builder/builder.sh
fi
    echo "You are now prompted to an interactive shell inside a container."
    echo "You can launch ./sh/builder/builder.sh to build scikit-tracker"
    docker run -i -t --name $DOCKER_CONTAINER -v $TMP_BUILDER:/builder:ro $DOCKER_IMAGE /bin/bash


