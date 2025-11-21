# Python Code Formatting Setup

This project uses **Black**, **isort**, and **autoflake** for automatic Python code formatting and import management.

## What's Configured

### 🎨 Black (Code Formatter)

- Formats Python code to a consistent style
- Line length: 88 characters
- Configured in `pyproject.toml`

### 📦 isort (Import Sorter)

- Automatically sorts and organizes imports
- Compatible with Black
- Groups imports: stdlib → django → third-party → first-party → local
- Configured in `pyproject.toml`

### 🧹 autoflake (Unused Import Remover)

- Removes unused imports
- Removes unused variables
- Configured in `pyproject.toml`

## How to Use

### Option 1: Automatic Formatting (Recommended)

**Format on Save** is enabled! Just save any Python file (`Cmd+S` or `Ctrl+S`) and it will:

1. ✅ Remove unused imports (autoflake)
2. ✅ Sort imports (isort)
3. ✅ Format code (black)

### Option 2: Manual Formatting in IDE

**Format Document:**

- **Mac**: `Shift+Option+F`
- **Windows/Linux**: `Shift+Alt+F`

**Organize Imports:**

- **Mac**: `Shift+Option+O`
- **Windows/Linux**: `Shift+Alt+O`

### Option 3: Command Line

**Format entire project:**

```bash
./format_code.sh
```

**Format specific file or directory:**

```bash
./format_code.sh app/account/views.py
./format_code.sh app/account/
```

**Individual commands:**

```bash
# Remove unused imports
env/bin/autoflake --in-place --remove-all-unused-imports app/

# Sort imports
env/bin/isort app/

# Format code
env/bin/black app/
```

## IDE Extensions Needed

Make sure you have these VS Code/Cursor extensions installed:

1. **Python** (by Microsoft) - `ms-python.python`
2. **Black Formatter** (by Microsoft) - `ms-python.black-formatter`
3. **isort** (by Microsoft) - `ms-python.isort`

To install, press `Cmd+Shift+P` → "Extensions: Install Extensions" → Search for each one.

## Configuration Files

- **`.vscode/settings.json`** - IDE settings for auto-formatting
- **`pyproject.toml`** - Black, isort, and autoflake configuration
- **`format_code.sh`** - Manual formatting script

## Import Order

isort will organize imports in this order:

```python
# 1. Future imports
from __future__ import annotations

# 2. Standard library
import os
import sys

# 3. Django
from django.contrib import admin
from django.db import models

# 4. Third-party packages
import requests
from rest_framework import serializers

# 5. First-party (your apps)
from account.models import Account
from email_client.services import EmailService

# 6. Local/relative imports
from .models import MyModel
from .utils import helper_function
```

## Excluding Files

The following directories are automatically excluded:

- `migrations/`
- `staticfiles/`
- `env/`
- `__pycache__/`
- `.git/`

## Troubleshooting

**Formatting not working on save?**

1. Reload the window: `Cmd+Shift+P` → "Reload Window"
2. Check Python interpreter is selected (bottom status bar)
3. Ensure extensions are installed

**Import sorting not working?**

- Right-click in file → "Organize Imports"
- Or run: `env/bin/isort app/`

**Want to disable auto-format temporarily?**

- Edit `.vscode/settings.json`
- Change `"editor.formatOnSave": true` to `false`

## Example

**Before:**

```python
from django.contrib import admin
from account.models import Account, CustomUser
import os
import sys
from rest_framework import serializers


class MyClass:
  def my_method( self,param1,param2 ):
        return param1+param2
```

**After (automatic):**

```python
import os
import sys

from django.contrib import admin
from rest_framework import serializers

from account.models import Account, CustomUser


class MyClass:
    def my_method(self, param1, param2):
        return param1 + param2
```
