"""Resume parsing and text extraction module."""

import os
from typing import Optional
from PyPDF2 import PdfReader
from pathlib import Path
from .models import CandidateProfile


class ResumeParser:
    """Parser for extracting text from resume files."""
    
    SUPPORTED_FORMATS = {'.pdf', '.txt', '.docx'}
    
    @staticmethod
    def extract_text(file_path: str) -> str:
        """
        Extract text from various resume formats.
        
        Args:
            file_path: Path to the resume file
            
        Returns:
            Extracted text content
            
        Raises:
            ValueError: If file format is not supported
            IOError: If file cannot be read
        """
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext not in ResumeParser.SUPPORTED_FORMATS:
            raise ValueError(
                f"Unsupported file format: {file_ext}. "
                f"Supported formats: {ResumeParser.SUPPORTED_FORMATS}"
            )
        
        if file_ext == '.pdf':
            return ResumeParser._extract_from_pdf(file_path)
        elif file_ext == '.txt':
            return ResumeParser._extract_from_txt(file_path)
        elif file_ext == '.docx':
            return ResumeParser._extract_from_docx(file_path)
    
    @staticmethod
    def _extract_from_pdf(file_path: str) -> str:
        """Extract text from PDF file."""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text
        except Exception as e:
            raise IOError(f"Failed to read PDF file: {str(e)}")
    
    @staticmethod
    def _extract_from_txt(file_path: str) -> str:
        """Extract text from plain text file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            raise IOError(f"Failed to read text file: {str(e)}")
    
    @staticmethod
    def _extract_from_docx(file_path: str) -> str:
        """Extract text from Word document."""
        try:
            from docx import Document
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except ImportError:
            raise ImportError("python-docx is required for DOCX support")
        except Exception as e:
            raise IOError(f"Failed to read DOCX file: {str(e)}")
    
    @staticmethod
    def parse_resume(file_path: str) -> CandidateProfile:
        """
        Parse resume file and create CandidateProfile.
        
        Args:
            file_path: Path to the resume file
            
        Returns:
            CandidateProfile object with extracted information
        """
        text = ResumeParser.extract_text(file_path)
        
        profile = CandidateProfile(
            raw_text=text,
            technical_skills=[],
            domain_expertise=[],
            key_achievements=[],
            education=[],
            certifications=[]
        )
        
        return profile
