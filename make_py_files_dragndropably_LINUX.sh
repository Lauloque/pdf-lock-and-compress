#!/bin/bash

# Generate .desktop files for all .py files in the current directory

CURRENT_DIR="$(pwd)"

# Check if there are any .py files
shopt -s nullglob
py_files=(*.py)

if [ ${#py_files[@]} -eq 0 ]; then
    echo "❌ No .py files found in the current directory."
    exit 1
fi

echo "Found ${#py_files[@]} Python script(s). Generating .desktop files..."
echo ""

for py_file in "${py_files[@]}"; do
    # Get the base name without extension
    base_name="${py_file%.py}"

    # Create a nice display name (replace underscores/dashes with spaces, capitalize)
    display_name=$(echo "$base_name" | sed 's/[_-]/ /g' | sed 's/\b\(.\)/\u\1/g')

    # Desktop file path
    if [ "$base_name" == "main" ]; then
        desktop_file="pdf_compress.desktop"
    elif [ "$base_name" == "constants" ]; then
        continue
    else
        desktop_file="${base_name}.desktop"
    fi

    # Get absolute path to the Python script
    absolute_path="${CURRENT_DIR}/${py_file}"

    # Generate the .desktop file
    cat > "$desktop_file" << EOF
[Desktop Entry]
Type=Application
Name=${display_name}
Comment=Run ${py_file}
Icon=text-x-python
Exec=konsole --hold -e python3 "${absolute_path}" %F
Terminal=true
Categories=Utility;
EOF

    # Make it executable
    chmod +x "$desktop_file"

    echo "✅ Created: ${desktop_file}"
done

echo ""
echo "🎉 Done! You can now drag files onto the .desktop files to run your Python scripts."
echo ""
echo "💡 Tip: You can edit the .desktop files to customize:"
echo "   - Name: Change the display name"
echo "   - Icon: Use a different icon (e.g., application-pdf, document-compress)"
echo "   - MimeType: Restrict to specific file types (e.g., MimeType=application/pdf)"
