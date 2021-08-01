import PyPDF2
import pyttsx3
import requests
from bs4 import BeautifulSoup


# Scrape the source HTML of the article and return the text from that.
def content(url):
    response = requests.get(url)                            # Response 200 means request has succeeded
    if response.status_code != 200:
        print("Error fetching page!!!")
        exit()
    else:
        soup = BeautifulSoup(response.text, "html.parser")  # (raw HTML content, HTML parser we used)
        articles = []
        for i in range(len(soup.select(".p"))):             # Select everything with a class of `p`(Paragraph).
            article = soup.select(".p")[i].getText().strip()
            articles.append(article)
            contents = " ".join(articles)
        return contents


engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
engine.setProperty("rate", 150)


def pdf_reader():
    pdf_name = str(input("Enter PDF name with full location & extension (Format Eg.,: D:\\myfiles\welcome.pdf): "))
    pdf = open(pdf_name, "rb")
    pdfReader = PyPDF2.PdfFileReader(pdf)
    pages = pdfReader.numPages
    print(f"Total pages: {pages}")
    for num in range(pages):
        page = pdfReader.getPage(num)
        text = page.extractText()
        save(text)
        print("Reading...")
        speak(text)


# Speak the content using `pyttsx3` library.
def speak(text):
    engine.say(text)
    engine.runAndWait()


# Save audio file.
def save(text):
    while True:
        save_opt = str(input("Would you like to save it as an audio file? (y/n): "))
        if save_opt.lower() == "y" or save_opt.lower() == "yes":
            file_name = str(input("Enter file name: "))
            engine.save_to_file(text, f"{file_name}.mp3")
            engine.runAndWait()
            return
        elif save_opt.lower() == "n" or save_opt.lower() == "no":
            return
        else:
            print("Invalid Input!!!...Try again.")


while True:
    print("\n--------------------------------------------------------------------\n")
    print("1-Read from Website\n2-Read from PDF\n3-Read from User Input\n4-Exit\n")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        url = str(input("Paste article URL: "))
        contents = content(url)
        save(contents)
        while True:
            print_opt = str(input("Would you like to print the content as well? (y/n): "))
            if print_opt.lower() == "y" or print_opt.lower == "yes":
                print(contents)
                break
            elif print_opt.lower() == "n" or print_opt.lower() == "no":
                break
            else:
                print("Invalid Input!!!...Try again.")
        print("\nReading...")
        speak(contents)
        break

    elif choice == 2:
        pdf_reader()
        break

    elif choice == 3:
        user_input = str(input("Enter text: "))
        save(user_input)
        print("\nReading...")
        speak(user_input)
        break

    elif choice == 4:
        exit()

    else:
        print("\nInvalid choice!!!")
