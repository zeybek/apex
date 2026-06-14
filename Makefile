SKILLS_REF_SOURCE ?= git+https://github.com/agentskills/agentskills@5d4c1fda3f786fff826c7f56b6cb3341e7f3a911\#subdirectory=skills-ref

.PHONY: validate validate-skills validate-distribution validate-official test

validate: validate-skills validate-distribution

validate-skills:
	python3 scripts/validate_package.py

validate-distribution:
	python3 scripts/validate_distribution.py

validate-official:
	@for skill in plugins/apex/skills/*; do \
		uvx --from "$(SKILLS_REF_SOURCE)" \
			skills-ref validate "$$skill" || exit 1; \
	done

test:
	uvx --with pytest-cov pytest tests/ --cov=scripts --cov-report=term-missing
