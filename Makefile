.PHONY: backend frontend full

backend:
	@bash -c 'cd backend && source venv/bin/activate && uvicorn app.main:app --reload'

frontend:
	cd frontend && npm run dev

full:
	@bash -c 'cd backend && source venv/bin/activate && uvicorn app.main:app --reload &'
	cd frontend && npm run dev
