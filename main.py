#!/usr/bin/env python3
"""
Adobe India Hackathon 2025 - Challenge 1a: PDF Outline Extraction
Main entry point for robust PDF outline extraction and structure analysis.
Standalone version adapted from the combined solution.
"""

import argparse
import json
import logging
import multiprocessing
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import List, Tuple, Dict, Any

from src.config import ExtractorConfig
from src.text_processor import TextProcessor
from src.heading_classifier import HeadingClassifier
from src.outline_hierarchy import OutlineHierarchy
from src.cache_manager import OutlineCache
from src.pdf_extractor import PDFOutlineExtractor

# Configure logging for clear terminal output
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('pdf_processor.log')
    ]
)
logger = logging.getLogger(__name__)


def display_banner():
    """Display the application banner"""
    print("\n" + "="*70)
    print("🚀 Adobe India Hackathon 2025 - Challenge 1a")
    print("📋 PDF Outline Extraction & Structure Analysis")
    print("="*70)
    print("🎯 Features:")
    print("   • Fast Processing: <10s for 50-page documents")
    print("   • Universal PDF Compatibility")
    print("   • Multilingual Support")
    print("   • Intelligent Structure Detection")
    print("="*70)


class RobustPDFProcessor:
    """Robust PDF processor with parallel processing and error handling"""
    
    def __init__(self, config: ExtractorConfig):
        self.config = config
        self.extractor = PDFOutlineExtractor(config)
        self.retry_config = {"max_retries": 3, "backoff_factor": 2}
    
    def process_pdf_with_retry(self, pdf_file: str, input_dir: str, output_dir: str) -> Tuple[str, float, bool]:
        """Process a single PDF with retry logic"""
        input_path = Path(input_dir) / pdf_file
        output_path = Path(output_dir) / f"{input_path.stem}.json"
        
        print(f"📄 Processing: {pdf_file}")
        start_time = time.time()
        
        success = False
        last_error = None
        
        for attempt in range(self.retry_config["max_retries"]):
            try:
                # Extract outline
                outline_data = self.extractor.extract_outline(str(input_path))
                
                # Save result
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, 'w', encoding='utf-8') as f:
                    import json
                    json.dump(outline_data, f, ensure_ascii=False, indent=2)
                
                success = True
                duration = time.time() - start_time
                
                # Display results
                outline_count = len(outline_data.get('outline', []))
                status = "✅" if success else "❌"
                print(f"   {status} Completed in {duration:.3f}s | Found {outline_count} outline items")
                
                break
                
            except Exception as e:
                last_error = e
                if attempt < self.retry_config["max_retries"] - 1:
                    wait_time = self.retry_config["backoff_factor"] ** attempt
                    print(f"   ⚠️  Attempt {attempt + 1} failed, retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    duration = time.time() - start_time
                    print(f"   ❌ Failed after {self.retry_config['max_retries']} attempts in {duration:.3f}s")
                    print(f"      Error: {str(last_error)}")
        
        duration = time.time() - start_time
        return pdf_file, duration, success
    
    def process_all_pdfs(self, input_dir: str, output_dir: str) -> List[Tuple[str, float, bool]]:
        """Process all PDFs in the input directory"""
        input_path = Path(input_dir)
        if not input_path.exists():
            logger.error(f"Input directory not found: {input_dir}")
            return []
        
        # Find all PDFs
        pdf_files = [f.name for f in input_path.iterdir() if f.suffix.lower() == '.pdf']
        if not pdf_files:
            logger.warning(f"No PDF files found in: {input_dir}")
            return []
        
        logger.info(f"🚀 Starting PDF processing...")
        logger.info(f"📁 Input: {len(pdf_files)} PDF files")
        logger.info(f"📂 Output: {output_dir}")
        
        # Optimized worker count for hackathon constraints (8 CPUs available)
        max_workers = min(6, multiprocessing.cpu_count(), len(pdf_files), getattr(self.config, 'max_workers', 6))
        
        # Process in batches
        batch_size = max_workers * getattr(self.config, 'batch_size_multiplier', 2)
        
        results = []
        total_processed = 0
        total_successful = 0
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for i in range(0, len(pdf_files), batch_size):
                batch = pdf_files[i:i + batch_size]
                futures = [
                    executor.submit(self.process_pdf_with_retry, pdf, input_dir, output_dir)
                    for pdf in batch
                ]
                for future in as_completed(futures):
                    try:
                        pdf_file, duration, success = future.result()
                        results.append((pdf_file, duration, success))
                        total_processed += 1
                        if success:
                            total_successful += 1
                    except Exception as e:
                        logger.error(f"   ❌ Unexpected error: {str(e)}")
        
        # Summary
        total_duration = sum(duration for _, duration, _ in results)
        logger.info(f"📊 Processing Summary:")
        logger.info(f"   ✅ Successful: {total_successful}/{total_processed}")
        logger.info(f"   ⏱️  Total time: {total_duration:.3f}s")
        logger.info(f"   📈 Average per file: {total_duration/total_processed:.3f}s")
        logger.info(f"   🔧 Workers used: {max_workers}")
        
        return results


def main():
    """Main entry point for Challenge 1a"""
    parser = argparse.ArgumentParser(description="Adobe Hackathon 2025 - Challenge 1a: PDF Outline Extraction")
    parser.add_argument("--input", "-i", type=str, help="Input directory containing PDF files")
    parser.add_argument("--output", "-o", type=str, help="Output directory for JSON results")
    parser.add_argument("--config", "-c", type=str, help="Configuration file path")
    
    args = parser.parse_args()
    
    # Display banner
    display_banner()
    
    # Determine base directory
    base_dir = Path(__file__).parent
    
    # Setup directories
    if args.input and args.output:
        input_dir = args.input
        output_dir = args.output
    else:
        # Default paths
        input_dir = str(base_dir / "input")
        output_dir = str(base_dir / "output")
        
        # Create directories if they don't exist
        Path(input_dir).mkdir(exist_ok=True)
        Path(output_dir).mkdir(exist_ok=True)
    
    # Check if PDFs exist in input directory
    pdf_files = list(Path(input_dir).glob("*.pdf"))
    if not pdf_files:
        logger.warning(f"⚠️  No PDF files found in {input_dir}")
        logger.info(f"📁 Please add PDF files to the input directory and try again.")
        return
    
    logger.info(f"📁 Found {len(pdf_files)} PDF files in input directory")
    
    # Load configuration
    try:
        if args.config and Path(args.config).exists():
            config = ExtractorConfig.from_file(args.config)
        elif (base_dir / "config.json").exists():
            config = ExtractorConfig.from_file(str(base_dir / "config.json"))
        else:
            logger.info("Using default configuration")
            config = ExtractorConfig()
    except Exception as e:
        logger.warning(f"Failed to load config: {e}. Using defaults.")
        config = ExtractorConfig()
    
    # Process PDFs
    overall_start = time.time()
    processor = RobustPDFProcessor(config)
    results = processor.process_all_pdfs(input_dir, output_dir)
    overall_time = time.time() - overall_start
    
    # Final summary
    print("\n" + "="*70)
    if results and any(success for _, _, success in results):
        print("🎉 PDF outline extraction completed successfully!")
        successful_count = sum(1 for _, _, success in results if success)
        print(f"📄 Successfully processed {successful_count}/{len(results)} files")
    else:
        print("❌ Processing failed. Check logs for details.")
    
    print(f"⏱️  Total execution time: {overall_time:.2f} seconds")
    print(f"📂 Results saved to: {Path(output_dir).resolve()}")
    print("="*70)

if __name__ == "__main__":
    main()
