# set up to work with a schema

# def setup_logger(name):
#     """
#     Set up a logger with a specific name to avoid duplicate logs.
#     """
#     logger = logging.getLogger(name)
#     if not logger.hasHandlers():
#         # Create handlers only if there are none
#         stdout_handler = logging.StreamHandler()
#         file_handler = logging.FileHandler("missing_columns.log")

#         # Set levels
#         stdout_handler.setLevel(logging.WARNING)
#         file_handler.setLevel(logging.WARNING)

#         # Create formatter and add it to the handlers
#         formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
#         stdout_handler.setFormatter(formatter)
#         file_handler.setFormatter(formatter)

#         # Add handlers to the logger
#         logger.addHandler(stdout_handler)
#         logger.addHandler(file_handler)

#     return logger


# # In your log_missing_columns function
# def log_missing_columns(df_stats: pd.DataFrame, template_df: pd.DataFrame):
#     # Initialize the loggers
#     logger = setup_logger(__name__)

#     # Example column lists
#     template_columns = template_df.columns
#     df_stats_columns = df_stats.columns

#     # Find missing columns
#     missing_in_template = [col for col in df_stats_columns if col not in template_columns]
#     missing_in_stats = [col for col in template_columns if col not in df_stats_columns]

#     # Log results for missing columns in df_stats
#     if missing_in_template:
#         logger.warning(f"The following columns in 'df_stats' did not match any columns in 'template_df': {', '.join(missing_in_template)}")
#     else:
#         logger.info("All columns from 'df_stats' found in 'template_df'.")

#     # Log results for missing columns in template_df
#     if missing_in_stats:
#         logger.warning(f"The following columns in 'template_df' did not match any columns in 'df_stats': {', '.join(missing_in_stats)}")
#     else:
#         logger.info("All columns from 'template_df' found in 'df_stats'.")


# def reformat_stats_to_template(df_stats, template_df=None, lookup_csvs=None) -> pd.DataFrame:
#     # Ensure df_stats is a DataFrame
#     if not isinstance(df_stats, pd.DataFrame):
#         raise ValueError("'df_stats' must be a pandas DataFrame.")

#     # Ensure only one of 'template_df' or 'lookup_csvs' is provided
#     if template_df is not None and lookup_csvs is not None:
#         raise ValueError("Only one of 'template_df' or 'lookup_csvs' can be specified, not both.")

#     # If template_df is provided, ensure it is a DataFrame
#     if template_df is not None and not isinstance(template_df, pd.DataFrame):
#         raise ValueError("'template_df' must be a pandas DataFrame.")

#     if lookup_csvs is None:
#         lookup_csvs_temp=[DEFAULT_GEE_DATASETS_LOOKUP_TABLE_PATH, DEFAULT_CONTEXT_LOOKUP_TABLE_PATH]
#         template_df = create_template_from_csvs(lookup_csvs_temp)

#     # If lookup_csvs is provided, handle either a single path or a list of paths
#     elif lookup_csvs is not None:

#         # if isinstance(lookup_csvs, str):
#         #     # If it's a single string path, convert it to a list with one element
#         #     lookup_csvs = [lookup_csvs]
#         # elif not isinstance(lookup_csvs, list):
#         #     raise ValueError("'lookup_csvs' must be a string or a list of paths.")

#         # Create a template from the provided lookup CSVs
#         template_df = create_template_from_csvs(lookup_csvs)

#     # Append the stats from df_stats to the prepared template DataFrame
#     return append_stats_to_template(template_df, df_stats)


# def create_template_from_dataframes(dataframes) -> pd.DataFrame:
#     """
#     Combines a single DataFrame or a list of DataFrames, creates a template DataFrame,
#     and removes 'name' from the column names at the end.
#     It filters out rows where 'exclude_from_output' == 1.

#     Args:
#     - dataframes (pd.DataFrame or list of pd.DataFrame): DataFrame(s) to combine.

#     Returns:
#     - pd.DataFrame: The resulting template DataFrame with transposed 'name' as columns.

#     Raises:
#     - ValueError: If 'name', 'exclude_from_output', or 'order' columns are missing.
#     """

#     # Check if input is a single DataFrame or a list of DataFrames
#     if isinstance(dataframes, pd.DataFrame):
#         dataframes = [dataframes]  # Convert to a list
#     elif not isinstance(dataframes, list) or not all(isinstance(df, pd.DataFrame) for df in dataframes):
#         raise ValueError("Input must be a single DataFrame or a list of DataFrames.")

