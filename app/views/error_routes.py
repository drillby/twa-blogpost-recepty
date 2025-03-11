from flask import render_template

from app import app


@app.errorhandler(Exception)
def handle_exception(e):
    return (
        render_template(
            "error.html",
            error_code=e.code if hasattr(e, "code") else 500,
            error_message=str(e),
        ),
        e.code if hasattr(e, "code") else 500,
    )
