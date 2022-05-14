run:
	uvicorn api.__main__:app --reload

db:
	psql -h /var/run/postgresql/ library -U nishant