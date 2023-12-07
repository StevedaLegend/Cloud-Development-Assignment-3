from flask import Flask, render_template, request
import DBcm
import swim_utils
import hfpy_utils

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

    with DBcm.UseDatabase(config) as db:
        db.execute(get_dates_query)
        timestamps = db.fetchall()
    print(timestamps)
    dates = [row[0] for row in timestamps]

    return render_template("select.html", timestamps=dates)


@app.route("/display_swimmers", methods=["POST"])
def display_swimmers():
    selected_date = request.form.get("selected_date")

    with DBcm.UseDatabase(config) as db:
        db.execute(
            """
            SELECT id, name, age
            FROM swimmers
            WHERE id IN (
                SELECT DISTINCT swimmer_id
                FROM times
                WHERE DATE(ts) = %s
            )
            """,
            (selected_date,),
        )
        swimmer_data = db.fetchall()

    print("Swimmer Data:", swimmer_data)

    return render_template("events.html", swimmer_data=swimmer_data)


@app.post("/chart")
def display_chart():
    selected_swimmer = request.form.get("event")

    if selected_swimmer:
        with DBcm.UseDatabase(config) as db:
            db.execute(
                """
                SELECT id, name, age, distance, stroke, time, ts
                FROM swimmers
                JOIN times ON swimmers_id = times.swimmer_id
                WHERE swimmers_id = %s
                """,
                (selected_swimmer,),
            )
            swimmer_data = db.fetchall()

        return render_template(
            "chart.html",
            title=f"{swimmer_data[0]['name']} (Under {swimmer_data[0]['age']}) {swimmer_data[0]['distance']} {swimmer_data[0]['stroke']}",
            average=0,
            data=[],
        )


if __name__ == "__main__":
    app.run(debug=True)
