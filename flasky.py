# -*- coding:utf-8 -*-
import os
import sys
import click
import coverage
from flask import jsonify
from apps import app

COV = None
if os.environ.get('FLASK_COVERAGE'):
    COV = coverage.coverage(branch=True, include='apps/*')
    COV.start()


@app.shell_context_processor
def make_shell_context():
    return dict(app=app)


@app.cli.command()
@click.option('--coverage/--no-coverage', default=False,
              help='Run tests under code coverage.')
def test(coverage):
    """Run the unit tests."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import subprocess
        os.environ['FLASK_COVERAGE'] = '1'
        sys.exit(subprocess.call(sys.argv))

    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()


@app.cli.command()
@click.option('--length', default=25,
              help='Number of functions to include in the profiler report.')
@click.option('--profile-dir', default=None,
              help='Directory where profiler data files are saved.')
def profile(length, profile_dir):
    """Start the application under the code profiler."""
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgiapp = ProfilerMiddleware(app.wsgiapp, restrictions=[length],
                                     profile_dir=profile_dir)
    app.run()


@app.errorhandler(400)
def bad_request(e):
    return jsonify({
        "Code": 400,
        "Message": str(e)
    }), 400


@app.errorhandler(404)
def not_found(e):
    return jsonify({
        "Code": 404,
        "Message": str(e)
    }), 404
    # return "URL Not Found!"


@app.errorhandler(500)
def error_500(e):
    return jsonify({
        "Code": 500,
        "Message": str(e)
    }), 500


@app.route("/")
def health_check():
    return "ok", 200


# 设置启动文件环境变量
#  set FLASKapp=flasky.py

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
