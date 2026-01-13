from website import static_to_public, generate_pages_recursive
import sys


def main():
    static_to_public("static", "public")
    basepath = sys.argv
    generate_pages_recursive(f"{basepath}/content", "template.html",f"{basepath}/public")
    

main()