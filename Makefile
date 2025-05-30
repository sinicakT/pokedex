migrations: ## create new migrations after model changes
	python manage.py makemigrations
migrate: ## run already created mirgations
	python manage.py migrate
superuser: ## run createsuperuser
	python manage.py createsuperuser
init_app: ## run migrations and import data
	python manage.py migrate
	python manage.py createsuperuser
	python manage.py sync_all