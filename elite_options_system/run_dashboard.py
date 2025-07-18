#!/usr/bin/env python3
"""
Enhanced Options Dashboard Runner Script (V2.1 - Canon Directive)

This script serves as a robust launcher for the Enhanced Options Dashboard application.
It performs pre-flight checks for dependencies, environment configurations, and
directory structures, and loads key settings from a central configuration file
(defaulting to config.json) before attempting to start the Dash server.
Now includes check for MSPIVisualizerV2 output directory.

Key Features:
-   Dynamic loading of dashboard module path from configuration.
-   Dynamic creation of required directories based on configuration.
-   Comprehensive logging and error handling.
-   Command-line arguments for server host, port, production mode, API checks,
    and custom configuration file path.
-   Checks for Python package dependencies and API credentials.
-   Attempts graceful cleanup on shutdown.
"""

# Standard Library Imports
import os
import sys
import argparse
import logging
import traceback
import importlib # For robust dependency checking
import json
from typing import Optional, List, Dict, Any, Tuple

# --- Python Path Adjustment for Package Resolution ---
# This script (run_dashboard.py) is now at the root of the 'elite_options_system' project.
# The packages 'core', 'services', 'dashboard', 'utils' are subdirectories.
# The current working directory when running 'python elite_options_system/run_dashboard.py'
# might be the parent of 'elite_options_system', or 'elite_options_system' itself.
# To ensure imports like 'from elite_options_system.dashboard.app import ...' work,
# the directory *containing* 'elite_options_system' must be in sys.path.

# Get the directory of this script (elite_options_system/run_dashboard.py)
# -> .../elite_options_system/
current_script_dir_rl = os.path.dirname(os.path.abspath(__file__))

# Get the parent of the script's directory (this should be the directory *containing* elite_options_system)
# -> .../ (parent of elite_options_system)
project_parent_dir_rl = os.path.dirname(current_script_dir_rl)

# Add this parent directory to sys.path if it's not already there
if project_parent_dir_rl not in sys.path:
    sys.path.insert(0, project_parent_dir_rl)
    print(f"INFO (run_dashboard.py): Added '{project_parent_dir_rl}' to sys.path for package discovery.")
else:
    print(f"INFO (run_dashboard.py): '{project_parent_dir_rl}' already in sys.path.")


# --- Initial Configuration ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)-8s] %(name)-15s: %(message)s (%(filename)s:%(lineno)d)',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("DashboardRunnerV2.1")

# The script is now in elite_options_system, so config is in the same directory
DEFAULT_CONFIG_FILENAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
DEFAULT_ENV_FILENAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")


PYTHON_PACKAGES = [
    "dash", "pandas", "numpy", "plotly", "requests",
    "dotenv", "dateutil", "convexlib", "dash_bootstrap_components",
    "psycopg2-binary", "scikit-learn", "joblib", "scipy"
]

# --- Helper Functions ---

def load_configuration(config_path: str) -> Optional[Dict[str, Any]]:
    """Loads the JSON configuration file."""
    logger.info(f"Attempting to load configuration from: {config_path}")
    try:
        with open(config_path, 'r', encoding='utf-8') as f: # Added encoding
            config = json.load(f)
        logger.info(f"Successfully loaded configuration from {config_path}.")
        return config
    except FileNotFoundError:
        logger.error(f"FATAL ERROR: Configuration file not found at {config_path}.")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"FATAL ERROR: Could not parse JSON configuration file {config_path}: {e}")
        return None
    except Exception as e:
        logger.error(f"FATAL ERROR: An unexpected error occurred while loading {config_path}: {e}", exc_info=True)
        return None

