#!/usr/bin/env python3

import argparse
import os
import sys
from pathlib import Path
from collections import defaultdict
from typing import List, Tuple, Optional, Set, Dict

class ConfigReader:
    def __init__(self, priority_file: str, debug: int = 0) -> None:
        self.priority_file = priority_file
        self.order: List[str] = []
        self.variants: Dict[str, List[str]] = {}
        self.config_values: Dict[str, Dict[str, str]] = defaultdict(dict)  # {config_name: {path: value}}
        self.debug: int = debug

    def msg(self, output: str, level: int = 1) -> None:
        if self.debug >= level:
            print(output)

    def read_priority_file(self) -> None:
        """Read and parse the priority file."""
        with open(self.priority_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if line.startswith('ORDER='):
                    self.order = line.split('=', 1)[1].split()
                elif '=' in line and not (line.startswith('EMPTY') or line.startswith('ORDER')):
                    variant, fragments = line.split('=', 1)
                    self.variants[variant.strip()] = fragments.split(':')

    def read_config_file(self, config_path: Path) -> str:
        """Read a single config file and return its value."""
        if not config_path.exists():
            return '-'
        with open(config_path, 'r') as f:
            for line in f:
                line = line.strip()
                # Detect 'not set' or 'not enabled' before skipping comment lines
                if line.startswith('# CONFIG_') and (' is not set' in line or ' is not enabled' in line):
                    return 'n'
                # Skip empty lines and other comments
                if not line or line.startswith('#'):
                    continue
                if line.startswith('CONFIG_') and line.endswith('=y'):
                    return 'y'
                elif line.startswith('CONFIG_') and line.endswith('=m'):
                    return 'm'
                return line
        return '-'

    def get_config_value_for_variant(self, config_name: str, variant: str, debug: bool = False, exclude_path: Optional[Path] = None, exclude_path2: Optional[Path] = None, priority_prefix: Optional[str] = None) -> Tuple[Optional[str], Optional[str], List[str]]:
        """Get the final value of a config for a specific variant following priority order."""
        if variant not in self.variants:
            self.msg(f"[DEBUG] Variant '{variant}' not found in priority file.")
            return None, None, []

        final_value = None
        final_path = None
        checked_paths = []  # Track all paths checked

        self.msg(f"ORDER: {self.order}")
        self.msg(f"Fragments for variant '{variant}': {self.variants[variant]}")

        # Follow the ORDER of directories
        for directory in self.order:
            # Skip if we're looking for a specific priority and this isn't it
            if priority_prefix and not directory.startswith(priority_prefix):
                continue

            # For each fragment in the variant
            for frag in self.variants[variant]:
                # Handle both generic and debug paths
                frag_parts = frag.split('-')
                base_path = Path(*frag_parts)

                # Check generic path
                config_path = Path(directory) / base_path / config_name
                if config_path == exclude_path or config_path == exclude_path2:
                    continue
                value = self.read_config_file(config_path)
                checked_paths.append(str(config_path))
                if value != '-':
                    final_value = value
                    final_path = str(config_path)

                # Check debug path if it exists
                debug_path = Path(directory) / base_path / 'debug' / config_name
                if debug_path == exclude_path or debug_path == exclude_path2:
                    continue
                value = self.read_config_file(debug_path)
                checked_paths.append(str(debug_path))
                if value != '-':
                    final_value = value
                    final_path = str(debug_path)

        return final_path, final_value, checked_paths

    def check_variant_impact(self, config_name: str, rhel_path: Path, fedora_path: Path, value: str, variant: str, priority_file: str) -> Tuple[Optional[str], Optional[str]]:
        """Check if moving a config to common would affect a variant."""
        reader = ConfigReader(priority_file, self.debug)
        reader.read_priority_file()
        # Get current final value
        final_path, final_value, _ = reader.get_config_value_for_variant(config_name, variant)
        # Check if this path affects this variant
        variant_fragments = reader.variants[variant]
        path_affects_variant = False
        for frag in variant_fragments:
            frag_parts = frag.split('-')
            if all(part in str(rhel_path) for part in frag_parts):
                path_affects_variant = True
                break
        if not path_affects_variant:
            return None, None

        # Get the value that would be used after moving to common
        new_value = None
        for directory in reader.order:
            if directory.startswith('common/'):
                continue
            for frag in variant_fragments:
                frag_parts = frag.split('-')
                base_path = Path(*frag_parts)
                check_path = Path(directory) / base_path / config_name
                if check_path != rhel_path and check_path != fedora_path and check_path.exists():
                    value = reader.read_config_file(check_path)
                    if value != '-':
                        new_value = value
                        break
            if new_value is not None:
                break
        # If no other configs found, use the common value
        if new_value is None:
            new_value = value
        return final_value, new_value

    def analyze_redundant_config(self, config_name: str, variant: Optional[str] = None, priority_prefix: Optional[str] = None) -> Set[Path]:
        """Analyze which config files are redundant without removing them."""
        variant_list = [variant] if variant else list(self.variants.keys())

        # First, get all paths and their values
        all_paths_and_values = []
        # Search in all directories under the current directory
        for root, _, files in os.walk('.'):
            if config_name in files:
                config_path = Path(root) / config_name
                # Only include files from the current priority
                if priority_prefix and not str(config_path).startswith(priority_prefix):
                    continue
                value = self.read_config_file(config_path)
                all_paths_and_values.append((config_path, value))

        if not all_paths_and_values:
            return set()

        self.msg("\nAll file locations:")
        self.msg("-" * 80)
        for path, value in sorted(all_paths_and_values):
            self.msg(f"{path}: {value}")
        self.msg("-" * 80)

        self.msg("\nFile analysis:")
        self.msg("-" * 80)

        safe_to_remove = set()
        # For each path, check if it's safe to remove across all variants
        for path, value in all_paths_and_values:
            safe_to_remove_path = True
            impact = []
            self.msg(f"\nAnalyzing {path}:")
            self.msg(f"  Current value: {value}")

            # Check each variant
            for variant in variant_list:
                self.msg(f"  Checking variant {variant}:")
                # Get the final value for this variant
                final_path, final_value, _ = self.get_config_value_for_variant(config_name, variant, priority_prefix=priority_prefix)
                self.msg(f"    Current final value: {final_value} (from {final_path})")

                # Check if this path affects this variant by checking if it's in the variant's fragments
                variant_fragments = self.variants[variant]
                path_affects_variant = False
                for frag in variant_fragments:
                    frag_parts = frag.split('-')
                    if all(part in str(path) for part in frag_parts):
                        path_affects_variant = True
                        break

                if not path_affects_variant:
                    self.msg("    Skipping - path doesn't affect this variant")
                    continue

                # Check if removing this path would change the final value
                new_path, new_value, _ = self.get_config_value_for_variant(config_name, variant, exclude_path=path, priority_prefix=priority_prefix)
                self.msg(f"    Value after removal: {new_value} (from {new_path})")

                if new_value != final_value:
                    safe_to_remove_path = False
                    impact.append(f"variant {variant}: would change from {final_value} to {new_value}")
                    self.msg("    KEEP - removal would change value")

            if safe_to_remove_path:
                self.msg(f"REMOVE: {path}")
                self.msg(f"  Reason: Redundant - removing won't change final value for any variant (value: {value})")
                safe_to_remove.add(path)
            else:
                self.msg(f"KEEP: {path}")
                self.msg("  Reason: Removing would affect:")
                for i in impact:
                    self.msg(f"    - {i}")
                self.msg(f"  Current value: {value}")
            self.msg("-" * 80)

        return safe_to_remove

    def process_fix_operation(self, config_name: str, priority_files: List[str], args: argparse.Namespace) -> None:
        """Process the fix operation for a config."""
        # First analyze all files to find which ones are safe to remove
        all_safe_to_remove = set()
        for priority_file in priority_files:
            self.msg(f"\nAnalyzing in {priority_file}")
            reader = ConfigReader(priority_file, args.debug)
            reader.read_priority_file()
            priority_prefix = priority_file.replace('priority.', '')
            safe_paths = reader.analyze_redundant_config(config_name, args.variant, priority_prefix=priority_prefix)
            # Add paths from this priority file to the set of safe paths
            all_safe_to_remove.update(safe_paths)

        # Now remove files that are safe to remove
        if len(all_safe_to_remove) > 0:  # Explicit check for non-empty set
            self.msg(f"\nRemoving redundant files for {config_name}:")
            for path in sorted(all_safe_to_remove):
                self.msg(f"Removed: {path}")
                path.unlink()
        else:
            self.msg("\nNo files to remove - all_safe_to_remove is empty")

    def find_common_configs(self, config_name: str) -> List[Tuple[Path, Path, str]]:
        """Find config files that exist in both rhel and fedora directories."""
        rhel_paths = set()
        fedora_paths = set()

        # Search in all directories under the current directory
        for root, _, files in os.walk('.'):
            if config_name in files:
                config_path = Path(root) / config_name
                if str(config_path).startswith('rhel/'):
                    rhel_paths.add(config_path)
                elif str(config_path).startswith('fedora/'):
                    fedora_paths.add(config_path)

        # Find paths that have matching structure in both rhel and fedora
        common_paths = []
        for rhel_path in rhel_paths:
            # Convert rhel path to fedora path
            fedora_path = Path('fedora') / rhel_path.relative_to('rhel')
            if fedora_path in fedora_paths:
                # Check if values match
                rhel_value = self.read_config_file(rhel_path)
                fedora_value = self.read_config_file(fedora_path)
                if rhel_value == fedora_value:
                    # Check if moving to common would affect any variants
                    safe_to_move = True
                    impact = []

                    # Check all variants
                    for variant in self.variants:
                        # Get current final value
                        final_path, final_value, _ = self.get_config_value_for_variant(config_name, variant)

                        # Check if this path affects this variant
                        variant_fragments = self.variants[variant]
                        path_affects_variant = False
                        for frag in variant_fragments:
                            frag_parts = frag.split('-')
                            if all(part in str(rhel_path) for part in frag_parts):
                                path_affects_variant = True
                                break

                        if not path_affects_variant:
                            continue

                        # Get the value that would be used after moving to common
                        new_value = None
                        for directory in self.order:
                            if directory.startswith('common/'):
                                continue
                            for frag in variant_fragments:
                                frag_parts = frag.split('-')
                                base_path = Path(*frag_parts)
                                check_path = Path(directory) / base_path / config_name
                                if check_path != rhel_path and check_path != fedora_path and check_path.exists():
                                    value = self.read_config_file(check_path)
                                    if value != '-':
                                        new_value = value
                                        break
                            if new_value is not None:
                                break

                        # If no other configs found, use the common value
                        if new_value is None:
                            new_value = rhel_value

                        if new_value != final_value:
                            safe_to_move = False
                            impact.append(f"variant {variant}: would change from {final_value} to {new_value}")

                    if safe_to_move:
                        common_paths.append((rhel_path, fedora_path, rhel_value))
                    else:
                        self.msg(f"\nKEEP: {rhel_path} and {fedora_path}")
                        self.msg("  Reason: Moving to common would affect:")
                        for i in impact:
                            self.msg(f"    - {i}")
                        self.msg(f"  Current value: {rhel_value}")

        return common_paths

    def move_to_common(self, rhel_path: Path, fedora_path: Path, value: str) -> Path:
        """Move a config file to the common directory."""
        # Create common path
        common_path = Path('common') / rhel_path.relative_to('rhel')

        # Create directory if it doesn't exist
        common_path.parent.mkdir(parents=True, exist_ok=True)

        # Write the value to the common file
        self.write_config_file(common_path, value)

        # Remove the rhel and fedora files
        rhel_path.unlink()
        fedora_path.unlink()

        return common_path

    def process_common_operation(self, config_name: str, priority_files: List[str], args: argparse.Namespace) -> None:
        """Process the common operation for a config."""
        # Find common configs using all priority files
        all_priority_files = ['priority.rhel', 'priority.fedora', 'priority.common']
        common_paths = []
        processed_paths = set()  # Track which paths we've already processed
        # First check in RHEL and Fedora
        for priority_file in ['priority.rhel', 'priority.fedora']:
            reader = ConfigReader(priority_file, args.debug)
            reader.read_priority_file()
            paths = reader.find_common_configs(config_name)
            if paths:
                # Only add paths we haven't processed yet
                for rhel_path, fedora_path, value in paths:
                    if rhel_path not in processed_paths and fedora_path not in processed_paths:
                        common_paths.append((rhel_path, fedora_path, value))
                        processed_paths.add(rhel_path)
                        processed_paths.add(fedora_path)
        if common_paths:
            self.msg(f"\nMoving common configs for {config_name}:")
            for rhel_path, fedora_path, value in common_paths:
                self.msg("Found matching configs:")
                self.msg(f"  RHEL:   {rhel_path} = {value}")
                self.msg(f"  Fedora: {fedora_path} = {value}")
                # Check if moving would affect any variants in any priority file
                safe_to_move = True
                impact = []
                for priority_file in all_priority_files:
                    reader = ConfigReader(priority_file, args.debug)
                    reader.read_priority_file()
                    # Check all variants in this priority file
                    for variant in reader.variants:
                        final_value, new_value = self.check_variant_impact(config_name, rhel_path, fedora_path, value, variant, priority_file)
                        if final_value is not None and new_value != final_value:
                            safe_to_move = False
                            impact.append(f"{priority_file} variant {variant}: would change from {final_value} to {new_value}")
                if safe_to_move:
                    common_path = reader.move_to_common(rhel_path, fedora_path, value)
                    self.msg(f"Moved to: {common_path}")
                else:
                    self.msg(f"KEEP: {rhel_path} and {fedora_path}")
                    self.msg("  Reason: Moving to common would affect:")
                    for i in impact:
                        self.msg(f"    - {i}")
                    self.msg(f"  Current value: {value}")
        else:
            self.msg(f"\nNo common configs found for {config_name}")

    def show_config_values(self, config_name: str, variant: Optional[str] = None, debug: bool = False, prefix: str = '',
                          variant_width: int = 40, value_width: int = 10, path_width: int = 60,
                          variant_padding: int = 2, value_padding: int = 2) -> None:
        """Show values for a specific config."""
        if variant:
            # Show value for specific variant
            path, value, checked_paths = self.get_config_value_for_variant(config_name, variant, debug)
            if value is not None:
                self.msg(f"{prefix}:{variant:<{variant_width-len(prefix)-1}}{' ' * variant_padding}{value:<{value_width}}{' ' * value_padding}{path:<{path_width}}")
            else:
                self.msg(f"{prefix}:{variant:<{variant_width-len(prefix)-1}}{' ' * variant_padding}{'X':<{value_width}}{' ' * value_padding}")

            # Print detailed table
            if checked_paths:  # Only show table if we have paths to check
                self.msg("\nDetailed directory check:")
                # Calculate the maximum path length for table formatting
                max_path_len = max(len(p) for p in checked_paths)

                # self.msg table header
                self.msg(f"{'Path':<{max_path_len}} {'Value':<10}")
                self.msg('-' * (max_path_len + 11))

                # self.msg each path and its value in table format
                for p in checked_paths:
                    p_value = self.read_config_file(Path(p))
                    self.msg(f"{p:<{max_path_len}} {p_value:<10}")
            else:
                self.msg("\nNo directories to check for this variant")
        else:
            # Show values for all variants
            for variant in sorted(self.variants.keys()):
                path, value, _ = self.get_config_value_for_variant(config_name, variant, debug)
                if value is not None:
                    self.msg(f"{prefix}:{variant:<{variant_width-len(prefix)-1}}{' ' * variant_padding}{value:<{value_width}}{' ' * value_padding}{path:<{path_width}}")
                else:
                    self.msg(f"{prefix}:{variant:<{variant_width-len(prefix)-1}}{' ' * variant_padding}{'X':<{value_width}}{' ' * value_padding}")

    def collect_entries(self, config_name: str, variant: Optional[str] = None) -> List[Dict[str, str]]:
        """Collect all entries to calculate column widths."""
        entries: List[Dict[str, str]] = []
        prefix = self.priority_file.replace('priority.', '')
        if variant:
            path, value, _ = self.get_config_value_for_variant(config_name, variant)
            if value is not None:
                entries.append({
                    'variant': f"{prefix}:{variant}",
                    'value': value,
                    'path': str(path) if path is not None else ''
                })
            else:
                entries.append({
                    'variant': f"{prefix}:{variant}",
                    'value': 'X',
                    'path': ''
                })
        else:
            for variant in sorted(self.variants.keys()):
                path, value, _ = self.get_config_value_for_variant(config_name, variant)
                if value is not None:
                    entries.append({
                        'variant': f"{prefix}:{variant}",
                        'value': value,
                        'path': str(path) if path is not None else ''
                    })
                else:
                    entries.append({
                        'variant': f"{prefix}:{variant}",
                        'value': 'X',
                        'path': ''
                    })
        return entries

    def process_show_operation(self, config_name: str, priority_files: List[str], args: argparse.Namespace) -> None:
        """Process the show operation for a config."""
        # First pass: collect all entries to calculate column widths
        all_entries = []
        for priority_file in priority_files:
            reader = ConfigReader(priority_file, args.debug)
            reader.read_priority_file()
            prefix = priority_file.replace('priority.', '')
            entries = reader.collect_entries(config_name, args.variant)
            all_entries.extend(entries)

        # Calculate column widths
        variant_width = max(len(entry['variant']) for entry in all_entries)
        value_width = max(len(entry['value']) for entry in all_entries)
        path_width = max(len(entry['path']) for entry in all_entries)

        # Add padding between columns
        variant_padding = 2
        value_padding = 2

        # Print header
        self.msg(f"\n{config_name}")
        self.msg(f"{'Variant':<{variant_width}} {'Value':<{value_width}} {'Found in':<{path_width}}")
        self.msg('-' * (variant_width + value_width + path_width + variant_padding + value_padding))

        # Second pass: print all entries with consistent column widths
        for priority_file in priority_files:
            reader = ConfigReader(priority_file, args.debug)
            reader.read_priority_file()
            prefix = priority_file.replace('priority.', '')
            reader.show_config_values(config_name, args.variant, args.debug, prefix,
                                   variant_width, value_width, path_width,
                                   variant_padding, value_padding)

    def write_config_file(self, config_path: Path, value: str) -> None:
        """Write a value to a config file."""
        # Create directory if it doesn't exist
        config_path.parent.mkdir(parents=True, exist_ok=True)

        # Read existing content
        existing_lines = []
        if config_path.exists():
            with open(config_path, 'r') as f:
                existing_lines = f.readlines()

        # Find if config already exists
        config_name = config_path.name
        # If config_name doesn't start with CONFIG_, add it
        if not config_name.startswith('CONFIG_'):
            config_name = f'CONFIG_{config_name}'

        found = False
        for i, line in enumerate(existing_lines):
            if line.startswith(f'{config_name}=') or line.startswith(f'# {config_name} '):
                if value == 'n':
                    existing_lines[i] = f'# {config_name} is not set\n'
                else:
                    existing_lines[i] = f'{config_name}={value}\n'
                found = True
                break

        # If not found, append to file
        if not found:
            if value == 'n':
                existing_lines.append(f'# {config_name} is not set\n')
            else:
                existing_lines.append(f'{config_name}={value}\n')

        # Write back to file
        with open(config_path, 'w') as f:
            f.writelines(existing_lines)

    def get_all_configs(self) -> List[str]:
        """Get a list of all config files in the directories."""
        configs = set()
        for directory in self.order:
            for variant in self.variants.values():
                for frag in variant:
                    frag_parts = frag.split('-')
                    base_path = Path(*frag_parts)

                    # Check generic path
                    config_dir = Path(directory) / base_path
                    if config_dir.exists():
                        for config_file in config_dir.glob('CONFIG_*'):
                            value = self.read_config_file(config_file)
                            if value in ['y', 'n', 'm']:
                                configs.add(config_file.name)

                    # Check debug path
                    debug_dir = config_dir / 'debug'
                    if debug_dir.exists():
                        for config_file in debug_dir.glob('CONFIG_*'):
                            value = self.read_config_file(config_file)
                            if value in ['y', 'n', 'm']:
                                configs.add(config_file.name)

        return sorted(configs)

    def find_all_config_locations(self, config_name: str) -> List[Tuple[Path, str]]:
        """Find all locations of a specific config file."""
        locations = []
        # Search in all directories under the current directory
        for root, _, files in os.walk('.'):
            if config_name in files:
                config_path = Path(root) / config_name
                value = self.read_config_file(config_path)
                locations.append((config_path, value))

        return locations

def main() -> None:
    parser = argparse.ArgumentParser(description='Evaluate kernel configs.')
    parser.add_argument('-c', '--config', help='Evaluate specific CONFIGs (file or comma-separated list)')
    parser.add_argument('-d', '--debug', nargs='?', const=1, type=int, choices=[1,2], default=0, help='Debug level (1=basic, 2=verbose)')
    parser.add_argument('-p', '--priority', help='Path to priority file (e.g., priority.rhel)')
    parser.add_argument('-j', '--common', action='store_true', help='Move common configs to common directory')
    parser.add_argument('-f', '--fix', action='store_true', help='Remove redundant config files')
    parser.add_argument('-v', '--variant', help='Show values for specific variant')
    parser.add_argument('-l', '--list', action='store_true', help='List all locations of a config file')
    args = parser.parse_args()

    try:
        # If no priority file specified, use both rhel and fedora
        priority_files = []
        if args.priority:
            priority_files = [args.priority]
        else:
            priority_files = ['priority.rhel', 'priority.fedora']

        if args.list:
            if not args.config:
                print("Error: -c/--config is required when using -l/--list")
                sys.exit(1)

            for priority_file in priority_files:
                reader.msg(f"\nLocations in {priority_file}:")
                reader.msg("-" * 80)
                reader = ConfigReader(priority_file, args.debug)
                reader.read_priority_file()
                locations = reader.find_all_config_locations(args.config)
                if locations:
                    for path, value in sorted(locations):
                        reader.msg(f"{path}: {value}")
                else:
                    reader.msg("No locations found")
            sys.exit(0)

        # Get all configs to process
        configs_to_process = []
        if args.config:
            configs_to_process = [args.config]
        else:
            # Get all configs from the first priority file
            reader = ConfigReader(priority_files[0], args.debug)
            reader.read_priority_file()
            configs_to_process = reader.get_all_configs()
            print(f"Found {len(configs_to_process)} configs to analyze")

        # Process each config
        for i, config_name in enumerate(configs_to_process, 1):
            if args.debug == 0:
                print(f"\r\033[K({i}/{len(configs_to_process)}) Analyzing {config_name}", end='', flush=True)
            else:
                reader.msg(f"\n{'='*80}")
                reader.msg(f"{i}/{len(configs_to_process)} Analyzing {config_name}")
                reader.msg(f"{'='*80}")
            # Process the config based on the operation
            if args.fix:
                reader.process_fix_operation(config_name, priority_files, args)
            elif args.common:
                reader.process_common_operation(config_name, priority_files, args)
            else:
                reader.process_show_operation(config_name, priority_files, args)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
