from flask import Flask, render_template, request
import os
import hfpy_utils
import swim_utils  # Assuming you have a swim_utils module

# Student Name: Steve Fasoranti
# Student Number: C00275756
app = Flask(__name__)


@app.route("/")
def get_swimmers_names():
    files = os.listdir(swim_utils.FOLDER)
    files.remove(".DS_Store")
    names = set()
    for swimmer in files:
        names.add(swim_utils.get_swimmers_data(swimmer)[0])
    return render_template(
        "select.html",
        title="Select a swimmer to chart",
        data=sorted(names),
    )


@app.route("/displayevents", methods=["POST"])
def display_events():
    selected_swimmer = request.form.get("swimmer")

    if selected_swimmer:
        files = os.listdir(swim_utils.FOLDER)
        files.remove(".DS_Store")

        events = [
            file
            for file in files
            if file.startswith(selected_swimmer) and file.endswith(".txt")
        ]

        txtremove = [event.removesuffix(".txt") for event in events]

        return render_template(
            "events.html",
            title="Select an event to chart",
            data=sorted(txtremove),
            selected_swimmer=selected_swimmer,
        )


@app.post("/chart")
def display_chart():
    selected_swimmer = request.form.get("event")

    if selected_swimmer:
        if not selected_swimmer.endswith(".txt"):
            selected_swimmer += ".txt"
        (
            name,
            age,
            distance,
            stroke,
            the_times,
            converts,
            the_average,
        ) = swim_utils.get_swimmers_data(selected_swimmer)

        the_title = f"{name} (Under {age}) {distance} {stroke}"
        from_max = max(converts) + 50
        the_converts = [
            hfpy_utils.convert2range(n, 0, from_max, 0, 350) for n in converts
        ]

        the_converts.reverse()
        the_times.reverse()

        the_data = zip(the_converts, the_times)

        return render_template(
            "chart.html",
            title=the_title,
            average=the_average,
            data=the_data,
        )


if __name__ == "__main__":
    app.run(debug=True)
