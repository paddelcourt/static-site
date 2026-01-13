from website import static_to_public, generate_page


def main():
    static_to_public("static", "public")
    generate_page("content/index.md", "template.html","public/index.html")


main()