def get_required_directories_from_config(config: Dict[str, Any]) -> List[str]:
    """
    Extracts required directory paths from the configuration.
    Uses absolute paths based on the config file location if paths are relative.
    """
    config_file_abs_path = config.get("_config_file_path", os.path.abspath(DEFAULT_CONFIG_FILENAME))
    # base_path is now the directory containing config.json (elite_options_system/)
    base_path = os.path.dirname(config_file_abs_path)
    logger.debug(f"Base path for resolving relative directories (runner): {base_path}")
    dirs_to_check = set()

    def _get_and_resolve_path(keys: List[str], default_relative_path: Optional[str] = None) -> Optional[str]:
        current_val = config
        try:
            for key_item in keys:
                current_val = current_val[key_item]
            path_str = str(current_val) if isinstance(current_val, str) else None
        except (KeyError, TypeError):
            path_str = default_relative_path
            if default_relative_path:
                logger.debug(f"Path {' -> '.join(keys)} not found or invalid in config. Using default relative path: '{default_relative_path}'")
            else:
                logger.debug(f"Path {' -> '.join(keys)} not found or invalid in config and no default specified.")
                return None

        if path_str:
            # Relative paths in config are now relative to the project root (elite_options_system/)
            resolved = os.path.join(base_path, path_str) if not os.path.isabs(path_str) else path_str
            return os.path.normpath(resolved)
        return None

    # 1. Processed Data Directory (system_settings.data_directory)
    # Example: if config has "data_processed_by_processor", it becomes elite_options_system/data_processed_by_processor
    dirs_to_check.add(_get_and_resolve_path(["system_settings", "data_directory"], "data_processed_by_processor"))

    # 2. Raw Data Directory (convention)
    # This will be elite_options_system/data/raw_data
    dirs_to_check.add(os.path.normpath(os.path.join(base_path, "data", "raw_data")))
    logger.debug(f"Adding conventional raw data directory: {os.path.join(base_path, 'data', 'raw_data')}")

    # 3. Dashboard Visualizations Output Directory (visualization_settings.dashboard.output_directory)
    # This is for general dashboard outputs, not the visualizer module's specific outputs.
    # If config has "dashboard_visualizations", it becomes elite_options_system/dashboard_visualizations
    dirs_to_check.add(_get_and_resolve_path(["visualization_settings", "dashboard", "output_directory"], "dashboard_visualizations"))

    # 4. MSPIVisualizerV2 Output Directory (visualization_settings.mspi_visualizer.output_dir)
    # If config has "mspi_visualizations_output_v2", it becomes elite_options_system/mspi_visualizations_output_v2
    dirs_to_check.add(_get_and_resolve_path(["visualization_settings", "mspi_visualizer", "output_dir"], "mspi_visualizations_output_v2"))

    # 5. Dashboard Assets Directory
    # This should point to elite_options_system/dashboard/assets/
    # The dashboard_module_path is now relative to elite_options_system
    dashboard_module_path_from_config = config.get("runner_settings", {}).get("dashboard_module_path", "elite_options_system.dashboard.app")

    # We know 'dashboard' is a top-level package within 'elite_options_system'
    # So, assets_dir is base_path (elite_options_system) / 'dashboard' / 'assets'
    assets_dir_path = os.path.normpath(os.path.join(base_path, "dashboard", "assets"))
    dirs_to_check.add(assets_dir_path)
    logger.debug(f"Derived assets directory for dashboard module: {assets_dir_path}")

    final_dirs_list = [d for d in list(dirs_to_check) if d is not None]
    logger.info(f"Required directories identified by runner: {final_dirs_list}")
    return final_dirs_list

def check_python_packages(packages: List[str]) -> bool:
    logger.info("Checking required Python package imports..."); missing = []
    for pkg_name in packages:
        try: base_pkg = pkg_name.split('==')[0].split('>')[0].split('<')[0].split('[')[0].replace("-","_"); importlib.import_module(base_pkg if base_pkg != "python_dotenv" else "dotenv"); logger.debug(f"  - Package '{pkg_name}' found.")
        except ImportError: logger.error(f"  - Required package '{pkg_name}' NOT installed."); missing.append(pkg_name)
        except Exception as e_pkg: logger.error(f"  - Error checking pkg '{pkg_name}': {e_pkg}"); missing.append(pkg_name)
    if missing: logger.error(f"FATAL: Missing packages: {missing}. Install via pip or requirements.txt."); return False
    logger.info("All required Python packages seem installed."); return True

def check_environment_variables(config: Dict[str, Any]) -> Tuple[bool, Optional[str], Optional[str]]:
    logger.info("Checking API credentials...");
    try:
        from dotenv import load_dotenv
        env_path = DEFAULT_ENV_FILENAME
        if os.path.exists(env_path):
            loaded_custom_env = load_dotenv(dotenv_path=env_path, verbose=True)
            logger.info(f"Loaded .env file ('{env_path}'): {loaded_custom_env}")
        else:
            logger.info(f".env file not found at '{env_path}'. Relying on system environment variables or config for API creds.")
            loaded_standard_env = load_dotenv(verbose=True)
            if loaded_standard_env:
                 logger.info(f"Loaded .env from standard location: {loaded_standard_env}")

    except ImportError: logger.warning("'python-dotenv' not found. Cannot load .env. Install with 'pip install python-dotenv'.")
    except Exception as e_dot: logger.warning(f"Error loading .env: {e_dot}")
    api_cfg = config.get("api_credentials",{}); email_var=api_cfg.get("email_env_var","CONVEX_EMAIL"); pass_var=api_cfg.get("password_env_var","CONVEX_PASSWORD")
    email, passwd = os.getenv(email_var), os.getenv(pass_var)
    if email and passwd: logger.info(f"API creds ({email_var}, {pass_var}) found in ENV."); return True, email, passwd
    logger.warning(f"API creds not in ENV. Checking config..."); email, passwd = api_cfg.get("convex_email"), api_cfg.get("convex_password")
    if email and passwd: logger.warning(f"Using API creds from config (less secure)."); return True, email, passwd
    logger.error(f"FATAL: API Credentials NOT FOUND for {email_var}/{pass_var} in ENV or config. Data fetching will fail."); return False, None, None

