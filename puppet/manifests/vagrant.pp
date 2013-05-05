
import "classes/*.pp"

include apt
include python
include nginx
include mysql
include supervisor

$database = "mysql://limetime:randompassword1234@localhost/limetime"

mysql::database{'limetime':
  user => 'limetime',
  password => 'randompassword1234'
}

python::venv {'limetime':
  path => "/usr/local/${name}-venv",
  requirements => '/vagrant/requirements.txt',
}

file{'/usr/local/bin/limetime-init.sh':
  content => "#!/bin/bash\n. /usr/local/main-venv/bin/activate\nDATABASE_URL=$database /usr/bin/env python manage.py run_gunicorn -c gunicorn_config --preload",
  ensure => present,
  mode => 755,
}

supervisor::program {'limetime':
  command => '/usr/local/bin/limetime-init.sh',
  directory => '/vagrant/app/',
  user => 'vagrant',
  require => [File['/usr/local/bin/limetime-init.sh'], Python::Venv['limetime'], Mysql::Database['limetime']],
}

nginx::gunicorn { 'limetime':
  ensure => enabled,
  host => '_',
  port => 3322,
  root => '/vagrant/root/',
  static => '/vagrant/static/',
}

exec{'limetime-collectstatic':
  command => "/usr/bin/env bash -c 'source /usr/local/main-venv/bin/activate; cd /vagrant/app;DATABASE_URL=$database /usr/bin/env python ./manage.py collectstatic --noinput'",
  path => '/usr/local/bin:/usr/bin:/bin',
  require => Python::Venv['limetime'],
}

exec{'limetime-syncdb':
  command => "/usr/bin/env bash -c 'source /usr/local/main-venv/bin/activate; cd /vagrant/app;DATABASE_URL=$database /usr/bin/env python ./manage.py syncdb --all --noinput'",
  path => '/usr/local/bin:/usr/bin:/bin',
  require => [Python::Venv['limetime'], Mysql::Database['limetime']],
}

exec{'limetime-migrationfake':
  command => "/usr/bin/env bash -c 'source /usr/local/main-venv/bin/activate; cd /vagrant/app;DATABASE_URL=$database /usr/bin/env python ./manage.py migrate --fake --noinput'",
  path => '/usr/local/bin:/usr/bin:/bin',
  require => Exec['limetime-syncdb'],
}