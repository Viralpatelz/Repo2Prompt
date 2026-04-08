import argparse
import sys
import os
import shutil

from repo2prompt.core import process_repository
from repo2prompt.git_utils import is_github_url, clone_repo_to_temp

def main():
    parser = argparse.ArgumentParser(description="Repo2Prompt++: Convert repositories to LLM-ready context bundles.")
    parser.add_argument("source", help="The local directory path or GitHub URL to process.")
    parser.add_argument("-o", "--output", default="context", help="Output file base name (default: context)")
    parser.add_argument("--max-tokens", type=int, default=100000, help="Maximum tokens per output file (default: 100k)")
    parser.add_argument("--mode", choices=["explain", "debug", "improve"], default="explain", help="Prompt generation mode")
    
    args = parser.parse_args()
    source = args.source
    
    print(f"Starting Repo2Prompt++ on: {source}")
    print(f"Mode: {args.mode.upper()} | Chunking limit: ~{args.max_tokens} tokens")
    
    temp_dir = None
    target_dir = source
    
    if is_github_url(source):
        try:
            temp_dir = clone_repo_to_temp(source)
            target_dir = temp_dir
        except Exception as e:
            print(f"Error cloning repository: {e}")
            sys.exit(1)
    else:
        if not os.path.isdir(target_dir):
            print(f"Error: Directory '{target_dir}' does not exist.")
            sys.exit(1)
            
    print("Extracting, Ranking, and Chunking codebase...")
    try:
        chunks = process_repository(target_dir, max_tokens_per_chunk=args.max_tokens, mode=args.mode)
        
        for i, chunk_text in enumerate(chunks):
            # If only 1 chunk, don't append _partX
            if len(chunks) == 1:
                out_path = f"{args.output}.txt"
            else:
                out_path = f"{args.output}_part{i+1}.txt"
                
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(chunk_text)
                
            print(f"Successfully generated: {out_path} ({len(chunk_text)/1024:.2f} KB)")
            
        print(f"All done! Total bundles generated: {len(chunks)}")
    finally:
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            print("Cleaned up temporary cloned repository.")

if __name__ == "__main__":
    main()
