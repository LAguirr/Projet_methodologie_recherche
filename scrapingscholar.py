from bs4 import BeautifulSoup
import json

with open("schoolargoogle.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")
results = soup.find_all("div", class_="gs_r gs_or gs_scl")

data = []
for r in results:
    # Titre et lien
    title_tag = r.find("h3", class_="gs_rt")
    link_tag = title_tag.find("a") if title_tag else None

    # Auteurs et source
    author_tag = r.find("div", class_="gs_a")

    # Résumé (s’il existe)
    abstract_tag = r.find("div", class_="gs_rs")
    abstract = abstract_tag.text.strip() if abstract_tag else "N/A"

    # Mots-clés éventuels (certains liens sous la zone 'gs_fl')
    keywords_tags = r.select(".gs_fl a")
    keywords = [kw.text for kw in keywords_tags if kw.text and not kw.text.startswith("Cited")]

    data.append({
        "title": title_tag.text if title_tag else "N/A",
        "link": link_tag["href"] if link_tag else "N/A",
        "authors": author_tag.text if author_tag else "N/A",
        "abstract": abstract,
        "keywords": keywords if keywords else []
    })

with open("results_google_scholar.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"✅ {len(data)} résultats extraits depuis la page locale (titre, auteurs, résumé, mots-clés).")
