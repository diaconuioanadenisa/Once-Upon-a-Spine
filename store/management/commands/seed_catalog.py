from decimal import Decimal
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify
from store.models import Category, Product

CATALOG = [
    ("New Books", "new-books", "Fresh stories, ready for their first reader.", "new", [
        ("The Midnight Library", "Matt Haig", "A library between life and death offers infinite chances to try again.", "15.99", "#315B56"),
        ("The Very Secret Society of Irregular Witches", "Sangu Mandanna", "A cosy, hopeful story about found family and a little everyday magic.", "17.50", "#7D5546"),
        ("Tomorrow, and Tomorrow, and Tomorrow", "Gabrielle Zevin", "Two friends build worlds together in a sweeping story of creativity.", "18.25", "#D29B60"),
        ("Piranesi", "Susanna Clarke", "A strange house, an endless sea and a mystery waiting to be remembered.", "14.75", "#547A89"),
        ("Lessons in Chemistry", "Bonnie Garmus", "A spirited scientist changes the rules in and out of the kitchen.", "16.90", "#B95E48"),
        ("The Book of Form and Emptiness", "Ruth Ozeki", "A boy hears the stories of objects in a novel full of heart.", "19.00", "#9C7859"),
        ("Yellowface", "R. F. Kuang", "A sharp novel about authorship, ambition and the stories we claim.", "16.25", "#D2A33C"),
        ("The House in the Cerulean Sea", "TJ Klune", "A quiet caseworker finds an extraordinary family and a new home.", "17.25", "#5193A0"),
        ("Small Things Like These", "Claire Keegan", "A spare, moving story set in a small Irish town at Christmas.", "13.50", "#73534A"),
        ("The Creative Act", "Rick Rubin", "A thoughtful guide to noticing ideas and making room for creative work.", "22.00", "#7C7B66"),
        ("Crying in H Mart", "Michelle Zauner", "A tender memoir about food, family and learning to carry grief.", "16.00", "#B4776A"),
        ("A Psalm for the Wild-Built", "Becky Chambers", "A tea monk and a robot set out to discover what people need.", "15.25", "#7E9C76"),
    ]),
    ("Pre-owned Books", "pre-owned-books", "Loved before, ready for another chapter.", "preowned", [
        ("The Night Circus", "Erin Morgenstern", "A dreamlike competition unfolds beneath a black and white striped tent.", "8.50", "#443D48"),
        ("Circe", "Madeline Miller", "An exiled goddess finds her strength among mortals and monsters.", "9.25", "#A88C57"),
        ("The Secret History", "Donna Tartt", "An insular group of classics students follows a dangerous idea.", "10.00", "#62765D"),
        ("Never Let Me Go", "Kazuo Ishiguro", "An intimate story of friendship, memory and the shape of a life.", "7.75", "#71808A"),
        ("The Song of Achilles", "Madeline Miller", "A retelling of Achilles and Patroclus, full of tenderness and fate.", "9.00", "#B76E5D"),
        ("Convenience Store Woman", "Sayaka Murata", "An offbeat portrait of a woman who finds order in a Tokyo shop.", "8.25", "#D1A24E"),
        ("The Goldfinch", "Donna Tartt", "A painting carries a young man through loss and a changing world.", "11.50", "#A36B44"),
        ("Braiding Sweetgrass", "Robin Wall Kimmerer", "Botany, Indigenous knowledge and reciprocity meet in lyrical essays.", "12.00", "#58745A"),
        ("The Ocean at the End of the Lane", "Neil Gaiman", "A childhood memory opens onto an uncanny world at the edge of home.", "7.50", "#4D6577"),
        ("A Man Called Ove", "Fredrik Backman", "A stubborn neighbour discovers that community can surprise him.", "8.00", "#818176"),
    ]),
    ("Bookmarks", "bookmarks", "Little companions for the page you will return to.", "bookmark", [
        ("Pressed Flowers Bookmark", "Once Upon a Spine", "A keepsake bookmark with a pressed-flower inspired botanical print.", "4.50", "#789174"),
        ("Velvet Night Sky Bookmark", "Once Upon a Spine", "Soft midnight-blue velvet with a slim gold ribbon marker.", "5.25", "#435B7C"),
        ("Mushroom Garden Bookmark", "Once Upon a Spine", "A sturdy illustrated bookmark for woodland daydreamers.", "3.75", "#B8795B"),
        ("Brass Page Marker", "Once Upon a Spine", "A reusable brass clip that marks your place without folding a page.", "6.00", "#B28D4F"),
        ("Reading Cat Bookmark", "Once Upon a Spine", "A cheerful little cat illustration for readers who share their chair.", "3.50", "#D99D75"),
    ]),
    ("Accessories", "accessories", "Thoughtful details for a slower, lovelier reading ritual.", "accessory", [
        ("Reading Journal", "Once Upon a Spine", "A clothbound journal for quotes, ratings and the books that stay with you.", "14.00", "#8C6956"),
        ("Library Card Tote", "Once Upon a Spine", "A sturdy cotton tote inspired by old library checkout cards.", "18.00", "#A7A181"),
        ("Bookish Enamel Pin", "Once Upon a Spine", "A small hard enamel pin for jackets, bags and book club nights.", "8.00", "#C77E65"),
        ("Literary Candle", "Once Upon a Spine", "A gentle cedar and vanilla candle for a quiet evening chapter.", "16.50", "#D5B78C"),
        ("Book Sleeve", "Once Upon a Spine", "A padded cotton sleeve to keep your current read safe on the go.", "21.00", "#82928A"),
    ]),
]

class Command(BaseCommand):
    help = "Load the Once Upon a Spine sample catalogue and local demo account."
    @transaction.atomic
    def handle(self, *args, **options):
        total = 0
        for name, slug, description, kind, entries in CATALOG:
            category, _ = Category.objects.get_or_create(slug=slug, defaults={"name": name, "description": description})
            for index, (title, author, text, price, color) in enumerate(entries):
                Product.objects.get_or_create(slug=slugify(title), defaults={"title": title, "author": author, "category": category, "kind": kind, "description": text, "price": Decimal(price), "stock": 8 if kind != "preowned" else 1, "cover_color": color, "featured": index == 0})
                total += 1
        user_model = get_user_model()
        reader, created = user_model.objects.get_or_create(username="reader", defaults={"email": "reader@example.test"})
        if created:
            reader.set_password("ReadingRoom!2026")
            reader.save()
        self.stdout.write(self.style.SUCCESS(f"Loaded {total} products in {len(CATALOG)} categories."))
        self.stdout.write("Demo login: reader / ReadingRoom!2026")