#     # Combine DataFrames
#     combined_df = pd.concat(dataframes, ignore_index=True)

#     # Check for required columns
#     required_columns = ['name', 'exclude_from_output', 'order']
#     missing_columns = [col for col in required_columns if col not in combined_df.columns]

#     if missing_columns:
#         raise ValueError(f"The following required columns are missing: {', '.join(missing_columns)}")

#     # Filter out rows where 'exclude_from_output' is 1
#     df_filtered = combined_df[combined_df['exclude_from_output'] != 1]

#     # Sort by 'order' column in ascending order
#     df_sorted = df_filtered.sort_values(by='order')

#     # Create an empty DataFrame with 'name' as the column names
#     template_df = pd.DataFrame(columns=df_sorted['name'])

#     # Remove the 'name' column from the final DataFrame before returning
#     template_df.drop(columns=['name'], inplace=True, errors='ignore')

#     return template_df


# def create_template_from_csvs(csv_files) -> pd.DataFrame:
#     """
#     Reads one or more CSV files, combines them into a DataFrame, creates a template DataFrame,
#     and removes 'name' from the column names at the end.
#     It filters out rows where 'exclude_from_output' == 1.

#     Args:
#     - csv_files (str, Path, or list of str/Path): Path(s) to CSV file(s).

#     Returns:
#     - pd.DataFrame: The resulting template DataFrame without 'name'.

#     Raises:
#     - ValueError: If 'name', 'exclude_from_output', or 'order' columns are missing.
#     """

#     # Check if input is a single string or Path, or a list of such elements
#     if isinstance(csv_files, (str, Path)):
#         csv_files = [csv_files]  # Convert to a list
#     elif not isinstance(csv_files, list) or not all(isinstance(file, (str, Path)) for file in csv_files):
#         raise ValueError("Input must be a string, Path, or a list of strings/Path objects representing file paths.")

#     # Convert Path objects to strings if necessary
#     csv_files = [str(file) if isinstance(file, Path) else file for file in csv_files]

#     # Load DataFrames from CSV files
#     dataframes = [pd.read_csv(file) for file in csv_files]

#     # Use the create_template_from_dataframes function to create the template
#     template_df = create_template_from_dataframes(dataframes)

#     return template_df

#     # Load DataFrames from CSV files
#     dataframes = [pd.read_csv(file) for file in csv_files]

#     # Use the create_template_from_dataframes function to create the template
#     template_df = create_template_from_dataframes(dataframes)

#     return template_df


# def append_stats_to_template(template_df: pd.DataFrame, df_stats: pd.DataFrame) -> pd.DataFrame:
#     """
#     Merges two DataFrames by concatenating them based on common columns, keeping all columns from template_df.

#     Args:
#         template_df (pd.DataFrame): The first DataFrame, usually a template.
#         df_stats (pd.DataFrame): The second DataFrame containing statistics.

#     Returns:
#         pd.DataFrame: DataFrame containing all columns from template_df and matching columns from df_stats.

#     Raises:
#         ValueError: If there are no common columns between the DataFrames.
#     """
#     # Get the common columns
#     common_columns = template_df.columns.intersection(df_stats.columns)

#     # Raise an error if there are no common columns
#     if common_columns.empty:
#         raise ValueError("No common columns found for merging.")

#     # Select all columns from template_df and only the matching columns from df_stats
#     df_stats_filtered = df_stats[common_columns]

#     # Create a new DataFrame to hold the merged result
#     # Fill NaN for df_stats columns that are not in template_df
#     df_merged = pd.concat([template_df, df_stats_filtered], axis=0, ignore_index=True)

#     log_missing_columns(df_stats,template_df)

#     return df_merged

# def append_stats_to_template(template_df: pd.DataFrame, df_stats: pd.DataFrame) -> pd.DataFrame:
#     """
#     Merges two DataFrames by aligning the statistics DataFrame to the template DataFrame's columns.

#     Args:
#         template_df (pd.DataFrame): The first DataFrame, usually a template.
#         df_stats (pd.DataFrame): The second DataFrame containing statistics.

#     Returns:
#         pd.DataFrame: DataFrame containing all columns from template_df, filled with data from df_stats.

#     Raises:
#         ValueError: If there are no common columns between the DataFrames.
#     """
#     # Reindex df_stats to match the columns of template_df, filling missing columns with NaN
#     df_stats_aligned = df_stats.reindex(columns=template_df.columns)

#     # Check for any missing columns in df_stats
#     if df_stats_aligned.isnull().all(axis=0).any():
#         log_missing_columns(df_stats, template_df)

