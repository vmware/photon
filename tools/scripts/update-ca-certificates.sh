#!/bin/bash

UPSTREAM_URL="https://anduin.linuxfromscratch.org/BLFS/other/certdata.txt"
PHOTON_REPO="https://github.com/vmware/photon.git"

REQUIRED_TOOLS="git wget awk sha256sum sed grep mktemp head"
for tool in $REQUIRED_TOOLS; do
    if ! command -v "$tool" >/dev/null 2>&1; then
        echo "Error: Required command '$tool' is not installed or not in PATH."
        exit 1
    fi
done

WORK_DIR="$1"
if [ -z "$WORK_DIR" ]; then
    read -p "Enter path to photon repo (leave empty to clone): " WORK_DIR
fi

if [ -z "$WORK_DIR" ]; then
    echo "Cloning photon..."
    git clone --depth 1 "$PHOTON_REPO" photon-verify
    WORK_DIR="photon-verify"
elif [ ! -d "$WORK_DIR" ]; then
    echo "Directory $WORK_DIR not found."
    exit 1
fi

cd "$WORK_DIR" || exit 1

SPEC="SPECS/ca-certificates/ca-certificates.spec"
LOCAL_FILE="SPECS/ca-certificates/certdata.txt"

if [ ! -f "$SPEC" ]; then
    echo "Error: $SPEC not found in $WORK_DIR"
    exit 1
fi

echo "Downloading upstream..."
TEMP=$(mktemp)
wget -q -O "$TEMP" "$UPSTREAM_URL"

if [ ! -s "$TEMP" ]; then
    echo "Download failed."
    rm -f "$TEMP"
    exit 1
fi

NEW_VER=$(grep "Revision:" "$TEMP" | head -n 1 | sed -E 's/.*Revision: ([0-9]+).*/\1/')

if [ -z "$NEW_VER" ]; then
    echo "Error: Could not extract Revision number from downloaded file."
    echo "File content check (first 5 lines):"
    head -n 5 "$TEMP"
    rm -f "$TEMP"
    exit 1
fi

echo "Upstream Revision: $NEW_VER"

UPDATED=false
if [ -f "$LOCAL_FILE" ]; then
    SUM_LOCAL=$(sha256sum "$LOCAL_FILE" | awk '{print $1}')
    SUM_NEW=$(sha256sum "$TEMP" | awk '{print $1}')

    if [ "$SUM_LOCAL" != "$SUM_NEW" ]; then
        echo "Hash change detected ($SUM_LOCAL -> $SUM_NEW). Updating..."
        UPDATED=true
    else
        CURRENT_SPEC_VER=$(grep "^Version:" "$SPEC" | awk '{print $2}')
        if [ "$CURRENT_SPEC_VER" != "$NEW_VER" ]; then
            echo "Hash match, but Spec version is outdated. Updating Spec only."
            UPDATED=true
            rm -f "$TEMP"
        else
            echo "No changes needed. Version $NEW_VER is current."
            rm -f "$TEMP"
            exit 0
        fi
    fi
else
    UPDATED=true
fi

if [ "$UPDATED" = true ]; then
    DATE_STR=$(date +"%a %b %d %Y")

    USER=$(git config user.name)
    EMAIL=$(git config user.email)

    if [ -z "$USER" ] || [ -z "$EMAIL" ]; then
        echo "Error: Git 'user.name' or 'user.email' is not configured."
        rm -f "$TEMP"
        exit 1
    fi

    if [ -f "$TEMP" ]; then
        mv "$TEMP" "$LOCAL_FILE"
    fi

    # Update Version and reset Release to 1
    sed -i "s/^Version:.*/Version:        $NEW_VER/" "$SPEC"
    sed -i 's/^Release:.*/Release:        1%{?dist}/' "$SPEC"

    ENTRY="* $DATE_STR $USER <$EMAIL> $NEW_VER-1"
    MSG="- Update certdata to revision $NEW_VER"

    # Insert safely after %changelog
    sed -i "/%changelog/a $ENTRY\n$MSG" "$SPEC"

    echo "Spec updated to version $NEW_VER"

    # 7. Commit
    echo "Creating git commit..."
    git add "$SPEC" "$LOCAL_FILE"
    git commit -m "ca-certificates: Update to revision $NEW_VER"

    echo "Success! Commit created."
fi
