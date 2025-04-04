install:
	poetry install

run:
	poetry run python src/manage.py \
	runserver \
	--pythonpath src \
	--settings probely.settings

lint:
	poetry run black ./src;
	poetry run isort ./src;
	poetry run mypy .;

test:
	poetry run pytest

migrations:
	poetry run python src/manage.py \
	makemigrations \
	--pythonpath src \
	--settings probely.settings

migrate:
	poetry run python src/manage.py \
	migrate \
	--pythonpath src \
	--settings probely.settings

shell:
	poetry run python src/manage.py \
	shell -i ipython \
	--pythonpath src \
	--settings probely.settings

retrieve_findings:
	poetry run python src/manage.py \
	retrieve_findings \
	--pythonpath src \
	--settings probely.settings