#     return df_stats_aligned
#     # # Update the template_df with values from df_stats_aligned
#     # updated_template_df = template_df.combine_first(df_stats_aligned)

#     # return updated_template_df


# def log_missing_columns(df_stats: pd.DataFrame, template_df: pd.DataFrame):
#     """
#     Check for missing columns in df_stats compared to template_df and vice versa, and log the results.

#     Parameters:
#     - df_stats (pd.DataFrame): The DataFrame containing statistics.
#     - template_df (pd.DataFrame): The template DataFrame to compare against.

#     Returns:
#     - None
#     """

#     # Initialize the loggers
#     stdout_logger = StdoutLogger(__name__).logger
#     file_logger = FileLogger("missing_columns.log").logger

#     # Example column lists
#     template_columns = template_df.columns
#     df_stats_columns = df_stats.columns

#     # Find columns that are in df_stats but not in template_df
#     missing_in_template = [col for col in df_stats_columns if col not in template_columns]

#     # Find columns that are in template_df but not in df_stats
#     missing_in_stats = [col for col in template_columns if col not in df_stats_columns]

#     # Log results for missing columns in df_stats
#     if missing_in_template:
#         stdout_logger.warning(f"The following columns in 'df_stats' did not match any columns in 'template_df': {', '.join(missing_in_template)}")
#         file_logger.warning(f"The following columns in 'df_stats' did not match any columns in 'template_df': {', '.join(missing_in_template)}")
#     else:
#         stdout_logger.info("All columns from 'df_stats' found in 'template_df'.")

#     # Log results for missing columns in template_df
#     if missing_in_stats:
#         stdout_logger.warning(f"The following columns in 'template_df' did not match any columns in 'df_stats': {', '.join(missing_in_stats)}")
#         file_logger.warning(f"The following columns in 'template_df' did not match any columns in 'df_stats': {', '.join(missing_in_stats)}")
#     else:
#         stdout_logger.info("All columns from 'template_df' found in 'df_stats'.")

# def log_missing_columns(df_stats: pd.DataFrame, template_df: pd.DataFrame):
#     """
#     Check for missing columns in df_stats compared to template_df and log the results.

#     Parameters:
#     - df_stats (pd.DataFrame): The DataFrame containing statistics.
#     - template_df (pd.DataFrame): The template DataFrame to compare against.

#     Returns:
#     - None
#     """

#     # Initialize the loggers
#     stdout_logger = StdoutLogger(__name__).logger
#     file_logger = FileLogger("missing_columns.log").logger

#     # Example column lists
#     template_columns = template_df.columns
#     df_stats_columns = df_stats.columns

#     # Find columns that are in df_stats but not in template_df
#     missing_columns = [col for col in df_stats_columns if col not in template_columns]

#     # Log warning if there are unmatched columns using both loggers
#     if missing_columns:
#         stdout_logger.warning(f"The following columns in 'df_stats' did not match any columns in 'template_df': {', '.join(missing_columns)}")
#         file_logger.warning(f"The following columns in 'df_stats' did not match any columns in 'template_df': {', '.join(missing_columns)}")
#     else:
#         stdout_logger.info("All columns from 'df_stats' found in 'template_df'.")
#         file_logger.info("All columns from 'df_stats' found in 'template_df'.")

###################OLD
# def whisp_stats_ee_to_ee(feature_collection: ee.FeatureCollection) -> ee.FeatureCollection:
#     """

#     Parameters
#     ----------
#     feature_collection : ee.FeatureCollection
#         The feature collection of the ROI to analyze.

#     Returns
#     -------
#     feature_collection : ee.FeatureCollection
#         The dataframe containing the Whisp stats for the input ROI.
#     """

#     roi = feature_collection


#     # processing_lists = make_processing_lists_from_gee_datasets_lookup()
#     # (
#     #     exclude_from_output_list,
#     #     all_datasets_list,
#     #     presence_only_flag_list,
#     #     decimal_place_column_list,
#     #     column_order_list,
#     # ) = processing_lists
#     # assert_all_datasets_found_in_lookup(all_datasets_list)

#     # stats_fc_formatted = get_stats_formatted(
#     #     roi,
#     #     id_name=plot_id_column,
#     #     flag_positive=presence_only_flag_list,
#     #     exclude_properties_from_output = exclude_from_output_list,
#     # )

#     # if keep_system_index:
#     #     stats_fc_formatted = add_system_index_as_property_to_fc(stats_fc_formatted)
#     #     column_order_list.extend(
#     #         [
#     #             element
#     #             for element in ["system:index"]
#     #             if element not in column_order_list
#     #         ]
#     #     )

