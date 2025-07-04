"""Universal document loader for the `health_rag` module.

Supports a wide range of file types using `langchain` document loaders.
Automatically detects file extension and delegates loading to the appropriate loader.

Supported file types:
- Text: .txt, .md, .pdf, .json, .csv
- Office: .docx, .xlsx, .xls
- Email: .eml
- Images: .png, .jpg, .jpeg, .tiff, .bmp
"""

import os
from typing import Callable, Iterator, List

from langchain_community.document_loaders import (
    Docx2txtLoader,
    UnstructuredEmailLoader,
    UnstructuredExcelLoader,
    UnstructuredFileLoader,
    UnstructuredMarkdownLoader,
    UnstructuredPDFLoader,
)
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.document_loaders.image import UnstructuredImageLoader
from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document

from constant import SUPPORTED_FILE_TYPES, SUPPORTED_IMAGE_TYPES

EXTENSION_LOADER_MAP: dict[str, Callable[[str], BaseLoader]] = {
    ".csv": lambda path: CSVLoader(path),
    ".eml": lambda path: UnstructuredEmailLoader(path),
    ".xlsx": lambda path: UnstructuredExcelLoader(path),
    ".xls": lambda path: UnstructuredExcelLoader(path),
    ".docx": lambda path: Docx2txtLoader(path),
    ".md": lambda path: UnstructuredMarkdownLoader(path),
    ".txt": lambda path: UnstructuredFileLoader(path),
    ".pdf": lambda path: UnstructuredPDFLoader(path),
}


class DocumentLoader:
    """Load a document from a supported file type using LangChain-compatible loaders.

    Automatically detects the file extension and delegates to the appropriate
    document loader from `langchain_community`.

    Supported file types:
        - PDF (.pdf)
        - Text (.txt, .md)
        - Word (.docx)
        - Excel (.xlsx, .xls)
        - CSV (.csv)
        - Email (.eml)
        - Images (.png, .jpg, .jpeg, .tiff, .bmp)

    Examples:
        from document_loader import DocumentLoader

        loader = DocumentLoader("data/report.pdf")
        docs = loader.load()

    """

    def __init__(self, file_path: str):
        """Initialize DocumentLoader.

        Args:
            file_path (str): Path to the document to load.

        Raises:
            ValueError: If the file type is not supported.

        """
        self._file_path = file_path
        self._file_extension = os.path.splitext(self._file_path)[1].lower()

        # Validate file type
        if self._file_extension not in SUPPORTED_FILE_TYPES:
            raise ValueError(f"File type '{self._file_extension}' is not supported.")

        self._file_loader: BaseLoader = self._select_loader()

    def _select_loader(self) -> BaseLoader:
        """Select appropriate loader based on file extension."""
        if self._file_extension in SUPPORTED_IMAGE_TYPES:
            return UnstructuredImageLoader(self._file_path)

        loader = EXTENSION_LOADER_MAP.get(self._file_extension)
        if loader:
            return loader(self._file_path)

        raise ValueError(f"File type '{self._file_extension}' is not supported.")

    def load(self) -> List[Document]:
        """Load the document fully using the LangChain loader.

        This method loads the entire document content into memory.
        See LangChain's documentation for more details on loader behavior.

        Returns:
            List[Document]: List of documents loaded from the file using LangChain.

        """
        return self._file_loader.load()  # type: ignore

    def lazy_load(self) -> Iterator[Document]:
        """Lazily load the document using the LangChain loader.

        This method yields documents one at a time as they are loaded,
        which is memory efficient for large documents.
        See LangChain's documentation for more details on loader behavior.

        Returns:
            Iterator[Document]: Iterator over documents loaded from the file using LangChain.

        """
        return self._file_loader.lazy_load()  # type: ignore
