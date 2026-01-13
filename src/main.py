from website import static_to_public, generate_pages_recursive



def main():
    static_to_public("static", "public")
    generate_pages_recursive("content", "template.html","public")
    

main()