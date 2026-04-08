import os
import pathspec

try:
    import tiktoken
    HAS_TIKTOKEN = True
except ImportError:
    HAS_TIKTOKEN = False

DEFAULT_IGNORES = [
    ".git", ".svn", ".hg",        
    "node_modules", "bower_components", 
    ".venv", "venv", "env",       
    "__pycache__", "*.pyc", "*.pyo",    
    "dist", "build", ".tox", ".nox",    
    ".idea", ".vscode", "*.swp",        
    "package-lock.json", "yarn.lock",   
    "pnpm-lock.yaml",
]

def get_token_count(text):
    if not HAS_TIKTOKEN:
        return len(text) // 4  # Very rough fallback heuristic
    enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(text, disallowed_special=()))

def is_binary(file_path):
    try:
        with open(file_path, "rb") as f:
            chunk = f.read(1024)
            if b"\0" in chunk:
                return True
            return False
    except Exception:
        return True

def get_ignore_spec(directory):
    ignore_patterns = list(DEFAULT_IGNORES)
    gitignore_path = os.path.join(directory, ".gitignore")
    if os.path.exists(gitignore_path):
        try:
            with open(gitignore_path, "r", encoding="utf-8") as f:
                ignore_patterns.extend(f.read().splitlines())
        except Exception as e:
            pass
    return pathspec.PathSpec.from_lines(pathspec.patterns.GitWildMatchPattern, ignore_patterns)

def rank_files(file_list):
    """
    Ranks files based on AI relevance. Returns sorted list.
    Priority: README -> entry points -> core source -> config -> tests -> others
    """
    def score(file_tuple):
        path = file_tuple[0].lower()
        if "readme" in path: return -100
        if "main." in path or "index." in path or "app." in path: return -90
        # Source code files are highly relevant
        if path.endswith(('.py', '.js', '.ts', '.java', '.cpp', '.go', '.rs')): return -50
        # Tests are slightly less important context initially
        if "test" in path or "spec" in path: return -10
        # Configs are lowest priority core files
        if path.endswith(('.json', '.yml', '.yaml', '.toml', '.ini', '.cfg')): return 10
        return 0
    
    return sorted(file_list, key=score)

def summarize_file(content):
    """Placeholder for Week 3 LLM-based summarization."""
    # In a full implementation, this would call an LLM API to get a summary
    # if the file is massive and low priority.
    return "[[FILE CONTENT OMITTED - auto-summarized to save context size.]]\n"

def process_repository(directory, max_tokens_per_chunk=100000, mode="explain"):
    """
    Builds context chunks (Part 1, Part 2, etc.) depending on token size.
    """
    spec = get_ignore_spec(directory)
    base_dir = os.path.abspath(directory)
    
    tree_lines = []
    found_files = [] # list of (rel_file, auth_path)
    
    # 1. Directory Traversal and Tree Generation
    for root, dirs, files in os.walk(base_dir):
        rel_root = os.path.relpath(root, base_dir)
        if rel_root == ".": rel_root = ""
            
        dirs[:] = [d for d in dirs if not spec.match_file(os.path.join(rel_root, d) + "/")]
        
        indent = "  " * (rel_root.count(os.sep) + 1 if rel_root else 0)
        if rel_root:
            tree_lines.append(f"{indent}- {os.path.basename(root)}/")
        else:
            tree_lines.append(f"- {os.path.basename(root)}/ (root)")
        
        for file in sorted(files):
            rel_file = os.path.join(rel_root, file)
            if spec.match_file(rel_file): continue
                
            file_path = os.path.join(root, file)
            if os.path.islink(file_path): continue
            if is_binary(file_path): continue
                
            tree_lines.append(f"{indent}  - {file}")
            found_files.append((rel_file, file_path))
            
    # Combine tree string
    tree_context = "# Directory Structure\n\n" + "\n".join(tree_lines) + "\n\n"
    tree_tokens = get_token_count(tree_context)
    
    # 2. Ranking and Content Extraction
    ranked_files = rank_files(found_files)
    
    chunks = []
    current_chunk = [tree_context]
    current_tokens = tree_tokens
    
    for rel_file, file_path in ranked_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Formatting
            file_payload = f"\n{'='*60}\nFile: {rel_file}\n{'='*60}\n\n{content}\n"
            file_tokens = get_token_count(file_payload)
            
            # Simple Mode Logic: If mode is 'debug', maybe we prioritize error logs (stubbed out)
            # For now, just truncate or summarize if the file itself is bigger than our max chunk
            if file_tokens > max_tokens_per_chunk:
                file_payload = f"\n{'='*60}\nFile: {rel_file}\n{'='*60}\n\n{summarize_file(content)}\n"
                file_tokens = get_token_count(file_payload)
                
            # Chunking Logic
            if current_tokens + file_tokens > max_tokens_per_chunk and current_chunk != [tree_context]:
                # Finalize current chunk before adding this file
                chunks.append("".join(current_chunk))
                current_chunk = [tree_context] # Include tree in every chunk for context
                current_tokens = tree_tokens
                
            current_chunk.append(file_payload)
            current_tokens += file_tokens
            
        except Exception as e:
            continue
            
    if current_chunk != [tree_context] or len(chunks) == 0:
        chunks.append("".join(current_chunk))
        
    # Return array of text blocks
    return chunks
