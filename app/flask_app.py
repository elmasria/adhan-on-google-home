import logging
import socket
import time

import pychromecast
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, jsonify, send_from_directory
from zeroconf import ServiceBrowser, Zeroconf

from app.app_types import IAppConfig
from app.bll import adhan_play

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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

    @app.route("/discover")
    def discover_chromecasts():
        """Discover Chromecast devices and return results"""
        devices = []

        # Method 0: Test manual IP from config
        chromecast_ip = app_config.get("chromecast_ip")
        if chromecast_ip:
            try:
                chromecasts, browser = pychromecast.get_chromecasts(known_hosts=[chromecast_ip])
                logger.info(f"Manual IP discovery for Chromecast at {chromecast_ip}")
                logger.info(f"Found {len(chromecasts)} devices at manual IP {chromecast_ip}")
                if chromecasts:
                    # Filter to only devices actually at this IP (known_hosts doesn't filter!)
                    devices_at_ip = [cc for cc in chromecasts if cc.cast_info.host == chromecast_ip]
                    logger.info(f"Found {len(devices_at_ip)} devices actually at IP {chromecast_ip}")

                    # Add all devices found at this IP
                    for device in devices_at_ip:
                        devices.append({
                            'name': device.name,
                            'ip': chromecast_ip,
                            'port': device.cast_info.port,
                            'method': 'manual_ip',
                            'status': 'connected'
                        })
                    browser.stop_discovery()
                else:
                    devices.append({
                        'ip': chromecast_ip,
                        'method': 'manual_ip',
                        'error': f'No Chromecast found at IP {chromecast_ip}'
                    })
            except Exception as e:
                devices.append({
                    'ip': chromecast_ip,
                    'method': 'manual_ip',
                    'error': f'Manual IP failed: {str(e)}'
                })

        # Method 1: mDNS Discovery
        try:
            zeroconf = Zeroconf()

            def on_service_state_change(zeroconf, service_type, name, state_change):
                if service_type == "_googlecast._tcp.local.":
                    info = zeroconf.get_service_info(service_type, name)
                    if info:
                        friendly_name = info.properties.get(b'fn', b'').decode('utf-8')
                        ip = socket.inet_ntoa(info.addresses[0])
                        port = info.port
                        devices.append({
                            'name': friendly_name,
                            'ip': ip,
                            'port': port,
                            'method': 'mDNS'
                        })

            browser = ServiceBrowser(zeroconf, "_googlecast._tcp.local.",
                                    handlers=[on_service_state_change])
            time.sleep(10)  # Wait for discovery
            browser.cancel()
            zeroconf.close()

        except Exception as e:
            devices.append({'error': f'mDNS failed: {str(e)}'})

        # Method 2: pychromecast
        try:
            chromecasts, browser = pychromecast.get_chromecasts(timeout=5)
            for cc in chromecasts:
                devices.append({
                    'name': cc.name,
                    'ip': cc.host,
                    'port': cc.port,
                    'method': 'pychromecast'
                })
            browser.stop_discovery()
        except Exception as e:
            devices.append({'error': f'pychromecast failed: {str(e)}'})

        return jsonify({
            'devices': devices,
            'total_found': len([d for d in devices if 'error' not in d]),
            'config': {
                'device_name': app_config.get('device_name'),
                'chromecast_ip': app_config.get('chromecast_ip')
            }
        })

    return app
