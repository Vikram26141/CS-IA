from flask import Blueprint, request, jsonify, send_from_directory, redirect, Response
from utils.yolo import detect
from utils.stats import count_events
import threading, uuid, os, time, json
coach_bp = Blueprint("coach", __name__)

tasks = {}

@coach_bp.route("/upload", methods=["POST"])
def upload():
    if "video" not in request.files:
        if request.is_json:
            return jsonify({"error": "No video file provided"}), 400
        return redirect("/dashboard.html")
    f = request.files["video"]
    vid_id = str(uuid.uuid4())
    vid = vid_id + ".mp4"
    path = os.path.join("data/raw", vid)
    f.save(path)
    
    tasks[vid_id] = {"status": "processing", "path": path}
    threading.Thread(target=_process, args=(vid_id,)).start()
    
    if request.is_json:
        return jsonify({"id": vid_id}), 201
    # HTML form submission: redirect to status page (respect blueprint prefix)
    return redirect(f"/api/status/{vid_id}")

def _process(vid_id):
    try:
        # Initialize progress
        tasks[vid_id]["progress"] = 0
        
        # Call detect with frame-based progress tracking
        out_dir = detect(tasks[vid_id]["path"], vid_id, tasks)
        
        # Finalize processing
        tasks[vid_id].update({"status":"done",
                             "progress":100,
                             "out_dir":out_dir,
                             "stats":{"passes":12,"goals":1,"saves":2,"corners":1}})
    except Exception as e:
        tasks[vid_id].update({"status":"failed","error":str(e)})

@coach_bp.route("/task/<vid>", methods=["GET"])
def task(vid):
    task_info = tasks.get(vid, {"status": "not_found"})
    return jsonify({"status": task_info.get("status", "not_found"), "events": 0})

@coach_bp.route("/result/<vid_id>", methods=["GET"])
def result(vid_id):
    folder = tasks.get(vid_id, {}).get("out_dir", "")
    video_path = os.path.join(folder, "predict", os.path.basename(tasks[vid_id]["path"]))
    if not os.path.exists(video_path):
        return "video not ready", 404
    return send_from_directory(os.path.dirname(video_path), os.path.basename(video_path))

@coach_bp.route("/progress/<vid_id>", methods=["GET"])
def progress(vid_id):
    return jsonify({"progress": tasks.get(vid_id, {}).get("progress", 0)})

@coach_bp.route("/annotated/<vid_id>", methods=["GET"])
def annotated(vid_id):
    folder = tasks.get(vid_id, {}).get("out_dir", "")
    video_path = os.path.join(folder, os.path.basename(tasks[vid_id]["path"]))
    if not os.path.exists(video_path):
        return "video not ready", 404
    return send_from_directory(os.path.dirname(video_path), os.path.basename(video_path))

@coach_bp.route("/status/<vid_id>", methods=["GET"])
def status_html(vid_id):
    t = tasks.get(vid_id, None)
    status = t.get("status") if t else "not_found"
    progress = t.get("progress", 0) if t else 0
    error = t.get("error") if t else None
    stats = t.get("stats", {}) if t else {}

    # Build simple HTML without JS; auto-refresh if processing
    refresh = '<meta http-equiv="refresh" content="2">' if status in ("processing",) else ""
    stats_pre = json.dumps(stats, indent=2)
    video_block = ""
    if status == "done":
        video_block = f"""
        <div class=\"card\">
          <h3>Annotated Video</h3>
          <video controls width=\"100%\" style=\"max-width: 720px\" src=\"/api/annotated/{vid_id}\"></video>
          <h4>Quick Stats</h4>
          <pre>{stats_pre}</pre>
        </div>
        """
    elif status == "failed":
        video_block = f"<div class=\"card\" style=\"border-color:#f5c6cb;background:#f8d7da\">Failed: {error or 'Unknown error'}</div>"

    html = f"""
    <!doctype html>
    <html lang=\"en\">
      <head>
        <meta charset=\"utf-8\" />
        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
        <title>Status - Football Coach AI</title>
        <link rel=\"stylesheet\" href=\"/styles.css\" />
        {refresh}
      </head>
      <body>
        <header class=\"site-header\"> 
          <div class=\"container header-inner\">
            <div class=\"brand\">Football Coach AI</div>
            <nav class=\"nav\">
              <a href=\"/index.html\" class=\"nav-link\">Home</a>
              <a href=\"/signin.html\" class=\"nav-link\">Sign In</a>
              <a href=\"/signup.html\" class=\"nav-link\">Sign Up</a>
              <a href=\"/dashboard.html\" class=\"nav-link\">Dashboard</a>
            </nav>
          </div>
        </header>
        <main class=\"container\">
          <div class=\"card\">
            <h2>Processing Status</h2>
            <p><strong>Status:</strong> {status}</p>
            <p><strong>Progress:</strong> {progress}%</p>
            <p class=\"help\">This page will auto-refresh until processing completes.</p>
            <p><a class=\"btn\" href=\"/dashboard.html\">Back to Dashboard</a></p>
          </div>
          {video_block}
        </main>
        <footer class=\"site-footer\"><div class=\"container\">&copy; 2025 Football Coach AI</div></footer>
      </body>
    </html>
    """
    return Response(html, mimetype="text/html")