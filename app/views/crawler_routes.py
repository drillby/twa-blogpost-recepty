import datetime

from flask import Response, request, send_from_directory

from app import app, db

from ..models.models import Recipe


@app.route("/robots.txt")
def robots():
    robots_txt = """User-agent: *
Disallow:
Sitemap: https://twa-blogpost-recepty.vercel.app/sitemap.xml"""
    return Response(robots_txt, mimetype="text/plain")


@app.route("/sitemap.xml")
def sitemap():
    pages = []

    # Statické stránky
    static_pages = [
        {
            "loc": "https://twa-blogpost-recepty.vercel.app/",
            "changefreq": "daily",
            "priority": "1.0",
            "lastmod": datetime.date.today().isoformat(),
        },
        {
            "loc": "https://twa-blogpost-recepty.vercel.app/account-settings",
            "changefreq": "monthly",
            "priority": "0.5",
            "lastmod": datetime.date.today().isoformat(),
        },
        {
            "loc": "https://twa-blogpost-recepty.vercel.app/add-recipe",
            "changefreq": "monthly",
            "priority": "0.6",
            "lastmod": datetime.date.today().isoformat(),
        },
    ]
    pages.extend(static_pages)

    # Dynamické recepty
    recipes = db.session.query(Recipe).all()
    for recipe in recipes:
        pages.append(
            {
                "loc": f"https://twa-blogpost-recepty.vercel.app/recipe/{recipe.id}",
                "changefreq": "weekly",  # Recepty se mohou občas měnit
                "priority": "0.8",
                "lastmod": (
                    recipe.created_at.date().isoformat()
                    if recipe.created_at
                    else datetime.date.today().isoformat()
                ),
            }
        )

    sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>'
    sitemap_xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    for page in pages:
        sitemap_xml += "<url>"
        sitemap_xml += f"<loc>{page['loc']}</loc>"
        sitemap_xml += f"<changefreq>{page['changefreq']}</changefreq>"
        sitemap_xml += f"<priority>{page['priority']}</priority>"
        sitemap_xml += f"<lastmod>{page['lastmod']}</lastmod>"
        sitemap_xml += "</url>"
    sitemap_xml += "</urlset>"

    response = Response(sitemap_xml, mimetype="text/xml")
    response.headers["Last-Modified"] = datetime.datetime.utcnow().strftime(
        "%a, %d %b %Y %H:%M:%S GMT"
    )
    return response
