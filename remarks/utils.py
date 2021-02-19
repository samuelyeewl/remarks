import json
import pathlib

import fitz  # PyMuPDF


def read_meta_file(path, suffix=".metadata"):
    file = path.with_name(f"{path.stem}{suffix}")
    if not file.exists():
        return None
    data = json.loads(open(file).read())
    return data


def is_document(path):
    metadata = read_meta_file(path)
    return metadata["type"] == 'DocumentType'


def get_document_filetype(path):
    content = read_meta_file(path, suffix=".content")
    return content["fileType"]


def get_visible_name(path):
    metadata = read_meta_file(path)
    return metadata["visibleName"]


def get_ui_path(path):
    metadata = read_meta_file(path)
    parent_filename = metadata["parent"]

    # Check the parent
    ui_path = pathlib.Path("")

    while parent_filename != "":
        # First get the total path of the parent
        parent_path = pathlib.Path(path.parent, metadata["parent"])

        # Get the meta data of this parent
        metadata = read_meta_file(parent_path)
        if not metadata:
            return pathlib.Path(".")

        parent_title = metadata["visibleName"]

        # These go in reverse order up to the top level
        ui_path = pathlib.Path(parent_title).joinpath(ui_path)

        # Get the parent of this one
        parent_filename = metadata["parent"]

    return ui_path


def get_pdf_page_dims(path, page_idx=0):
    with fitz.open(path.with_name(f"{path.stem}.pdf")) as doc:
        first_page = doc.loadPage(page_idx)
        return first_page.rect.width, first_page.rect.height


def list_pages_uuids(path):
    content = read_meta_file(path, suffix=".content")
    if "pages" in content:
        return content["pages"]
    else:
        return []


def list_ann_rm_files(path):
    content_dir = pathlib.Path(f"{path.parents[0]}/{path.stem}/")
    if not content_dir.is_dir():
        return None
    return list(content_dir.glob("*.rm"))
