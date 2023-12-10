from flask import Flask, render_template, request
import DBcm

app = Flask(__name__)

config = {
    "user": "swimmeruser",
    "password": "swimmers",
    "database": "swimclubdb",
    "host": "localhost",
    "port": 3308,
}


@app.route("/")
def select_training_session():
    get_dates_query = """SELECT DISTINCT DATE(ts) AS Date FROM times"""
    # Fetch timestamps from the database
    with DBcm.UseDatabase(config) as db:
        db.execute(get_dates_query)
        timestamps = db.fetchall()
    print(timestamps)
    dates = [row[0] for row in timestamps]

    return render_template("events.html", timestamps=dates)


# @app.route("/display_swimmers", methods=["POST"])
# def display_swimmers():
#     selected_timestamp_id = request.form.get("timestamp_id")

#     if selected_timestamp_id:
#         # Fetch swimmers based on the selected timestamp from the database
#         with DBcm.UseDatabase(config) as db:
#             db.execute(
#                 """
#                 SELECT swimmer_id, event_id, time, ts
#                 FROM times
#                 WHERE timestamp_id = %s
#                 """,
#                 (selected_timestamp_id,),
#             )
#             swimmer_data = db.fetchall()

#         return render_template("select.html", swimmer_data=swimmer_data)


if __name__ == "__main__":
    app.run(debug=True)
