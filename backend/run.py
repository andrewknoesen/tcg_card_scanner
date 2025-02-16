import os
from app import create_app
from flasgger import Swagger

app = create_app()
swagger = Swagger(app)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False,     # Disable debug in production
        threaded=True    # Enable threading for better performance
    )
