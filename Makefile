install:
	uv sync

audit-self:
	python src/main.py --url <repo_url>
