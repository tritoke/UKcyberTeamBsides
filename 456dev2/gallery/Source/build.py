from dataclasses import dataclass
import shutil
from typing import Optional
from jinja2 import Environment, select_autoescape, FileSystemLoader
import pathlib

out_path = pathlib.Path("dist")

env = Environment(
    loader=FileSystemLoader("templates/"),
    autoescape=select_autoescape()
)

@dataclass
class Image():
    url: str
    attribution: str
    alt: Optional[str] = None

@dataclass
class Gallery():
    slug: str
    name: str
    images: list[Image]
    description: Optional[str] = None

galleries = [
    Gallery(
        slug="cats",
        name="Cats",
        images=[
            Image(
                attribution="Birhanb, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons",
                url="/upload/Domestic_cat_with_harness.jpeg",
                alt="Domestic cat with harness"
                ),
            Image(
                attribution="E.E., CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons",
                url="/upload/Tiger_Tim.jpeg",
                alt="Norwegian orange male cat"
            ),
            Image(
                attribution="MichalPL, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons",
                url="/upload/Domestic_cat_in_Poland.jpeg",
                alt="Domestic cat in Poland"
            ),
            Image(
                url="/upload/Domestic_cat_in_Poland_2.jpeg",
                attribution="MichalPL, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons",
                alt="Domestic cat in Poland"
            ),
            Image(
                url="/upload/Domestic_Cat_Black_Sitting.jpeg",
                attribution="Anish Anilkumar, CC BY 4.0 <https://creativecommons.org/licenses/by/4.0>, via Wikimedia Commons",
                alt=" Domestic Cat Black sitting "
            )
            ],
        description="Aren't cats cute?"
    ),
    Gallery(
        slug="dogs",
        name="Dogs",
        images=[
            Image(
            attribution="Fernando Losada Rodríguez, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons",
            url="/upload/dog.jpeg",
            alt="Dog"
            ),
            Image(
                attribution="Richard Bartz, Munich Makro Freak, CC BY-SA 2.5 <https://creativecommons.org/licenses/by-sa/2.5>, via Wikimedia Commons",
                url="/upload/dog_cool.jpeg",
                alt="Siberian-Husky wearing sunglasses"
            )
        ]
    )

]

# copy static files

shutil.copytree("public/", out_path, dirs_exist_ok=True)


def render_and_save_file(file_name: str, context: dict, dest_file_name: Optional[str] =None):
    if dest_file_name is None:
        dest_file_name = file_name
    template = env.get_template(file_name)
    rendered = template.render(context)
    out_file = out_path / dest_file_name
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(rendered)
    
render_and_save_file("index.html", {"galleries": galleries})

for gallery in galleries:
    render_and_save_file("galleryview.html", {"gallery": gallery}, f"view/{gallery.slug}/index.html")