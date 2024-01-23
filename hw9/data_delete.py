from connection import connect
from models import Author, Quote


def delete_all_documents():
    # Delete all documents in the "author" collection
    Author.objects().delete()

    # Delete all documents in the "quote" collection
    Quote.objects().delete()

    print("All documents deleted successfully.")


if __name__ == "__main__":
    delete_all_documents()
