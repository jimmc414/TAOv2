# Advanced Guide: Adding a Complex Custom Task to TAO Agent v2.0

This guide provides a detailed, step-by-step process for adding a new complex custom task to the TAO Agent v2.0 project. We'll create a multi-step data processing task that demonstrates various features and capabilities of the system.

## 1. Task Overview

Our new custom task, called "DataProcessingTask", will perform the following steps:

1. Check for a new CSV file in a specified input directory.
2. If a new file is found, load it using pandas.
3. Perform data manipulation (we'll demonstrate several operations).
4. Generate three output files in different formats (CSV, JSON, and Excel).
5. Copy these files to different output directories.

This task will demonstrate error handling, logging, progress reporting, and use of the variable manager.

## 2. Creating the Plugin

First, let's create a new plugin file:

1. Navigate to the `plugins` directory in your TAO Agent v2.0 project.
2. Create a new Python file named `data_processing_plugin.py`.
3. Open the file and add the following initial structure:

```python
import os
import pandas as pd
from datetime import datetime
from typing import Dict, Any, List
from tao.base_plugin import BasePlugin
from tao.variable_manager import VariableManager

class DataProcessingPlugin(BasePlugin):
    def __init__(self):
        super().__init__()
        self.name = "data_processing_plugin"
        self.variable_manager = None

    def initialize(self) -> None:
        self.logger.info("Initializing DataProcessingPlugin")
        # Any initialization code can go here

    def cleanup(self) -> None:
        self.logger.info("Cleaning up DataProcessingPlugin")
        # Any cleanup code can go here

    def set_variable_manager(self, variable_manager: VariableManager):
        self.variable_manager = variable_manager

    def validate_config(self, config: Dict[str, Any]) -> bool:
        required_keys = ['input_directory', 'output_directory_csv', 'output_directory_json', 'output_directory_excel']
        return all(key in config for key in required_keys)

    def get_available_tasks(self) -> List[str]:
        return ["process_data"]

    def execute_task(self, task_name: str, parameters: Dict[str, Any], variables: Dict[str, Any]) -> Any:
        if task_name == "process_data":
            return self._process_data(parameters)
        else:
            raise ValueError(f"Unknown task: {task_name}")

    def _process_data(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        # This method will be implemented in the next section
        pass
```

## 3. Implementing the Custom Task

Now, let's implement the `_process_data` method with all the required steps:

```python
import shutil
from pathlib import Path

def _process_data(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
    input_dir = Path(parameters['input_directory'])
    output_dir_csv = Path(parameters['output_directory_csv'])
    output_dir_json = Path(parameters['output_directory_json'])
    output_dir_excel = Path(parameters['output_directory_excel'])

    # Step 1: Check for new CSV file
    csv_file = self._check_for_new_csv(input_dir)
    if not csv_file:
        return {"status": "No new file found"}

    # Step 2: Retrieve and load CSV file
    df = self._load_csv(csv_file)

    # Step 3: Process data with pandas
    df_processed = self._process_dataframe(df)

    # Step 4: Generate output files
    output_files = self._generate_output_files(df_processed, output_dir_csv, output_dir_json, output_dir_excel)

    # Step 5: Copy files to destination directories
    self._copy_files_to_destinations(output_files)

    return {"status": "success", "processed_file": csv_file.name, "output_files": output_files}
```

Now, let's implement each step in detail:

### Step 1: Check for New CSV File

```python
def _check_for_new_csv(self, input_dir: Path) -> Path:
    self.logger.info(f"Checking for new CSV files in {input_dir}")
    csv_files = list(input_dir.glob('*.csv'))
    if not csv_files:
        self.logger.info("No CSV files found")
        return None
    
    # Get the most recent file
    latest_file = max(csv_files, key=lambda f: f.stat().st_mtime)
    
    # Check if this file has been processed before
    last_processed_file = self.variable_manager.get_variable('last_processed_file', '')
    if latest_file.name == last_processed_file:
        self.logger.info(f"No new files to process. Last processed file: {last_processed_file}")
        return None
    
    self.logger.info(f"New file found: {latest_file.name}")
    return latest_file
```

### Step 2: Retrieve and Load CSV File

```python
def _load_csv(self, file_path: Path) -> pd.DataFrame:
    self.logger.info(f"Loading CSV file: {file_path}")
    try:
        df = pd.read_csv(file_path)
        self.logger.info(f"Successfully loaded CSV with {len(df)} rows and {len(df.columns)} columns")
        return df
    except Exception as e:
        self.logger.error(f"Error loading CSV file: {str(e)}")
        raise
```

### Step 3: Process Data with Pandas

```python
def _process_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
    self.logger.info("Processing dataframe")
    
    # Example processing steps
    # 1. Remove any rows with missing values
    df = df.dropna()
    
    # 2. Convert date column to datetime
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    
    # 3. Create a new column 'year' from the 'date' column
    if 'date' in df.columns:
        df['year'] = df['date'].dt.year
    
    # 4. Group by 'year' and calculate mean for numeric columns
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    df_summary = df.groupby('year')[numeric_columns].mean().reset_index()
    
    self.logger.info(f"Processed dataframe. New shape: {df_summary.shape}")
    return df_summary
```

### Step 4: Generate Output Files

```python
def _generate_output_files(self, df: pd.DataFrame, output_dir_csv: Path, output_dir_json: Path, output_dir_excel: Path) -> Dict[str, Path]:
    self.logger.info("Generating output files")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    output_files = {}
    
    # Generate CSV
    csv_path = output_dir_csv / f"processed_data_{timestamp}.csv"
    df.to_csv(csv_path, index=False)
    output_files['csv'] = csv_path
    
    # Generate JSON
    json_path = output_dir_json / f"processed_data_{timestamp}.json"
    df.to_json(json_path, orient='records')
    output_files['json'] = json_path
    
    # Generate Excel
    excel_path = output_dir_excel / f"processed_data_{timestamp}.xlsx"
    df.to_excel(excel_path, index=False)
    output_files['excel'] = excel_path
    
    self.logger.info(f"Generated output files: {', '.join(str(path) for path in output_files.values())}")
    return output_files
```

### Step 5: Copy Files to Destination Directories

```python
def _copy_files_to_destinations(self, output_files: Dict[str, Path]) -> None:
    self.logger.info("Copying files to destination directories")
    for file_type, file_path in output_files.items():
        dest_dir = self.variable_manager.get_variable(f'destination_directory_{file_type}')
        if dest_dir:
            dest_path = Path(dest_dir) / file_path.name
            shutil.copy2(file_path, dest_path)
            self.logger.info(f"Copied {file_type} file to {dest_path}")
        else:
            self.logger.warning(f"No destination directory specified for {file_type} files")
```

## 4. Configuring the New Task

Update your configuration file (e.g., `config/config.yaml`) to include the new plugin and its configuration:

```yaml
plugins:
  - name: "data_processing_plugin"
    module: "plugins.data_processing_plugin"
    description: "Plugin for processing CSV data"

workflow_engine:
  data_processing_plugin:
    enabled: true
    input_directory: "/path/to/input/directory"
    output_directory_csv: "/path/to/output/csv"
    output_directory_json: "/path/to/output/json"
    output_directory_excel: "/path/to/output/excel"
    destination_directory_csv: "/path/to/final/csv"
    destination_directory_json: "/path/to/final/json"
    destination_directory_excel: "/path/to/final/excel"
```

## 5. Using the New Task in a Workflow

Now you can use the new task in your workflow configuration:

```yaml
workflow:
  name: "Data Processing Workflow"
  tasks:
    - name: process_csv_data
      description: "Process new CSV data"
      plugin: data_processing_plugin
      function: process_data
      parameters:
        input_directory: ${input_directory}
        output_directory_csv: ${output_directory_csv}
        output_directory_json: ${output_directory_json}
        output_directory_excel: ${output_directory_excel}
      on_success:
        next: check_processing_result
      on_failure:
        action: notify_admin

    - name: check_processing_result
      description: "Check the result of data processing"
      plugin: core_plugin
      function: conditional_execution
      parameters:
        condition: "{{ tasks.process_csv_data.output.status == 'success' }}"
      on_success:
        true_branch: update_last_processed_file
        false_branch: log_no_new_files

    - name: update_last_processed_file
      description: "Update the last processed file variable"
      plugin: core_plugin
      function: set_variable
      parameters:
        variable_name: last_processed_file
        value: "{{ tasks.process_csv_data.output.processed_file }}"

    - name: log_no_new_files
      description: "Log when no new files are found"
      plugin: core_plugin
      function: log_message
      parameters:
        message: "No new files to process"
        level: INFO
```

## 6. Error Handling and Logging

Error handling and logging have been implemented throughout the custom task. Here's a summary of the approach:

1. Use `self.logger` for logging at different levels (info, warning, error).
2. Wrap critical operations in try-except blocks to catch and log specific exceptions.
3. Raise exceptions when encountering critical errors that should halt the task execution.
4. Use the variable manager to store and retrieve state information (e.g., last processed file).

## 7. Testing the Custom Task

Create a unit test file `tests/test_data_processing_plugin.py`:

```python
import unittest
from unittest.mock import Mock, patch
from pathlib import Path
import pandas as pd
from plugins.data_processing_plugin import DataProcessingPlugin

class TestDataProcessingPlugin(unittest.TestCase):
    def setUp(self):
        self.plugin = DataProcessingPlugin()
        self.plugin.logger = Mock()
        self.plugin.variable_manager = Mock()

    @patch('plugins.data_processing_plugin.pd.read_csv')
    def test_load_csv(self, mock_read_csv):
        mock_df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        mock_read_csv.return_value = mock_df
        
        result = self.plugin._load_csv(Path('test.csv'))
        
        self.assertTrue(isinstance(result, pd.DataFrame))
        self.assertEqual(len(result), 3)
        self.assertEqual(len(result.columns), 2)

    def test_process_dataframe(self):
        input_df = pd.DataFrame({
            'date': ['2021-01-01', '2021-02-01', '2022-01-01'],
            'value': [10, 20, 30]
        })
        
        result = self.plugin._process_dataframe(input_df)
        
        self.assertEqual(len(result), 2)  # Two years: 2021 and 2022
        self.assertIn('year', result.columns)
        self.assertIn('value', result.columns)

    # Add more tests for other methods...

if __name__ == '__main__':
    unittest.main()
```

## 8. Advanced Scenarios and Best Practices

1. **Handling Large Files**: 
   - Use `pd.read_csv()` with `chunksize` parameter for processing large files in chunks.
   - Implement a generator function to yield processed chunks.

2. **Parallel Processing**:
   - Use `multiprocessing` or `concurrent.futures` for parallel file processing when dealing with multiple input files.

3. **Customizable Data Processing**:
   - Allow users to specify custom processing steps in the configuration.
   - Implement a simple DSL (Domain Specific Language) for defining data transformations.

4. **Incremental Processing**:
   - Implement a mechanism to track which parts of a file have been processed.
   - Use database or file-based checkpointing to resume processing from where it left off.

5. **Data Validation**:
   - Implement data validation checks before processing.
   - Use libraries like `great_expectations` for more advanced data validation.

6. **Secure File Handling**:
   - Implement file integrity checks (e.g., MD5 hashing) to ensure files haven't been tampered with.