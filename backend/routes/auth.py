from flask import Blueprint, request, jsonify, redirect
from utils.database import create_user, verify_user, init_database
auth_bp = Blueprint("auth", __name__)

# Initialize database on import
init_database()

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json(silent=True) or request.form
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        if request.is_json:
            return jsonify({"error": "Email and password required"}), 400
        return redirect("/signup.html")
    
    user_id = create_user(email, password)
    if user_id:
        if request.is_json:
            return jsonify({"msg": "User created successfully", "user_id": user_id}), 201
        # HTML form submission: go to dashboard
        return redirect("/dashboard.html")
    else:
        if request.is_json:
            return jsonify({"error": "User creation failed. Email may already exist."}), 400
        return redirect("/signup.html")

@auth_bp.route("/signin", methods=["POST"])
def signin():
    data = request.get_json(silent=True) or request.form
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        if request.is_json:
            return jsonify({"error": "Email and password required"}), 400
        return redirect("/signin.html")
    
    user_id = verify_user(email, password)
    if user_id:
        if request.is_json:
            return jsonify({"token": f"user-{user_id}", "user_id": user_id}), 200
        # HTML form submission: go to dashboard
        return redirect("/dashboard.html")
    else:
        if request.is_json:
            return jsonify({"error": "Invalid credentials"}), 401
        return redirect("/signin.html")