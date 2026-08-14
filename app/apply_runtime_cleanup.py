#!/usr/bin/env python3
from pathlib import Path
import shutil

path = Path("app/main.py")
if not path.exists():
    raise SystemExit("ERROR: run this from the 333-network-local repository root.")
text = path.read_text(encoding="utf-8")
if "sovereign_runtime_ready" in text:
    print("ALREADY PATCHED: app/main.py")
    raise SystemExit(0)

backup = Path("app/main.py.pre-sovereign-runtime")
if not backup.exists():
    shutil.copy2(path, backup)

text = text.replace("import logging\n", "import logging\nimport os\n", 1)
text = text.replace("from app.core.database import database_health_check, dispose_engine\n", "")

old_start = '''    health = await database_health_check()\n    app.state.startup_database_health = health.to_dict()\n\n    if not health.ok:\n        LOGGER.warning(\n            "database_not_ready_at_startup",\n            extra={"database_status": health.status},\n        )\n        if settings.database_required_on_startup:\n            raise RuntimeError("Database is required but unavailable at startup.")\n\n'''
if old_start not in text:
    raise SystemExit("ERROR: expected database startup block was not found.")
text = text.replace(
    old_start,
    '''    app.state.sovereign_runtime_ready = bool(\n        os.getenv("OHMIC_UPSTREAM_URL", "").strip()\n        and len(os.getenv("OHMIC_GATEWAY_TOKEN", "").strip()) >= 32\n    )\n\n    if not app.state.sovereign_runtime_ready:\n        LOGGER.warning("ohmic_authority_not_ready_at_startup")\n\n''',
    1,
)

text = text.replace(
    '''        await rate_limiter.close()\n        await dispose_engine()\n        LOGGER.info(''',
    '''        await rate_limiter.close()\n        LOGGER.info(''',
    1,
)

old_ready = '''    @app.get("/ready", tags=["System"])\n    async def readiness() -> JSONResponse:\n        """Check configuration plus a live database connection."""\n        configuration = application_settings.configuration_readiness()\n        database = await database_health_check()\n\n        configuration_ready = all(configuration.values())\n        ready = database.ok and (\n            configuration_ready if application_settings.is_production else True\n        )\n\n        return JSONResponse(\n            status_code=200 if ready else 503,\n            content={\n                "ready": ready,\n                "mode": (\n                    "production"\n                    if application_settings.is_production\n                    else "development"\n                ),\n                "configuration": configuration,\n                "database": database.to_dict(),\n                "routers_loaded": list(app.state.routers_loaded),\n            },\n        )\n'''
new_ready = '''    @app.get("/ready", tags=["System"])\n    async def readiness() -> JSONResponse:\n        """Check the sovereign OHMIC authority seam; no external database is required."""\n        ohmic_ready = bool(\n            os.getenv("OHMIC_UPSTREAM_URL", "").strip()\n            and len(os.getenv("OHMIC_GATEWAY_TOKEN", "").strip()) >= 32\n        )\n        configuration = application_settings.configuration_readiness()\n        configuration.pop("database_url_configured", None)\n        configuration.pop("redis_url_configured", None)\n        configuration["ohmic_authority_configured"] = ohmic_ready\n\n        ready = ohmic_ready and (\n            all(configuration.values()) if application_settings.is_production else True\n        )\n\n        return JSONResponse(\n            status_code=200 if ready else 503,\n            content={\n                "ready": ready,\n                "mode": (\n                    "production"\n                    if application_settings.is_production\n                    else "development"\n                ),\n                "authority": "OHMIC Foundry",\n                "configuration": configuration,\n                "persistent_external_database_required": False,\n                "persistent_external_cache_required": False,\n                "routers_loaded": list(app.state.routers_loaded),\n            },\n        )\n'''
if old_ready not in text:
    raise SystemExit("ERROR: expected /ready block was not found.")
text = text.replace(old_ready, new_ready, 1)

path.write_text(text, encoding="utf-8")
print("PATCHED: app/main.py")
print("BACKUP: app/main.py.pre-sovereign-runtime")
