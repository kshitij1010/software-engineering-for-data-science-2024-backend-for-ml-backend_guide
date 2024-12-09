from flask import Blueprint, request, jsonify, current_app
import psycopg
import psycopg.rows

database_service = Blueprint("database", __name__)

# Database connection helper
def connect_postgres() -> psycopg.Connection[psycopg.rows.TupleRow]:
    database_client = psycopg.connect(
        host=current_app.config["POSTGRES_HOST"],
        port=current_app.config["POSTGRES_PORT"],
        user=current_app.config["POSTGRES_USER"],
        password=current_app.config["POSTGRES_PASSWORD"],
        dbname=current_app.config["POSTGRES_DB"],
        row_factory=psycopg.rows.dict_row
    )
    return database_client

@database_service.route("/create_table", methods=["POST"])
def create_table():
    try:
        with connect_postgres() as client:
            cursor = client.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS classes (id UUID PRIMARY KEY, name TEXT)"
            )
            client.commit()
        return jsonify({"message": "Table created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@database_service.route("/get_table", methods=["GET"])
def get_table():
    try:
        with connect_postgres() as client:
            cursor = client.cursor()
            cursor.execute("SELECT * FROM classes")
            results = cursor.fetchall()
            return jsonify({"data": results}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@database_service.route("/add_class", methods=["POST"])
def add_class():
    try:
        data = request.get_json()
        class_name = data.get("class")
        if not class_name:
            return jsonify({"error": "Class name is required"}), 400

        with connect_postgres() as client:
            cursor = client.cursor()
            cursor.execute(
                "INSERT INTO classes (id, name) VALUES (gen_random_uuid(), %s)",
                (class_name,)
            )
            client.commit()
        return jsonify({"message": "Class added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500