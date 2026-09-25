from datetime import datetime, timezone

from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    server_time = datetime.now(timezone.utc).isoformat()
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Benchmark D</title>
</head>
<body>
  <h1>Benchmark D</h1>
  <p>Current server time (UTC): <span id="server-time">{server_time}</span></p>

  <!-- Stage 3 will add a "Check health" button and its result area here. -->
  <div id="health-check"></div>
</body>
</html>
"""
    return html, 200, {"Content-Type": "text/html"}


if __name__ == "__main__":
    app.run(host="127.0.0.1")
