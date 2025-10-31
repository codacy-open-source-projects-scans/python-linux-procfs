# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

python-linux-procfs is a Python library that provides abstractions to extract information from the Linux kernel /proc filesystem. It's a GPL-2.0-only licensed library maintained by Red Hat developers, primarily for Linux system programming and process introspection.

## Build and Test Commands

### Installation
```bash
# Install the package locally for development
python3 -m pip install -e .

# Or using setup.py directly
python3 setup.py install
```

### Testing
```bash
# Run the bitmasklist unit tests
python3 bitmasklist_test.py
```

### Clean
```bash
# Remove temporary files and tags
make clean

# Remove only Python cache files
make pyclean
```

### Tags Generation
```bash
# Generate ctags for code navigation
make tags
```

## Architecture

### Core Module Structure

The library consists of a single `procfs` package with two main modules:

**procfs/procfs.py** - Main module containing all /proc abstraction classes:
- `pidstat` - Parses /proc/PID/stat files for process statistics
- `pidstatus` - Parses /proc/PID/status files for additional process info
- `process` - Combines stat and status data, lazy-loads cmdline, threads, cgroups, environ
- `pidstats` - Collection of all processes in the system with find/search methods
- `interrupts` - Parses /proc/interrupts for IRQ information
- `cmdline` - Parses /proc/cmdline for kernel boot parameters
- `cpuinfo` - Parses /proc/cpuinfo for CPU information and topology
- `cpustat`/`cpusstats` - Parses /proc/stat for CPU usage statistics
- `smaps`/`smaps_lib` - Parses /proc/PID/smaps for memory mapping information

**procfs/utilist.py** - Utility functions for bitmask conversions:
- `bitmasklist()` - Converts hex CPU affinity masks to lists of CPU numbers
- `hexbitmask()` - Converts CPU number lists to hex bitmask format

### Design Patterns

1. **Lazy Loading**: The `process` class implements lazy loading via `__getitem__` - attributes like "stat", "status", "cmdline", "threads", "cgroups", and "environ" are only loaded when accessed.

2. **Dictionary-like Interfaces**: Most classes implement dict-like access patterns (`__getitem__`, `keys()`, `values()`, `items()`, `__contains__`) for intuitive data access.

3. **Ephemeral Process Handling**: Code throughout handles processes disappearing mid-query by catching `FileNotFoundError` and `IOError` exceptions.

4. **basedir Parameter**: Most classes accept a `basedir` parameter (default "/proc") to support testing with mock /proc filesystems or accessing /proc from containers.

### Key Implementation Details

- **Process flags**: `pidstat` class defines PF_* constants matching kernel's include/linux/sched.h. Some flags have duplicate values representing kernel API changes (e.g., PF_THREAD_BOUND and PF_NO_SETAFFINITY both = 0x04000000).

- **Thread handling**: Threads are loaded from /proc/PID/task/ with the thread leader (matching the PID) removed from the collection.

- **CPU topology**: `cpuinfo` class calculates `nr_sockets` and `nr_cores` based on "physical id", "siblings", and "cpu cores" fields. Has special handling for s390/s390x architectures.

- **Interrupt affinity**: The `interrupts` class reads both /proc/interrupts and /proc/irq/*/smp_affinity to provide complete IRQ information.

## Command Line Tools

**pflags** - Utility to display process flags for running processes:
- Can filter by PID, process name, or glob patterns
- Shows kernel process flags (PF_*) in human-readable format
- Handles superseded flags (removes old flag names when new ones exist)
- Note: Currently imports from `six.moves` which should be removed as Python 2 support is no longer needed (requires-python = ">=3.10")

## Python Version Requirements

- Minimum Python version: 3.10
- The codebase has been migrated away from Python 2/3 compatibility
- Still has one remaining `six` import in `pflags` that should be removed

## Package Configuration

The project uses modern Python packaging with both:
- `pyproject.toml` - Modern build configuration (preferred)
- `setup.py` - Legacy setup script for backwards compatibility

Both files must be kept in sync for version numbers and metadata.
