"""Module from graphs subpackage with routes for Dashboard features."""

__docformat__ = "google"

from collections import Counter

from flask import render_template, request, redirect, url_for, Blueprint
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots

from .utils import read_logs

graphs = Blueprint("graphs", __name__)


@graphs.route("/dashboard")
def dashboard():
    """Return the dashboard page.

    Returns:
        Rendered template with the dashboard page.
    """
    total_count, df = read_logs()

    # Generate Plotly subplots and create figure
    fig_line = px.line(
        df, x="day", y="mime_types_count", color="mime_types", title="MIME Types"
    )
    fig2_line = px.line(
        df, x="day", y="status_codes_count", color="status_codes", title="Status Codes"
    )
    fig = make_subplots(rows=1, cols=2, subplot_titles=("MIME Types", "Status Codes"))

    for i in range(len(fig_line.data)):
        fig.add_trace(fig_line.data[i], row=1, col=1)
    for i in range(len(fig2_line.data)):
        fig.add_trace(fig2_line.data[i], row=1, col=2)

    fig.update_xaxes(title_text="Day", row=1, col=1)
    fig.update_xaxes(title_text="Day", row=1, col=2)
    fig.update_yaxes(title_text="Count", row=1, col=1)
    fig.update_yaxes(title_text="Count", row=1, col=2)
    fig.update_layout(legend_title_text="MIME Types and Status Codes")

    # Convert the plot to HTML using Plotly's built-in function
    plot_html = fig.to_html(full_html=False)

    # Render the HTML template with the plot embedded
    return render_template(
        "dashboard.html",
        title="Dashboard",
        total_count_of_logs=total_count,
        plot_html=plot_html,
    )


@graphs.route("/dashboard/day/<int:day>")
def dashboard_day(day: int):
    """Return a dashboard of bar charts for a specific day.

    Args:
        day: Day to show the dashboard.

    Returns:
        Rendered template with the dashboard page.
    """

    if day == 0:
        selected_day = request.args.get("day", "1")
        return redirect(url_for("graphs.dashboard_day", day=selected_day))
    elif day > 365:
        return redirect(url_for("graphs.dashboard"))

    total_count, status_codes, mime_types = read_logs(day)
    status_codes_counter = Counter(status_codes)
    mime_types_counter = Counter(mime_types)

    # Generate Plotly plot with subplots
    fig = make_subplots(rows=1, cols=2, subplot_titles=("MIME Types", "Status Codes"))
    fig.add_trace(
        go.Bar(
            x=list(mime_types_counter.keys()),
            y=list(mime_types_counter.values()),
            name="MIME Types",
        ),
        row=1,
        col=1,
    )
    fig.update_xaxes(tickangle=45)
    fig.add_trace(
        go.Bar(
            x=list(status_codes_counter.keys()),
            y=list(status_codes_counter.values()),
            name="Status Codes",
        ),
        row=1,
        col=2,
    )

    # Convert the plot to HTML using Plotly's built-in function
    plot_html = fig.to_html(full_html=False)

    # Render the HTML template with the plot embedded
    return render_template(
        "dashboard.html",
        title=f"Dashboard at day {day}",
        total_count_of_logs=total_count,
        plot_html=plot_html,
    )
