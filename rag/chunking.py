from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    MarkdownHeaderTextSplitter,
)
from langchain_core.documents import Document
import os, json

PARENT_DIR = "./parent_dir"
PARENT_MIN_SIZE = 2000
PARENT_MAX_SIZE = 4000
CHILD_CHUNK_SIZE = 500
CHILD_OVERLAP = 100

parent_splitter = MarkdownHeaderTextSplitter([
        ("#", "H1"),
        ("##", "H2"),
        ("###", "H3"),
        ("####", "H4"),
    ])
child_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHILD_CHUNK_SIZE,
    chunk_overlap=CHILD_OVERLAP,
    separators=[
        "\n#### ",
        "\n### ",
        "\n## ",
        "\n\n",
        "\n",
        ". ",
        " ",
        ""
    ]
)
import re

def normalize_headings(md_text: str) -> str:
    """
    Convert numbered headings to proper markdown hierarchy.
    Example:
    ## 3 Method           -> # 3 Method
    ## 3.1 Dataset        -> ## 3.1 Dataset
    ## 3.1.1 Details      -> ### 3.1.1 Details
    ## 3.1.1.1 Something  -> #### 3.1.1.1 Something
    """

    new_lines = []

    for line in md_text.splitlines():

        match = re.match(r"^(#+)\s+(\d+(?:\.\d+)*)\s+(.*)", line)

        if match:
            number = match.group(2)
            title = match.group(3)

            level = number.count(".") + 1

            level = min(level, 4)

            line = "#" * level + f" {number} {title}"

        new_lines.append(line)

    return "\n".join(new_lines)

def divide_document_into_chunks(md_text : str , doc_name : str):
    md_text = normalize_headings(md_text)
    parent_chunks = parent_splitter.split_text(md_text)

    merged_parent_chunks = merge_small_parents(parent_chunks, PARENT_MIN_SIZE)
    final_parent_chunks = merge_large_parents(merged_parent_chunks, PARENT_MAX_SIZE)

    os.makedirs(PARENT_DIR, exist_ok=True)
    all_child_chunks = []
    for i, parent in enumerate(final_parent_chunks):
        parent_id = f"{doc_name}_parent_{i+1}"
        parent_data = {
            "page_content": parent.page_content,
            "metadata": {**parent.metadata, "source":doc_name, "parent_id": parent_id}
        }
        json_path = os.path.join(PARENT_DIR, f"{parent_id}.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(parent_data, f, ensure_ascii=False, indent=4)

        parent_doc = Document(
            page_content=parent_data["page_content"],
            metadata=parent_data["metadata"]
        )
        child_chunks = child_splitter.split_documents([parent_doc])

        for child in child_chunks:
            child.metadata["source"] = doc_name
            child.metadata["parent_id"] = parent_id
            all_child_chunks.append(child)

    return all_child_chunks

def merge_small_parents(parent_chunks, min_size):
    merged_chunks = []
    current= None

    for chunk in parent_chunks:
        if current is None:
            current = Document(
                page_content=chunk.page_content,
                metadata=chunk.metadata.copy()
            )
        else:
            if len(current.page_content)>=min_size:
                merged_chunks.append(current)
                current = Document(
                    page_content=chunk.page_content,
                    metadata=chunk.metadata.copy()
                )
            else:
                current.page_content += "\n" + chunk.page_content
            
    if current is not None:
        if len(current.page_content) >= min_size:
            merged_chunks.append(current)
        else:
            if merged_chunks:
                merged_chunks[-1].page_content += "\n" + current.page_content
            else:
                merged_chunks.append(current)
    return merged_chunks

def merge_large_parents(parent_chunks, max_size):
    final_chunks = []
    large_chunk_splitter = RecursiveCharacterTextSplitter(
        chunk_size=max_size,
        chunk_overlap=400
    )
    for chunks in parent_chunks:
        if len(chunks.page_content) > max_size:
            child_chunks = large_chunk_splitter.split_documents([chunks])
            final_chunks.extend(child_chunks)
        else:
            final_chunks.append(chunks)
    return final_chunks

