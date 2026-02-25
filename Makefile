install:
	uv pip install -r requirements.txt

test:
	PYTHONPATH=. pytest tests/

audit-self:
	python src/main.py --url $(REPO_URL)