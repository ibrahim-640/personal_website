release: cd portfolio_site && python3 manage.py collectstatic --noinput && python3 manage.py migrate
web:    cd portfolio_site && gunicorn portfolio_site.wsgi:application --log-file -

