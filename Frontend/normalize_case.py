import os
import re
from pathlib import Path

BASE_DIR = Path('')
FILE_EXTENSIONS = ('.js', '.ts', '.vue')
IMPORT_REGEX = re.compile(r'(import\s+.*?from\s+[\'"])([^\'"]+)([\'"])')

def find_all_files():
    """Build a case-insensitive lookup of all files"""
    file_map = {}
    
    for file_path in BASE_DIR.rglob('*'):
        if file_path.is_file() and file_path.suffix in FILE_EXTENSIONS:
            # Skip node_modules, .git, etc.
            if any(part.startswith('.') or part == 'node_modules' for part in file_path.parts):
                continue
            
            # Create lookup key (lowercase path)
            key = str(file_path).lower()
            file_map[key] = file_path
    
    return file_map

def resolve_import_path(import_path, current_file_dir, file_map):
    """Find the actual file that matches the import path"""
    if not (import_path.startswith('@/') or import_path.startswith('./') or import_path.startswith('../')):
        return None  # Skip external imports
    
    # Convert import to absolute path
    if import_path.startswith('@/'):
        # Assuming @/ maps to src/
        target_path = BASE_DIR / 'src' / import_path[2:]
    else:
        target_path = (current_file_dir / import_path).resolve()
    
    # Try exact match first
    target_str = str(target_path).lower()
    if target_str in file_map:
        return file_map[target_str]
    
    # If no extension, try adding extensions
    if target_path.suffix == '':
        for ext in FILE_EXTENSIONS:
            test_path = str(target_path.with_suffix(ext)).lower()
            if test_path in file_map:
                return file_map[test_path]
        
        # Try index files
        for ext in FILE_EXTENSIONS:
            index_path = str(target_path / f'index{ext}').lower()
            if index_path in file_map:
                return file_map[index_path]
    
    return None

def path_to_import(file_path, current_file_dir):
    """Convert file path back to import string"""
    file_path = Path(file_path).resolve()
    current_file_dir = Path(current_file_dir).resolve()
    
    # Try @/ alias (if file is in src/)
    src_dir = (BASE_DIR / 'src').resolve()
    try:
        rel_to_src = file_path.relative_to(src_dir)
        import_path = f"@/{rel_to_src.as_posix()}"
        
        # Keep .vue extensions, remove .js/.ts extensions
        if file_path.suffix == '.vue':
            return import_path
        elif file_path.suffix in ('.js', '.ts'):
            return import_path.replace(file_path.suffix, '')
        return import_path
    except ValueError:
        pass
    
    # Use relative path
    try:
        rel_path = file_path.relative_to(current_file_dir)
        rel_str = rel_path.as_posix()
        
        if not rel_str.startswith('../'):
            rel_str = f'./{rel_str}'
        
        # Keep .vue extensions, remove .js/.ts extensions
        if file_path.suffix == '.vue':
            return rel_str
        elif file_path.suffix in ('.js', '.ts'):
            return rel_str.replace(file_path.suffix, '')
        return rel_str
    except ValueError:
        return str(file_path)

def fix_imports_in_file(file_path, file_map):
    """Fix imports in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except (UnicodeDecodeError, PermissionError):
        return False
    
    lines = content.splitlines()
    changed = False
    current_dir = file_path.parent
    
    for i, line in enumerate(lines):
        match = IMPORT_REGEX.search(line)
        if match:
            prefix, import_path, suffix = match.groups()
            
            # Find the actual file
            actual_file = resolve_import_path(import_path, current_dir, file_map)
            if actual_file:
                correct_import = path_to_import(actual_file, current_dir)
                if correct_import != import_path:
                    # Replace the import path in the line
                    new_line = line.replace(f'"{import_path}"', f'"{correct_import}"')
                    new_line = new_line.replace(f"'{import_path}'", f"'{correct_import}'")
                    lines[i] = new_line
                    changed = True
                    print(f"  📝 {import_path} → {correct_import}")
            else:
                print(f"  ❌ Could not find file for: {import_path}")
    
    if changed:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines) + '\n')
        return True
    return False

def main():
    print("🔍 Building file index...")
    file_map = find_all_files()
    
    print(f"📁 Found {len(file_map)} files")
    
    # Show some example files for debugging
    print("\n📋 Sample files found:")
    for i, (key, path) in enumerate(file_map.items()):
        if i < 10:  # Show first 10
            print(f"  {path}")
    
    print(f"\n🔧 Fixing imports...")
    total_files_changed = 0
    
    # Process all source files
    for file_path in file_map.values():
        print(f"\nChecking: {file_path.relative_to(BASE_DIR)}")
        if fix_imports_in_file(file_path, file_map):
            total_files_changed += 1
    
    print(f"\n✅ Done! Fixed imports in {total_files_changed} files.")

if __name__ == "__main__":
    main()
