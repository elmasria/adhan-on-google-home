from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, jsonify, send_from_directory

from app.app_types import IAppConfig
from app.bll import adhan_play


def init_app(scheduler: BackgroundScheduler, app_config: IAppConfig):
    app = Flask(__name__)

    @app.route("/")
    def home():
        return jsonify({"status": "good"}), 200

    @app.route("/scheduler")
    def scheduler_route():
        jobs = scheduler.get_jobs()
        if not jobs:
            return jsonify({"message": "No jobs scheduled"})
        result = []
        for job in jobs:
            job_details = {
                "job_id": job.id,
                "job_function": str(job.func),
                "next_run_time": str(job.next_run_time),
            }
            result.append(job_details)
        return jsonify(result)

    @app.route("/test/<salat>")
    def test(salat):
        adhan_play(salat, app_config)
        return jsonify({"status": "good"}), 200

    @app.route("/play/<filename>")
    def play_song(filename):
        return send_from_directory("static", filename)

    return app
