from langchain.document_loaders import TextLoader
from transformers import GPT2TokenizerFast
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import UnstructuredPDFLoader

SOURCE= "sample_data/bare_act.pdf"
# loader = TextLoader(SOURCE)
loader = UnstructuredPDFLoader(SOURCE)
docs = loader.load()
tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
text_splitter = CharacterTextSplitter.from_huggingface_tokenizer(
    tokenizer, chunk_size=750, chunk_overlap=25
)
print("Splitting")
chunks = text_splitter.split_documents(docs)
print("Done splitting", len(chunks))

for i, chunk in enumerate(chunks):
    content = chunk.page_content
    while "\n\n" in content:
        content = content.replace("\n\n", "\n")
    outFile = SOURCE.replace(".pdf", f"_{i}.txt")
    print(outFile)
    with open(outFile, "w+") as f:
        f.write(content)