def ensure_directories(dir_list: List[str]) -> bool:
    if not dir_list: logger.info("No specific directories to check/create."); return True
    logger.info(f"Ensuring directories: {dir_list}"); all_ok = True
    for d_path in dir_list:
        if not d_path: continue
        try: os.makedirs(d_path, exist_ok=True); logger.debug(f"  - Directory '{d_path}' ensured.")
        except Exception as e_dir: logger.error(f"  - FAILED creating directory '{d_path}': {e}", exc_info=True); all_ok = False
    if not all_ok: logger.error("FATAL: Failed to create one or more required directories."); return False
    logger.info("All required directories verified/created."); return True

def attempt_app_import(app_module_name: str) -> Optional[Tuple[Any, Any, Optional[Any], Optional[Any]]]:
    logger.info(f"Attempting to import app components from module: '{app_module_name}'...")
    try:
        # Corrected import path for the new structure
        # app_module_name will be like "elite_options_system.dashboard.app"
        app_mod = importlib.import_module(app_module_name)
        dash_app, dash_server = getattr(app_mod,'app',None), getattr(app_mod,'server',None)
        # FETCHER_INSTANCE and cleanup_cache are attributes of the app_mod (dashboard.app)
        fetcher_inst, cleanup_func = getattr(app_mod,'FETCHER_INSTANCE',None), getattr(app_mod,'cleanup_cache',None)
        if dash_app is None or dash_server is None: raise ImportError(f"'app' or 'server' not in '{app_module_name}'.")
        logger.info(f"Successfully imported 'app', 'server', related components from '{app_module_name}'.")
        return dash_app, dash_server, fetcher_inst, cleanup_func
    except Exception as e_imp: logger.critical(f"FATAL IMPORT ERROR from '{app_module_name}': {e_imp}\n{traceback.format_exc()}"); return None

def main():
    """Main execution function."""
    logger.info("====================================================================================================================")
    logger.info("=== Starting Enhanced Options Dashboard Runner Script (V2.1 Canon) ===")
    logger.info("====================================================================================================================")

    parser = argparse.ArgumentParser(description="Run Enhanced Options Dashboard V2.1")
    parser.add_argument("--config-path", type=str, default=DEFAULT_CONFIG_FILENAME, help=f"Config file path (default: {DEFAULT_CONFIG_FILENAME})")
    parser.add_argument("--production", action="store_true", help="Run in production mode (disables Dash debug)")
    parser.add_argument("--host", type=str, default=None, help="Server host IP (overrides config)")
    parser.add_argument("--port", type=int, default=None, help="Server port (overrides config)")
    parser.add_argument("--skip-api-check", action="store_true", help="Skip API credential validation")
    args = parser.parse_args()

    config = load_configuration(args.config_path)
    if config is None: sys.exit(1)
    config["_config_file_path"] = os.path.abspath(args.config_path)

    final_host = args.host if args.host is not None else config.get("system_settings", {}).get("dashboard_host", "0.0.0.0")
    final_port = args.port if args.port is not None else config.get("system_settings", {}).get("dashboard_port", 8050)
    logger.info(f"Config: {args.config_path}, Mode: {'PROD' if args.production else 'DEV'}, Host: {final_host}, Port: {final_port}, SkipAPI: {args.skip_api_check}")

    if not check_python_packages(PYTHON_PACKAGES): sys.exit(1)
    if not args.skip_api_check and not check_environment_variables(config)[0]: sys.exit(1)
    
    required_dirs = get_required_directories_from_config(config)
    if not ensure_directories(required_dirs): sys.exit(1)

    # The dashboard_module_path in config.json should now be "elite_options_system.dashboard.app"
    app_module_path_from_config = config.get("runner_settings", {}).get("dashboard_module_path", "elite_options_system.dashboard.app")
    logger.info(f"Dashboard module path from config: {app_module_path_from_config}")

    import_result = attempt_app_import(app_module_path_from_config)
    if import_result is None: sys.exit(1)
    app, server, _, cleanup_cache_on_exit = import_result

    debug_server_mode = not args.production
    logger.info(f"Starting Dash server (Debug: {debug_server_mode}). Access: http://{final_host}:{final_port}")
    print("-" * 60 + f"\nDashboard available at: http://{final_host}:{final_port}" + (" (and http://127.0.0.1:{final_port})" if final_host == '0.0.0.0' else "") + "\n" + "-" * 60 + "\nPress CTRL+C to stop.", flush=True)

    try:
        # Use app.run_server for Dash 2.0+
        app.run_server(debug=debug_server_mode, host=final_host, port=final_port, use_reloader=False, dev_tools_hot_reload=False)
    except Exception as e_run: logger.critical(f"FATAL DASH SERVER ERROR: {e_run}\n{traceback.format_exc()}"); sys.exit(1)
    finally:
        logger.info("Server stopped. Attempting cleanup...")
        if cleanup_cache_on_exit and callable(cleanup_cache_on_exit):
            try: cleanup_cache_on_exit(); logger.info("Dashboard cleanup executed.")
            except Exception as e_clean: logger.warning(f"Error during cleanup: {e_clean}", exc_info=True)
        else: logger.info("No specific cleanup function found or callable.")
        logger.info("Dashboard runner shutdown complete.")

if __name__ == '__main__':
    main()
