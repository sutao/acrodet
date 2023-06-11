#!/usr/bin/env python3
import csv
import re

import fire
from pypdf import PdfReader
from rich.progress import Progress, TextColumn, SpinnerColumn, BarColumn, MofNCompleteColumn, TimeElapsedColumn, \
    TimeRemainingColumn


PUNC = '!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~“”’‘，。：？'


class AcroDet:
    def __init__(self, filename, pages=None):
        self.filename = filename
        self.pages = pages
        self.acronyms = {}

    def extract_one_page(self, page):
        text = page.extract_text()
        words = re.sub('[' + PUNC + ']', '', text).split()
        matches = []
        for word in words:
            if sum([1 for c in word if c.isupper()]) < 3:
                continue
            if sum([1 for c in word if c.isdigit()]) > 0:
                continue
            matches.append(word)
        return matches

    def extract(self):
        reader = PdfReader(self.filename)
        number_of_pages = len(reader.pages)
        pages = list(self.pages or range(number_of_pages))

        with Progress(
            TextColumn(f"[bold green]Parsing {len(pages)} pages"),
            SpinnerColumn(),
            BarColumn(bar_width=20),
            "[progress.percentage]{task.percentage:>3.1f}%",
            "•",
            MofNCompleteColumn(),
            "•",
            TimeElapsedColumn(),
            "• ETA",
            TimeRemainingColumn(),
            SpinnerColumn()
        ) as progress:
            task = progress.add_task("parse", total=len(pages))
            parsed = 0
            for i in pages:
                words = self.extract_one_page(reader.pages[i])
                for word in words:
                    if word not in self.acronyms:
                        self.acronyms[word] = i
                parsed += 1
                progress.update(task, completed=parsed)

    def save(self, output_file):
        print(f"Saving to file {output_file}...")
        with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Acronym", "First Occurrence"])
            for word, page in self.acronyms.items():
                writer.writerow([word, page])

    def print(self):
        for word, page in self.acronyms.items():
            print(f"{word:40s}{page:-5d}")


def acrodet(file_name: str,
            start_page: int = None,
            end_page: int = None,
            output: str = "acronyms.csv",
            print_results: bool = False):
    """
    AcroDet - Acronym Detector
    :param file_name: Full path to the PDF file to be parsed
    :param start_page: Start page if you want to parse a subsection
    :param end_page: End page if you want to parse a subsection
    :param output: Output CSV file for the result
    :param print_results: Print result to screen if set
    :return: None
    """
    print(f"AcroDet - Acronym Detector")
    print(f"file_name = {file_name}")
    print(f"pages = {start_page} - {end_page}")
    print(f"output = {output}")
    print(f"print_results = {print_results}")

    if start_page is None or end_page is None:
        pages = None
    else:
        pages = range(start_page, end_page)

    ad = AcroDet(file_name, pages)
    ad.extract()
    ad.save(output)
    if print_results:
        ad.print()


if __name__ == "__main__":
    fire.Fire(acrodet)
