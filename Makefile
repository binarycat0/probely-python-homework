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

load_findings:
	poetry run python src/manage.py \
	load_findings \
	--pythonpath src \
	--settings probely.settings
