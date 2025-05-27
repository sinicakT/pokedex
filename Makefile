migrations: ## create new migrations after model changes
	python manage.py makemigrations
migrate: ## run already created mirgations
	python manage.py migrate
superuser: ## run createsuperuser
	python manage.py createsuperuser