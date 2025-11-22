import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas


def get_code_files(directory, excluded_files=None, excluded_dirs=None):
    """Fetch all TS/TSX/JS/JSX project files excluding sensitive configuration files."""
    if excluded_files is None:
        # Sensitive files to exclude
        excluded_files = {
            "package-lock.json",
            "yarn.lock",
            "pnpm-lock.yaml",
            ".DS_Store",
            "Thumbs.db",
            "Desktop.ini",
            # Sensitive configuration files
            ".env",
            ".env.development",
            ".env.production",
            ".env.local",
            ".env.staging",
            ".env.test",
            "env.ts",
            "env.js",
            "keys.ts",
            "keys.js",
            "secrets.ts",
            "secrets.js",
            "firebase.ts",
            "firebase.js",
            "firebase.config.ts",
            "firebase.config.js",
            "aws.config.ts",
            "aws.config.js",
            "api.config.ts",
            "api.config.js",
            # Script files
            "reset-project.js",
            "generate-icons.js",
        }

    if excluded_dirs is None:
        excluded_dirs = {
            "node_modules",
            ".git",
            "__pycache__",
            "build",
            "dist",
            ".next",
            "coverage",
            ".nyc_output",
            "logs",
            "uploads",
            "secrets",
            ".expo",
            ".vscode",
            "android",
            "ios",
            "__tests__",
            "_tests_",
            "assets",
            "scripts",
        }

    code_files = {}

    # Define file extensions to include
    code_extensions = {".ts", ".tsx", ".js", ".jsx", ".d.ts"}

    # Define safe configuration files to include (non-sensitive)
    safe_config_files = {
        "package.json",
        "tsconfig.json",
        "app.json",
        "babel.config.js",
        "eslint.config.js",
        ".eslintrc.js",
        ".prettierrc",
        "prettier.config.js",
        "jest.config.js",
        "tailwind.config.js",
        "tailwind.config.ts",
        "expo-env.d.ts",
        "global.d.ts",
    }

    for root, dirs, files in os.walk(directory):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in excluded_dirs]

        # Skip if current directory is an excluded directory
        if any(excluded_dir in root.split(os.sep) for excluded_dir in excluded_dirs):
            continue

        for file in files:
            # Skip excluded files
            if file in excluded_files:
                continue

            # Additional check for any file containing sensitive patterns
            if any(
                pattern in file.lower()
                for pattern in [
                    "secret",
                    "password",
                    "token",
                    "credential",
                ]
            ):
                # Allow .env.example
                if not file.endswith(".example"):
                    continue

            file_path = os.path.join(root, file)

            # Get file extension
            _, ext = os.path.splitext(file)

            # Only include code files OR safe configuration files
            if ext.lower() in code_extensions or file in safe_config_files:
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        code_files[file_path] = f.readlines()

                except Exception as e:
                    print(f"❌ Error reading {file_path}: {e}")
                    code_files[file_path] = [f"[Error reading file: {str(e)}]"]

    return code_files


