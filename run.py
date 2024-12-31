import os
import uvicorn

from app.common import config
from app.utils.common_utils import get_ttl_hash

if __name__ == "__main__":
    api_env = os.environ.get("API_ENV", "DEV")
    ttl_hash = get_ttl_hash()
    conf = config.get_config(
        ttl_hash=ttl_hash,
        api_env=api_env
    )

    uvicorn.run(
        "app.main:create_app",
        host="0.0.0.0",
        port=8088,
        factory=True,
        reload=conf.PROJECT_RELOAD
    )