#     # if keep_original_properties:
#     #     original_columns = roi.first().propertyNames().getInfo()
#     #     column_order_list.extend(
#     #         [
#     #             element
#     #             for element in original_columns
#     #             if element not in column_order_list
#     #         ]
#     #     )


#     # return stats_fc_formatted
#     return get_stats(feature_collection)


# def whisp_stats_ee_to_df(feature_collection: ee.FeatureCollection) -> pd.DataFrame:
#     """

#     Parameters
#     ----------
#     feature_collection : ee.FeatureCollection
#         The filepath to the GeoJSON of the ROI to analyze.

#     Returns
#     -------
#     df_stats : pd.DataFrame
#         The dataframe containing the Whisp stats for the input ROI.
#     """

#     # roi = feature_collection
#     # # lookup_gee_datasets_csv: Path | str = DEFAULT_GEE_DATASETS_LOOKUP_TABLE_PATH
#     # # lookup_gee_datasets_df: data_lookup_type = pd.read_csv(lookup_gee_datasets_csv)
#     # lookup_gee_datasets_df= pd.read_csv(DEFAULT_GEE_DATASETS_LOOKUP_TABLE_PATH)

#     # column_order_list = order_list_from_lookup(lookup_gee_datasets_df)

#     # stats_fc_formatted = whisp_stats_ee_to_ee(roi)

#     # if keep_system_index:
#     #     stats_fc_formatted = add_system_index_as_property_to_fc(stats_fc_formatted)
#     #     column_order_list.extend(
#     #         [
#     #             element
#     #             for element in ["system:index"]
#     #             if element not in column_order_list
#     #         ]
#     #     )

#     # if keep_original_properties:
#     #     original_columns = roi.first().propertyNames().getInfo()
#     #     column_order_list.extend(
#     #         [
#     #             element
#     #             for element in original_columns
#     #             if element not in column_order_list
#     #         ]
#     #     )

#     # df_stats = geemap.ee_to_df(stats_fc_formatted).rename(
#     #     columns={"system_index": "system:index"}
#     # )
#     # df_stats = df_stats.reindex(columns=column_order_list)

#     # return df_stats
#     roi = feature_collection
#     stats_fc_formatted = whisp_stats_ee_to_ee(roi)
#     return geemap.ee_to_df(stats_fc_formatted)

# def whisp_stats_geojson_to_df(roi_filepath: Path | str) -> pd.DataFrame:
#     """

#     Parameters
#     ----------
#     roi_filepath : Path | str
#         The filepath to the GeoJSON of the ROI to analyze.

#     Returns
#     -------
#     df_stats : pd.DataFrame
#         The dataframe containing the Whisp stats for the input ROI.
#     """

#     # feature_collection = geojson_to_ee(str(roi_filepath), "r") # update this to use geojson_to_ee from agstack_to_gee.py
#     feature_collection = geojson_to_ee(str(roi_filepath)) # updated to use geojson_to_ee from agstack_to_gee.py

#     df_stats = whisp_stats_ee_to_df(feature_collection)
#     return df_stats

# import ee
# from pathlib import Path

# def whisp_stats_ee_to_drive(feature_collection: ee.FeatureCollection):

#     try:
#         task = ee.batch.Export.table.toDrive(
#             collection=whisp_stats_ee_to_ee(feature_collection),
#             description="whisp_output_table",
#             # folder="whisp_results",
#             fileFormat="CSV"
#         )
#         task.start()
#         print("Exporting to Google Drive: 'whisp_results/whisp_output_table.csv'. To track progress: https://code.earthengine.google.com/tasks")
#     except Exception as e:
#         print(f"An error occurred during the export: {e}")


# def whisp_stats_geojson_to_drive(roi_filepath: Path | str):
#     """
#     Parameters
#     ----------
#     roi_filepath : Path | str
#         The filepath to the GeoJSON of the ROI to analyze.

#     Returns
#     -------
#     Message showing location of file in Google Drive
#     """

#     try:
#         roi_filepath = Path(roi_filepath)
#         if not roi_filepath.exists():
#             raise FileNotFoundError(f"File {roi_filepath} does not exist.")

#         # Assuming geojson_to_ee is properly imported from data_conversion.py
#         feature_collection = geojson_to_ee(str(roi_filepath), "r")

#         return whisp_stats_ee_to_drive(feature_collection)

#     except Exception as e:
#         print(f"An error occurred: {e}")


