# PDF ko load krke usko markdown mai convert krte
from pathlib import Path
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions

def convert_pdf_to_markdown(pdf_path: str) -> None:
    """
    Convert a PDF into markdown format using docling
    Args:
        pdf_path (str) : Path to the PDF file
    """

    pipeline = PdfPipelineOptions()
    pipeline.do_table_structure = True
    pipeline.do_ocr = False
    pipeline.images_scale = 2.0
    pipeline.generate_picture_images = True
    pipeline.do_formula_enrichment = True

    converter = DocumentConverter(
        format_options = {
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pipeline
            )
        }
    )
    generate_file = []
    output_folder = Path("/Users/abhinavdwivedi/Desktop/ResearchAgent/data")
    output_folder.mkdir(parents=True, exist_ok=True)

    pdf_files = iter_pdf_files(pdf_path)

    for pdf in pdf_files:
        try:
            result = converter.convert(str(pdf))
            md_content = result.document.export_to_markdown()

            output_file = output_folder / f"{pdf.stem}.md"
            output_file.write_text(md_content, encoding="utf-8")
            generate_file.append(str(output_file))
            print(f"Successfully converted {pdf} to {output_file}")
        except Exception as e:
            print(f"Error occurred while processing {pdf}: {e}")
        
    return generate_file


def iter_pdf_files(pdf_path: str):
    path = Path(pdf_path)

    if path.is_file():
        yield path

    elif path.is_dir():
        yield from path.glob("*.pdf")

