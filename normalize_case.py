import os
import re

BASE_DIR = '.'  # your project root
SRC_DIR = os.path.join(BASE_DIR, 'src')  # alias @ => ./src
FILE_EXTENSIONS = ('.js', '.ts', '.vue')
IMPORT_REGEX = re.compile(r'(import\s+(?:.*?\s+from\s+)?[\'"])([^\'"]+)([\'"])')

def find_real_case_path(path):
    """Return the correctly cased version of a path, if it exists"""
    if not os.path.exists(path):
        parts = path.split(os.sep)
        corrected_parts = []
        current = ''
        for part in parts:
            try:
                entries = os.listdir(current or '.')
                match = next((e for e in entries if e.lower() == part.lower()), part)
                corrected_parts.append(match)
                current = os.path.join(current, match)
            except FileNotFoundError:
                return path  # Fallback
        return os.path.join(*corrected_parts)
    return path

def resolve_import_path(import_path):
    if import_path.startswith('@/'):
        return os.path.join(SRC_DIR, import_path[2:])
    elif import_path.startswith('./') or import_path.startswith('../'):
        return os.path.join(BASE_DIR, import_path)
    return None

def to_import_path(full_path):
    """Convert full path back to import path (with @/ if inside src)"""
    if full_path.startswith(SRC_DIR):
        rel = os.path.relpath(full_path, SRC_DIR)
        return '@/{}'.format(rel.replace(os.sep, '/'))
    elif full_path.startswith(BASE_DIR):
        rel = os.path.relpath(full_path, BASE_DIR)
        return './{}'.format(rel.replace(os.sep, '/'))
    return full_path

def normalize_imports_and_files(base_dir=BASE_DIR):
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if not file.endswith(FILE_EXTENSIONS):
                continue

            full_path = os.path.join(root, file)
            updated_lines = []

            with open(full_path, 'r') as f:
                lines = f.readlines()

            changed = False

            for line in lines:
                match = IMPORT_REGEX.search(line)
                if match:
                    prefix, import_path, suffix = match.groups()

                    resolved = resolve_import_path(import_path)
                    if resolved and os.path.splitext(resolved)[1] == '':
                        # Try adding extensions
                        for ext in ['.vue', '.js', '.ts']:
                            if os.path.exists(resolved + ext):
                                resolved += ext
                                break

                    real_path = find_real_case_path(resolved) if resolved else None

                    if real_path and os.path.exists(real_path):
                        corrected_import = to_import_path(real_path)
                        if corrected_import != import_path:
                            line = line.replace(import_path, corrected_import)
                            changed = True

                updated_lines.append(line)

            if changed:
                print(f"🔧 Fixed imports in: {full_path}")
                with open(full_path, 'w') as f:
                    f.writelines(updated_lines)

        # Rename files on disk to match actual casing
        for file in files:
            correct_case = find_real_case_path(os.path.join(root, file))
            if os.path.exists(correct_case):
                target = os.path.join(root, os.path.basename(correct_case))
                if file != os.path.basename(target):
                    os.rename(os.path.join(root, file), target)
                    print(f"📁 Renamed file: {file} → {os.path.basename(target)}")

        # Rename directories
        for i, dir_name in enumerate(dirs):
            real_name = find_real_case_path(os.path.join(root, dir_name))
            if os.path.exists(real_name):
                corrected = os.path.basename(real_name)
                if corrected != dir_name:
                    os.rename(os.path.join(root, dir_name), os.path.join(root, corrected))
                    dirs[i] = corrected
                    print(f"📂 Renamed dir: {dir_name} → {corrected}")

if __name__ == "__main__":
    normalize_imports_and_files()