# def make_processing_lists_from_gee_datasets_lookup(
#     lookup_gee_datasets_csv: Path | str = DEFAULT_GEE_DATASETS_LOOKUP_TABLE_PATH,
# ) -> (list[str], list[str], list[str], list[str], list[str]):
#     """Generates processing lists for the datasets found in the lookup table.

#     Parameters
#     ----------
#     lookup_gee_datasets_csv: Path | str, default: DEFAULT_GEE_DATASETS_LOOKUP_TABLE_PATH
#         The path to the GEE datasets lookup table.

#     Returns
#     -------
#     exclude_from_output_list : list[str]
#         The datasets to exclude from the output csv columns.
#     all_datasets_list : list[str]
#     The datasets found.
#     presence_only_flag_list : list[str]
#         The `prensence_only_flag` binary value for the datasets.
#     decimal_place_column_list : list[str]
#         The decimal place value for the datasets.
#     order_list : list[str]
#         The order value for the datasets.
#     """

#     lookup_gee_datasets_df: data_lookup_type = pd.read_csv(lookup_gee_datasets_csv)
#     exclude_from_output_list = list(
#         lookup_gee_datasets_df["name"][(lookup_gee_datasets_df["exclude_from_output"] == 1)]
#     )

#     # use the exclude list to filter lookup so all subsequent lists don't contain them
#     lookup_gee_datasets_df = lookup_gee_datasets_df[
#         (lookup_gee_datasets_df["exclude_from_output"] != 1)
#     ]
#     all_datasets_list = list(lookup_gee_datasets_df["name"])
#     presence_only_flag_list = list(
#         lookup_gee_datasets_df["name"][
#             (lookup_gee_datasets_df["presence_only_flag"] == 1)
#         ]
#     )
#     decimal_place_column_list = [
#         i for i in all_datasets_list if i not in presence_only_flag_list
#     ]
#     order_list = order_list_from_lookup(lookup_gee_datasets_df)

#     return (
#         exclude_from_output_list,
#         all_datasets_list,
#         presence_only_flag_list,
#         decimal_place_column_list,
#         order_list,
#     )


# def assert_all_datasets_found_in_lookup(all_datasets_list: list[str]) -> None:
#     """Issues a warning of not all listed datasets were found in GEE.

#     Parameters
#     ----------
#     all_datasets_list : list[str]
#         The list of datasets found in the lookup table.

#     Returns
#     -------
#     out : None
#     """

#     multiband_image_list = combine_datasets().bandNames()
#     #if in
#     in_both_lists = multiband_image_list.filter(
#         ee.Filter.inList("item", all_datasets_list)
#     )
#     not_in_multiband = multiband_image_list.filter(
#         ee.Filter.inList("item", all_datasets_list).Not()
#     )
#     not_in_lookup = ee.List(all_datasets_list).filter(
#         ee.Filter.inList("item", multiband_image_list).Not()
#     )

#     # logger.logger.info(
#     #     f"number_in_multiband_datasets_list: {multiband_image_list.length().getInfo()}"
#     # )
#     # logger.logger.info(f"number_in_both_lists: {in_both_lists.length().getInfo()}")
#     # logger.logger.info(f"not_in_multiband: {not_in_multiband.getInfo()}")

#     in_lookup = multiband_image_list.containsAll(ee.List(all_datasets_list)).getInfo()
#     logger.logger.info(f"Datasets present in lookup: {in_lookup}")
#     if not in_lookup:
#         logger.logger.warning(f"Missing from lookup: {not_in_lookup.getInfo()}")


# def add_system_index_as_property_to_feature(feature: ee.Feature) -> ee.Feature:
#     """Adds the system index to a feature.

#     Parameters
#     ----------
#     feature : ee.Feature
#         The input feature.

#     Returns
#     -------
#     enriched_feature : ee.Feature
#         The enriched feature.
#     """

#     # Get the system:index of the feature
#     system_index = feature.get("system:index")
#     # Set the 'id' property of the feature
#     enriched_feature = feature.set("system_index", system_index)
#     return enriched_feature


# def add_system_index_as_property_to_fc(
#     feature_col: ee.FeatureCollection,
# ) -> ee.FeatureCollection:
#     """Adds the system index to a feature collection as a property.

#     Parameters
#     ----------
#     feature_col : ee.FeatureCollection
#         The input collection.

#     Returns
#     -------
#     enriched_feature : ee.FeatureCollection
#         The enriched feature collection.
#     """

#     enriched_fc = feature_col.map(add_system_index_as_property_to_feature)
#     return enriched_fc
