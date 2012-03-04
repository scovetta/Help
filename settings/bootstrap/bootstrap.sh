#!/bin/bash

echo "Grand Central Bootstrap Script"
echo "------------------------------"
# create_environment.sh
# Requirements
REQUIRED=(virtualenv git pip wget svn)
for required in ${REQUIRED[@]}; do
    hash ${required} 2>&- || { echo >&2 "${required} must be installed first. Aborting."; exit 1; }
done

# Create basic environment
ROOT=${1:-.}
cd $ROOT
ROOT=`pwd`
echo "Using root path: $ROOT"

cd $ROOT
echo "Creating project and app directories"
mkdir -p project app

echo "Creating virtualenv"
cd $ROOT/project
virtualenv --no-site-packages --distribute .

echo "Activating virtualenv"
source ./bin/activate

echo "Path is now $PATH"

echo "Cloning source code repository"
cd $ROOT/app
git clone "https://scovetta@github.com/cbsamp/Grand-Central.git" .
[ -f $ROOT/settings-development-private.ini ] && cp $ROOT/settings-development-private.ini ./settings

echo "Installing buildout"
cd $ROOT/project
wget "http://svn.zope.org/*checkout*/zc.buildout/trunk/bootstrap/bootstrap.py"
echo -e "[buildout]\nparts = \n" > ./buildout.cfg
python bootstrap.py

echo "Installing depdendencies"
cd $ROOT/app
# Do this three times in case of a network blip
./settings/virtualenv/install-modules.sh
./settings/virtualenv/install-modules.sh
./settings/virtualenv/install-modules.sh

echo "Creating ancillary directories"
cd $ROOT/project
mkdir -p cache db log pid sock tmp uploads static etc/nginx
touch log/application.log

export PYTHONPATH=$ROOT/app:$PYTHONPATH
export DJANGO_SETTINGS_MODULE=settings.settings

echo "Creating gcactivate and gcstart scripts"
echo "#!/bin/bash" > $ROOT/gcactivate.sh
echo "export PYTHONPATH=$ROOT/app/" >> $ROOT/gcactivate.sh
echo "export DJANGO_SETTINGS_MODULE=settings.settings" >> $ROOT/gcactivate.sh
echo "source $ROOT/project/bin/activate" >> $ROOT/gcactivate.sh

echo "#!/bin/bash" > $ROOT/gcstart.sh
echo "ROOT=$ROOT" >> $ROOT/gcstart.sh
echo "source $ROOT/project/bin/activate" >> $ROOT/gcstart.sh
echo "export PYTHONPATH=$PYTHONPATH" >> $ROOT/gcstart.sh
echo "export DJANGO_SETTINGS_MODULE=settings.settings" >> $ROOT/gcstart.sh
echo "python $ROOT/project/bin/django-admin.py run_gunicorn -b 0.0.0.0:8000" >> $ROOT/gcstart.sh
echo "deactivate" >> $ROOT/gcstart.sh

echo "#!/bin/bash" > $ROOT/gcsentry.sh
echo "export PYTHONPATH=$PYTHONPATH" >> $ROOT/gcsentry.sh
echo "watchmedo shell-command --patterns=\"*.py;*.html\" --recursive --command='kill -HUP `cat /tmp/gunicorn.pid`' $PYTHONPATH &" >> $ROOT/gcsentry.sh
chmod +x $ROOT/gcactivate.sh $ROOT/gcstart.sh $ROOT/gcsentry.sh

echo "Installing and configuring Nginx and Ngx-HTTP-Redis"
cd $ROOT/project/tmp
git clone https://github.com/git-mirror/nginx.git nginx
cd nginx
git checkout release-1.0.12
cd ..
wget http://people.freebsd.org/~osa/ngx_http_redis-0.3.5.tar.gz
tar zxvf ngx_http_redis-0.3.5.tar.gz

cd nginx
auto/configure --sbin-path=$ROOT/project/bin/nginx --conf-path=$ROOT/project/etc/nginx/nginx.conf --pid-path=$ROOT/project/pid/nginx.pid --with-http_ssl_module --prefix=$ROOT/project --add-module=../ngx_http_redis-0.3.5
make

echo "Creating database"
cd $ROOT/app
django-admin.py validate
django-admin.py syncdb --noinput
django-admin.py migrate
django-admin.py loaddata settings/initial_data/initial_data.json