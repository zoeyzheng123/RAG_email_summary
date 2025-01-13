import argparse
from src import api
from src.transform import answer_question_with_ollama


class SafeArgumentParser(argparse.ArgumentParser):
    """Prevents silent SystemExit on missing required argument"""
    def exit(self, status=0, message=None):
        if status:
            raise RuntimeError(message)
        exit(status)

def get_parser():
    arg_parser = SafeArgumentParser(description="rag")

    arg_parser.add_argument(
        "--question",
        type=str,
        help="query for RAG, e.g. which meetings do i have",
        required=True
    )

    arg_parser.add_argument(
        "--max_result",
        type=int,
        help="max number of documents the retriever can return",
        default=20,
        required=False
    )
    return arg_parser


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    parser = get_parser()
    args, _ = parser.parse_known_args()
    maxResult = args.max_result
    question = args.question
    vector_store = api.fetch_and_store_emails(maxResult)
    answers = answer_question_with_ollama(vector_store, question)
    print(answers)


if __name__ == "__main__":
    main()