def create_pdf(code_data, output_pdf="ReactNative_Code_Export.pdf"):
    c = canvas.Canvas(output_pdf, pagesize=A4)
    width, height = A4
    margin = 20 * mm
    line_height = 10
    y = height - margin

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(margin, y, "📱 React Native/Expo Project Code Export")
    y -= 2 * line_height
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "📁 TypeScript/JavaScript Files & Configuration:")
    y -= 2 * line_height

    file_paths = sorted(list(code_data.keys()))

    # 1. File list with file type indicators
    c.setFont("Courier", 8)
    for path in file_paths:
        if y < margin:
            c.showPage()
            c.setFont("Courier", 8)
            y = height - margin

        display_path = os.path.relpath(path)

        # Add file type indicator
        if display_path.endswith(".tsx"):
            file_type = "[TSX]"
        elif display_path.endswith(".ts") and not display_path.endswith(".d.ts"):
            file_type = "[TS]"
        elif display_path.endswith(".d.ts"):
            file_type = "[DTS]"
        elif display_path.endswith(".jsx"):
            file_type = "[JSX]"
        elif display_path.endswith(".js"):
            file_type = "[JS]"
        elif display_path.endswith("package.json"):
            file_type = "[PKG]"
        elif display_path.endswith("tsconfig.json"):
            file_type = "[TSC]"
        elif display_path.endswith("app.json"):
            file_type = "[APP]"
        elif ".config." in display_path:
            file_type = "[CFG]"
        else:
            file_type = "[FILE]"

        c.drawString(margin, y, f"- {file_type} {display_path}")
        y -= line_height

    # Add page break before code content
    c.showPage()
    y = height - margin

    # 2. File contents
    for file_path in file_paths:
        lines = code_data[file_path]
        print(f"📄 Adding: {file_path}")

        if y < margin + 3 * line_height:
            c.showPage()
            y = height - margin

        # File header
        rel_path = os.path.relpath(file_path)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(margin, y, f"📄 File: {rel_path}")
        y -= line_height

        # Add separator line
        c.setFont("Courier", 8)
        c.drawString(margin, y, "=" * 80)
        y -= line_height

        # File content with line numbers
        for line_num, line in enumerate(lines, 1):
            if y < margin:
                c.showPage()
                c.setFont("Courier", 8)
                y = height - margin

            # Clean and truncate line
            line = line.strip("\n").encode("latin-1", "replace").decode("latin-1")

            # Add line numbers for all files
            display_line = f"{line_num:3d}: {line[:280]}"

            c.drawString(margin, y, display_line)
            y -= line_height

        # Add spacing between files
        y -= line_height
        if y > margin:
            c.setFont("Courier", 8)
            c.drawString(margin, y, "-" * 80)
            y -= 2 * line_height

    c.save()
    print(f"✅ PDF successfully created: {output_pdf}")
    print(f"📊 Total files processed: {len(code_data)}")
    print(f"📁 File breakdown:")

    # Print file type breakdown
    tsx_count = sum(1 for f in code_data.keys() if f.endswith(".tsx"))
    ts_count = sum(
        1 for f in code_data.keys() if f.endswith(".ts") and not f.endswith(".d.ts")
    )
    dts_count = sum(1 for f in code_data.keys() if f.endswith(".d.ts"))
    jsx_count = sum(1 for f in code_data.keys() if f.endswith(".jsx"))
    js_count = sum(
        1
        for f in code_data.keys()
        if f.endswith(".js") and not any(x in f for x in [".config.", "babel"])
    )
    config_count = len(code_data) - tsx_count - ts_count - dts_count - jsx_count - js_count

    print(f"   - TSX files: {tsx_count}")
    print(f"   - TypeScript files: {ts_count}")
    print(f"   - Type definition files: {dts_count}")
    print(f"   - JSX files: {jsx_count}")
    print(f"   - JavaScript files: {js_count}")
    print(f"   - Configuration files: {config_count}")


def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))

    # Expanded exclusions to include sensitive files
    excluded_files = {
        "package-lock.json",
        "yarn.lock",
        "pnpm-lock.yaml",
        ".DS_Store",
        "Thumbs.db",
        "Desktop.ini",
        # Sensitive files
        ".env",
        ".env.development",
        ".env.production",
        ".env.local",
        ".env.staging",
        ".env.test",
        "env.ts",
        "env.js",
        "keys.ts",
        "keys.js",
        "secrets.ts",
        "secrets.js",
        "firebase.ts",
        "firebase.js",
        "firebase.config.ts",
        "firebase.config.js",
        "aws.config.ts",
        "aws.config.js",
        "api.config.ts",
        "api.config.js",
        # Script files
        "reset-project.js",
        "generate-icons.js",
    }

    # Directories to exclude
    excluded_dirs = {
        "node_modules",
        ".git",
        "__pycache__",
        "build",
        "dist",
        ".next",
        "coverage",
        ".nyc_output",
        "logs",
        "uploads",
        "secrets",
        ".expo",
        ".vscode",
        "android",
        "ios",
        "__tests__",
        "_tests_",
        "assets",
        "scripts",
    }

    print("🔍 Scanning React Native/Expo project for code files...")
    print("🔒 Sensitive files (.env, keys, secrets, etc.) will be excluded")
    print("📱 Including: app/, src/, components/, hooks/, etc.")

    code_files = get_code_files(root_dir, excluded_files, excluded_dirs)

    if not code_files:
        print("❌ No code files found to process!")
        return

    print(f"📁 Found {len(code_files)} files to include in PDF")

    # Show user what files will be included (first 20 files)
    print("\n📋 Files to be included (showing first 20):")
    for idx, file_path in enumerate(sorted(code_files.keys())[:20]):
        rel_path = os.path.relpath(file_path)
        print(f"   📄 {rel_path}")
    
    if len(code_files) > 20:
        print(f"   ... and {len(code_files) - 20} more files")

    create_pdf(code_files)


if __name__ == "__main__":
    main()