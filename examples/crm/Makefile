UV ?= $(shell which uv || echo uvx)
UVX ?= $(shell which uvx || echo uvx)

.PHONY: start install install-backend install-frontend

start: install
	$(UVX) honcho start

install: install-frontend install-backend

install-frontend:
	(cd frontend; pnpm install)

install-backend:
	$(UV) sync
