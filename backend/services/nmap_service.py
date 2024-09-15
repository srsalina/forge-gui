import subprocess
import shlex
import logging
import xmltodict
from defusedxml import defuse_stdlib
defuse_stdlib()
from defusedxml import ElementTree as ET
from xml.parsers.expat import ExpatError
import ipaddress
import re

# Custom Exceptions
class NmapError(Exception):
    """Base exception class for Nmap errors."""
    pass

class NmapScanError(NmapError):
    pass

class NmapParseError(NmapError):
    pass

def validate_targets(targets):
    """
    Validates a string containing one or more target specifications for Nmap.

    Parameters:
    - targets (str): The target specification(s) as a string.

    Returns:
    - bool: True if all targets are valid, False otherwise.
    """
    targets_list = shlex.split(targets)
    for target in targets_list:
        target = target.strip()
        # Validate IPv4 address
        try:
            ipaddress.IPv4Address(target)
            continue
        except ValueError:
            pass
        # Validate IPv4 CIDR notation
        try:
            ipaddress.IPv4Network(target, strict=False)
            continue
        except ValueError:
            pass
        # Validate IPv6 address
        try:
            ipaddress.IPv6Address(target)
            continue
        except ValueError:
            pass
        # Validate IPv6 CIDR notation
        try:
            ipaddress.IPv6Network(target, strict=False)
            continue
        except ValueError:
            pass
        # Validate IP range (e.g., 192.168.1.1-254)
        ip_range_pattern = re.compile(
            r"^(?:\d{1,3}\.){3}\d{1,3}-\d{1,3}$"
        )
        if ip_range_pattern.match(target):
            continue
        # Validate domain name (allowing single-label hostnames)
        domain_pattern = re.compile(
            r"^(?=.{1,253}$)(?!-)[A-Za-z0-9][A-Za-z0-9\-]{0,61}[A-Za-z0-9]?(?:\.[A-Za-z]{2,})*$"
        )
        if domain_pattern.match(target):
            continue
        # Wildcard domain (basic validation)
        if target.startswith('*.'):
            if domain_pattern.match(target[2:]):
                continue
        # If none of the above, invalid target
        return False
    return True

# Mapping of allowed options and expected argument counts
OPTION_ARGUMENTS = {
    '-sV': 0,
    '-sC': 0,
    '-Pn': 0,
    '-A': 0,
    '-O': 0,
    '-p': 1,     # '-p' expects one argument
    '--top-ports': 1  # Example of long option with argument
}

def validate_options(options):
    """
    Validates the Nmap options provided by the user.

    Parameters:
    - options (str): The Nmap options string.

    Returns:
    - bool: True if all options are valid and allowed, False otherwise.
    """
    options_list = shlex.split(options)
    i = 0
    while i < len(options_list):
        opt = options_list[i]
        if opt in OPTION_ARGUMENTS:
            arg_count = OPTION_ARGUMENTS[opt]
            i += 1  # Move to the next item
            # Check for required arguments
            for _ in range(arg_count):
                if i >= len(options_list) or options_list[i].startswith('-'):
                    # Missing argument for the option
                    return False
                i += 1
        else:
            # Option not allowed
            return False
    return True

def run_nmap(targets, options, timeout=300):
    """
    Runs an Nmap scan on the specified targets with given options.

    Parameters:
    - targets (str): The target specification(s) to scan.
    - options (str): Nmap command options.
    - timeout (int, optional): Maximum time in seconds to allow the scan to run.

    Returns:
    - dict: Parsed Nmap scan results.

    Raises:
    - ValueError: If the targets or options are invalid.
    - TimeoutError: If the scan exceeds the specified timeout.
    - NmapScanError: If Nmap returns an error.
    - NmapParseError: If parsing the Nmap output fails.
    """
    if not validate_targets(targets):
        raise ValueError('Invalid target format.')

    if not validate_options(options):
        raise ValueError('Invalid or disallowed Nmap options.')

    # Sanitize inputs
    targets_list = shlex.split(targets)
    options_list = shlex.split(options)

    # Construct the Nmap command as a list
    command = ['nmap'] + options_list + ['-oX', '-'] + targets_list  # Output in XML format

    logging.info(f"Starting Nmap scan on targets: {' '.join(targets_list)} with options: {options}")

    try:
        # Execute the command
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        if result.returncode != 0:
            logging.error(f"Nmap scan error: {result.stderr.strip()}")
            raise NmapScanError(result.stderr.strip())
        # Parse XML output
        xml_output = result.stdout
        try:
            nmap_dict = xmltodict.parse(xml_output)
            logging.info('Nmap scan completed successfully.')
            return nmap_dict
        except ExpatError as e:
            logging.error(f'Failed to parse Nmap XML output: {str(e)}')
            raise NmapParseError('Failed to parse Nmap output.')
        except ET.ParseError as e:
            logging.error(f'Failed to parse Nmap XML output: {str(e)}')
            raise NmapParseError('Failed to parse Nmap output.')
        except Exception as e:
            logging.error(f'Unexpected error during XML parsing: {str(e)}')
            raise NmapParseError('An unexpected error occurred during XML parsing.')
    except subprocess.TimeoutExpired:
        logging.error('Nmap scan timed out.')
        raise TimeoutError('Nmap scan timed out.')
    except FileNotFoundError:
        logging.error('Nmap command not found.')
        raise NmapScanError('Nmap command not found.')
    except subprocess.SubprocessError as e:
        logging.error(f'Subprocess error: {str(e)}')
        raise NmapScanError(f'Subprocess error: {str(e)}')
