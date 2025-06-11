# /home/ubuntu/dashboard_v2/utils.py
# -*- coding: utf-8 -*-
"""
Utility functions for the Enhanced Options Dashboard V2, including
configuration management, plotting helpers, caching interaction wrappers,
and formatting utilities.
(Version: Utils Rewrite - Canon Directive - Full Integration)
"""

# Standard Library Imports
import logging
import time as pytime
import json
import copy
import os
from datetime import datetime
from typing import Dict, Any, Optional, Tuple, List, Union

# Third-Party Imports
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from dateutil import parser as date_parser
from dash import html

# Setup logger for this utility module
logger = logging.getLogger(__name__)
# Basic logging config if not already set by a higher-level script (e.g., runner)
if not logging.getLogger().hasHandlers():
    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s] (%(name)s:%(lineno)d) %(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

# --- Attempt to Import Styling for Plotly Template ---
# This is used by create_empty_figure.
# If styling.py is unavailable, a very basic Plotly dark template is used.
_PLOTLY_TEMPLATE_FALLBACK = {"layout": go.Layout(template="plotly_dark")}
PLOTLY_TEMPLATE_DARK: Dict[str, Any]
try:
    from elite_options_system.dashboard.styling import PLOTLY_TEMPLATE_DARK as imported_plotly_template
    PLOTLY_TEMPLATE_DARK = imported_plotly_template
    logger.debug("UTILS.PY: Successfully imported PLOTLY_TEMPLATE_DARK from elite_options_system.dashboard.styling.")
except ImportError:
    logger.warning("UTILS.PY: Could not import PLOTLY_TEMPLATE_DARK from elite_options_system.dashboard.styling. Using basic plotly_dark fallback template for empty figures.")
    PLOTLY_TEMPLATE_DARK = _PLOTLY_TEMPLATE_FALLBACK


# --- Configuration Management ---
CONFIG_CACHE: Optional[Dict[str, Any]] = None # Module-level cache for the application configuration
DEFAULT_CONFIG_FILENAME_UTILS: str = "config.json" # Updated default name

def load_app_config(config_path: str = DEFAULT_CONFIG_FILENAME_UTILS) -> Dict[str, Any]:
    """
    Loads the main application configuration from a JSON file.
    The path is resolved assuming 'utils.py' is in 'elite_options_system/dashboard/',
    and the config file is in 'elite_options_system/'.
    Caches the loaded configuration globally within this module for subsequent calls.
    """
    global CONFIG_CACHE

    if CONFIG_CACHE is not None:
        logger.debug("UTILS: Returning already cached application configuration.")
        return CONFIG_CACHE

    absolute_config_path_to_load: str
    if os.path.isabs(config_path):
        absolute_config_path_to_load = config_path
    else:
        # utils.py is in elite_options_system/dashboard/utils.py
        # We want elite_options_system/config.json
        current_script_directory = os.path.dirname(os.path.abspath(__file__)) # elite_options_system/dashboard/
        project_root_directory = os.path.dirname(current_script_directory)    # elite_options_system/
        absolute_config_path_to_load = os.path.normpath(os.path.join(project_root_directory, config_path))
    
    logger.info(f"UTILS: Attempting to load application configuration from: '{absolute_config_path_to_load}'")

    try:
        with open(absolute_config_path_to_load, "r", encoding="utf-8") as f:
            loaded_config_data = json.load(f)
        if not isinstance(loaded_config_data, dict):
            logger.error(f"UTILS: Config file at '{absolute_config_path_to_load}' did not contain a valid JSON dictionary. Using empty config.")
            CONFIG_CACHE = {}
        else:
            CONFIG_CACHE = loaded_config_data
            logger.info(f"UTILS: Successfully loaded and cached application configuration from '{absolute_config_path_to_load}'.")
    except FileNotFoundError:
        logger.error(f"UTILS: Configuration file not found at '{absolute_config_path_to_load}'. Using empty config.")
        CONFIG_CACHE = {}
    except json.JSONDecodeError as e_json:
        logger.error(f"UTILS: Error decoding JSON from '{absolute_config_path_to_load}': {e_json}. Using empty config.")
        CONFIG_CACHE = {}
    except Exception as e_load:
        logger.error(f"UTILS: Unexpected error loading configuration from '{absolute_config_path_to_load}': {e_load}.", exc_info=True)
        CONFIG_CACHE = {}
    
    return CONFIG_CACHE

def get_config_value(path: List[str], default: Any = None) -> Any:
    """
    Safely retrieves a nested value from the globally cached application configuration.
    Args:
        path (List[str]): A list of keys representing the path to the desired value.
        default (Any, optional): The value to return if the path is not found or an error occurs.
                                 Defaults to None.
    Returns:
        Any: The retrieved configuration value or the default.
    """
    if CONFIG_CACHE is None:
        logger.warning("UTILS: get_config_value called before CONFIG_CACHE was populated. Attempting to load default config now.")
        load_app_config()

    current_level = CONFIG_CACHE
    if not isinstance(current_level, dict):
        logger.error(f"UTILS: CONFIG_CACHE is not a dictionary (type: {type(current_level)}) after load attempt. Cannot retrieve path: {'.'.join(path)}")
        return default

    try:
        for key_segment in path:
            if isinstance(current_level, dict):
                current_level = current_level[key_segment]
            else:
                logger.debug(f"UTILS: Path traversal for '{'.'.join(path)}' failed at non-dictionary for segment '{key_segment}'. Current level type: {type(current_level)}.")
                return default
        return current_level
    except KeyError:
        return default
    except TypeError:
        logger.warning(f"UTILS: Invalid structure or path encountered for '{'.'.join(path)}'. Path segment might be incorrect. Returning default.")
        return default
    except Exception as e_get_val:
        logger.error(f"UTILS: Unexpected error retrieving config value for path '{'.'.join(path)}': {e_get_val}. Returning default.")
        return default

# --- Plotting Utilities ---
def create_empty_figure(title: str = "Waiting for data...", height: Optional[int] = None, reason: str = "N/A") -> go.Figure:
    """ Creates a standard empty Plotly figure with improved styling, using configured defaults. """
    empty_fig_logger = logger.getChild("CreateEmptyFigure")
    empty_fig_logger.debug(f"Creating empty figure with title: '{title}', Reason: '{reason}'")
    
    fig = go.Figure()

    if height is None:
        height = get_config_value(["visualization_settings", "dashboard", "default_graph_height"], 600)
        if not isinstance(height, int) or height <= 0: height = 600

    base_fig_layout = {}
    if isinstance(PLOTLY_TEMPLATE_DARK, dict) and "layout" in PLOTLY_TEMPLATE_DARK:
        base_fig_layout = PLOTLY_TEMPLATE_DARK["layout"]
    elif isinstance(PLOTLY_TEMPLATE_DARK, str):
        base_fig_layout = go.Layout(template=PLOTLY_TEMPLATE_DARK)
    else:
        base_fig_layout = go.Layout(template="plotly_dark")
        empty_fig_logger.warning("PLOTLY_TEMPLATE_DARK from styling was not in expected format. Using basic 'plotly_dark'.")
    
    fig.update_layout(base_fig_layout)

    title_text_with_reason = f"<i>{title}<br><small style='color:grey; font-size:0.8em;'>({reason})</small></i>"
    fig.update_layout(
        title={
            "text": title_text_with_reason,
            "y": 0.5, "x": 0.5,
            "xanchor": "center", "yanchor": "middle",
            "font": {"size": 16, "color": "#95a5a6"}
        },
        height=height,
        xaxis={"visible": False, "showgrid": False, "zeroline": False}, 
        yaxis={"visible": False, "showgrid": False, "zeroline": False},
        annotations=[],
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig

# --- Data Handling & Caching Utilities ---
_cache_timeout_config_path = ["system_settings", "dashboard_cache_timeout_seconds"]
_cache_timeout_default = 600
CACHE_TIMEOUT_SECONDS: int = get_config_value(_cache_timeout_config_path, _cache_timeout_default)
if not isinstance(CACHE_TIMEOUT_SECONDS, int) or CACHE_TIMEOUT_SECONDS < 0:
    logger.warning(f"Invalid CACHE_TIMEOUT_SECONDS '{CACHE_TIMEOUT_SECONDS}' from config. Defaulting to {_cache_timeout_default}s.")
    CACHE_TIMEOUT_SECONDS = _cache_timeout_default
logger.info(f"UTILS: Cache timeout set to {CACHE_TIMEOUT_SECONDS} seconds.")

def generate_cache_key(symbol: str, dte_str: str, range_pct: Optional[Union[int, float]]) -> str:
    """
    Generates a consistent cache key from input parameters.
    Includes symbol, DTE string, range, and current minute for time-sensitivity.
    """
    range_val_for_key = int(range_pct) if isinstance(range_pct, (int, float)) and pd.notna(range_pct) else 0
    timestamp_minute_str = datetime.now().strftime('%Y%m%d%H%M')
    cache_key_generated = f"{str(symbol).strip().upper()}_{str(dte_str).strip()}_{range_val_for_key}pct_{timestamp_minute_str}"
    logger.debug(f"UTILS: Generated cache key: '{cache_key_generated}'")
    return cache_key_generated

def get_data_from_server_cache(cache_key: Optional[str], server_cache_ref: Dict[str, Tuple[float, Dict[str, Any]]]) -> Optional[Dict[str, Any]]:
    """
    Retrieves data from the main server-side cache if the key exists and data hasn't expired.
    Returns a deep copy of the cached bundle to prevent mutation issues.
    Expects the cached data bundle to have 'options_chain' as a list-of-dicts.
    """
    cache_get_logger = logger.getChild("CacheGet")
    if not cache_key or not isinstance(cache_key, str):
        cache_get_logger.debug(f"Invalid cache key provided (type: {type(cache_key)}, value: '{cache_key}'). Cannot retrieve from cache.")
        return None
    if cache_key not in server_cache_ref:
        cache_get_logger.debug(f"Key '{cache_key}' not found in server cache.")
        return None

    stored_timestamp, stored_data_bundle = server_cache_ref[cache_key]

    current_time_secs = pytime.time()
    age_seconds = current_time_secs - stored_timestamp
    if age_seconds > CACHE_TIMEOUT_SECONDS:
        cache_get_logger.info(f"Key '{cache_key}' has expired (Age: {age_seconds:.1f}s > Timeout: {CACHE_TIMEOUT_SECONDS}s). Removing from cache.")
        server_cache_ref.pop(cache_key, None)
        return None

    if not isinstance(stored_data_bundle, dict):
        cache_get_logger.error(f"Corrupted cache entry for key '{cache_key}': Stored data is not a dictionary (Type: {type(stored_data_bundle)}). Removing.")
        server_cache_ref.pop(cache_key, None)
        return None
    
    options_chain_in_bundle = stored_data_bundle.get("processed_data", {}).get("options_chain")
    if isinstance(options_chain_in_bundle, pd.DataFrame):
         cache_get_logger.error(f"CRITICAL CACHE CORRUPTION for key '{cache_key}': 'options_chain' retrieved from cache is a DataFrame! Should be list of dicts.")
    elif not isinstance(options_chain_in_bundle, list):
        cache_get_logger.warning(f"Cache data for key '{cache_key}': 'options_chain' is not a list (Type: {type(options_chain_in_bundle)}). Plotting might fail if expecting list of records.")

    cache_get_logger.debug(f"Retrieved valid (non-expired) data bundle for key: '{cache_key}'. Age: {age_seconds:.1f}s.")
    try:
        return copy.deepcopy(stored_data_bundle)
    except Exception as e_deepcopy:
        cache_get_logger.error(f"Failed to deep copy cached data for key '{cache_key}': {e_deepcopy}. Returning original reference (MUTABLE).", exc_info=True)
        return stored_data_bundle

def store_data_in_server_cache(cache_key: Optional[str], data_bundle_to_store: Dict[str, Any], server_cache_ref: Dict[str, Tuple[float, Dict[str, Any]]]):
    """
    Stores the data bundle in the main server-side cache with a current timestamp.
    Performs a deep copy of the bundle before storing to ensure cache integrity.
    Includes Point C style logging to check 'options_chain' format before storage.
    """
    cache_store_logger = logger.getChild("CacheStore")
    if not cache_key or not isinstance(cache_key, str):
        cache_store_logger.error(f"Invalid cache key provided (type: {type(cache_key)}, value: '{cache_key}'). Cannot store data.")
        return
    if not isinstance(data_bundle_to_store, dict):
        cache_store_logger.error(f"Cannot store non-dictionary data in cache for key '{cache_key}'. Provided data type: {type(data_bundle_to_store)}")
        return

    try:
        bundle_for_storage = copy.deepcopy(data_bundle_to_store)
    except Exception as e_deepcopy_store:
         cache_store_logger.error(f"Failed to deep copy data bundle before caching for key '{cache_key}': {e_deepcopy_store}. Storing original reference (RISK OF MUTATION).", exc_info=True)
         bundle_for_storage = data_bundle_to_store

    options_chain_data_in_bundle = bundle_for_storage.get("processed_data", {}).get("options_chain")
    if isinstance(options_chain_data_in_bundle, list):
        if options_chain_data_in_bundle:
            first_record_check = options_chain_data_in_bundle[0]
            if isinstance(first_record_check, dict):
                rolling_cols_for_log = [col for col in first_record_check.keys() if 'volmbs_' in col or 'valuebs_' in col]
                if rolling_cols_for_log:
                    rolling_vals_log = {k: (v, type(v).__name__) for k,v in first_record_check.items() if k in rolling_cols_for_log}
                    cache_store_logger.debug(f"UTILS STORE CHECK ({cache_key}): Rolling vals/types in first rec before store: {rolling_vals_log}")
                    if any(not isinstance(val_type_tuple[0], (int, float, type(None), np.number)) for val_type_tuple in rolling_vals_log.values()):
                         cache_store_logger.error(f"UTILS STORE CHECK ({cache_key}): CRITICAL - Rolling column has non-numeric/None type just before storing!")
                else: cache_store_logger.debug(f"UTILS STORE CHECK ({cache_key}): No 'volmbs_' or 'valuebs_' keys in first record of options_chain.")
            else: cache_store_logger.warning(f"UTILS STORE CHECK ({cache_key}): First item in 'options_chain' list is not a dictionary. Type: {type(first_record_check)}")
        else: cache_store_logger.debug(f"UTILS STORE CHECK ({cache_key}): 'options_chain' is an empty list.")
    elif isinstance(options_chain_data_in_bundle, pd.DataFrame):
         cache_store_logger.error(f"UTILS STORE ERROR ({cache_key}): 'options_chain' is a DataFrame JUST BEFORE STORING! Processor's JSON-safe conversion was bypassed or failed.")
    else:
         cache_store_logger.warning(f"UTILS STORE CHECK ({cache_key}): 'options_chain' data type before storing is '{type(options_chain_data_in_bundle)}'. Expected list of dicts.")

    server_cache_ref[cache_key] = (pytime.time(), bundle_for_storage)
    cache_store_logger.info(f"Stored data bundle with key: '{cache_key}'. Current server cache size: {len(server_cache_ref)}")


# --- Formatting & Display Utilities ---
def format_status_message(message: str, is_error: bool = False) -> Tuple[Union[str, html.Div], Dict[str, str]]:
    """
    Formats a status message string for display and returns an appropriate style dictionary.
    Uses html.Div for consistent component type return.
    """
    base_style_cfg_path = ["visualization_settings", "dashboard", "styles", "status_display", "base"]
    base_style_default = {"padding": "10px", "textAlign": "center", "borderRadius": "5px", "fontSize": "1em", "minHeight": "30px", "fontWeight":"500"}
    base_style = get_config_value(base_style_cfg_path, base_style_default)
    if not isinstance(base_style, dict): base_style = base_style_default

    final_style: Dict[str,str]
    if is_error:
        error_style_cfg_path = ["visualization_settings", "dashboard", "styles", "status_display", "error"]
        error_style_default = {"color": "#f8d7da", "backgroundColor": "#721c24", "border": "1px solid #f5c6cb"}
        error_style = get_config_value(error_style_cfg_path, error_style_default)
        if not isinstance(error_style, dict): error_style = error_style_default
        final_style = {**base_style, **error_style}
        prefix = "Error: " if not ("error" in message.lower() or "failed" in message.lower() or "critical" in message.lower()) else ""
        display_message = f"{prefix}{message}"
    else:
        is_success_msg = any(keyword in message.lower() for keyword in ["success", "loaded", "completed", "✓"])
        if is_success_msg:
            success_style_cfg_path = ["visualization_settings", "dashboard", "styles", "status_display", "success"]
            success_style_default = {"color": "#d4edda", "backgroundColor": "#155724", "border": "1px solid #c3e6cb"}
            success_style = get_config_value(success_style_cfg_path, success_style_default)
            if not isinstance(success_style, dict): success_style = success_style_default
            final_style = {**base_style, **success_style}
        else:
            info_style_cfg_path = ["visualization_settings", "dashboard", "styles", "status_display", "info"]
            info_style_default = {"color": "#bee5eb", "backgroundColor": "#0c5460", "border": "1px solid #bee5eb"}
            info_style = get_config_value(info_style_cfg_path, info_style_default)
            if not isinstance(info_style, dict): info_style = info_style_default
            final_style = {**base_style, **info_style}
        display_message = message
    
    return html.Div(display_message), final_style

def parse_timestamp(timestamp_string: Optional[str]) -> Optional[datetime]:
    """
    Safely parses an ISO format timestamp string (or other common formats)
    into a timezone-aware or naive datetime object using dateutil.parser.
    Returns None if parsing fails or input is invalid.
    """
    if not timestamp_string or not isinstance(timestamp_string, str):
        return None
    try:
        parsed_datetime_object = date_parser.parse(timestamp_string)
        return parsed_datetime_object
    except (ValueError, TypeError, OverflowError) as e_parse:
        logger.warning(f"UTILS: Could not parse timestamp string '{timestamp_string}': {e_parse}")
        return None
    except Exception as e_unknown_parse:
        logger.error(f"UTILS: Unexpected error parsing timestamp string '{timestamp_string}': {e_unknown_parse}", exc_info=True)
        return None

# app_config_main = load_app_config()
# some_setting = get_config_value(["path","to","setting"], "default_val")
