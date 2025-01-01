# testsuiteextension.py

import os
import time
import psutil
import pandas as pd
from statistics import mean
from tabulate import tabulate
from grid import Grid
from fileRead import FileRead
from testgenerator import TestGenerator

class TestSuiteExtension:
    def __init__(self):
        self.test_cases_dir = 'test_cases'
        self.results = {}
        self.summary = {}
        self.generator = TestGenerator()
        # Import search methods during initialization to avoid circular import
        from searchstrat import (BreadthFirstSearch, DepthFirstSearch, 
                                AStarSearch, GreedyBestFirstSearch, 
                                BidirectionalSearch, BeamSearch)
        
        self.search_methods = {
            'bfs': (BreadthFirstSearch, 'bfsPath', 'Breadth-First Search'),
            'dfs': (DepthFirstSearch, 'dfsPath', 'Depth-First Search'),
            'astar': (AStarSearch, 'astarPath', 'A* Search'),
            'gbfs': (GreedyBestFirstSearch, 'gbfsPath', 'Greedy Best-First Search'),
            'bds': (BidirectionalSearch, 'bdsPath', 'Bidirectional Search'),
            'bs': (BeamSearch, 'beamPath', 'Beam Search')
        }
        
    def runTestSuite(self):
        # Execute the complete test suite
        print("\n" + "="*50)
        print("Starting Search Algorithm Test Suite")
        print("="*50)

        try:
            # Phase 1: Generate Tests
            print("\nPhase 1: Generating Test Cases")
            print("-"*30)
            self.generateTests()

            # Phase 2: Run Tests
            print("\nPhase 2: Running Tests")
            print("-"*30)
            self.runTests()

            # Phase 3: Generate Report
            print("\nPhase 3: Generating Report")
            print("-"*30)
            self.generateReport()

        except Exception as e:
            print(f"\nError in test suite execution: {str(e)}")
            return False

        print("\n" + "="*50)
        print("Test Suite Execution Complete")
        print("="*50)
        return True

    def generateTests(self):
        # Generate all test cases
        print("Generating test cases...")
        self.generator.generateAllTests()  # Using the new combined test generation method
        print("Test cases generated successfully.")

    def runTests(self):
        # Run all tests for each search method
        # Initialize results
        for method in self.search_methods.keys():
            self.results[method] = []
            self.summary[method] = {
                'total_tests': 0,
                'passed': 0,
                'failed': 0,
                'avg_time': 0,
                'avg_nodes': 0,
                'avg_path_length': 0,
                'avg_memory': 0,
                'failed_tests': []
            }

        # Get test files
        test_files = sorted([f for f in os.listdir(self.test_cases_dir) 
                            if f.startswith('test') and f.endswith('.txt')],
                            key=lambda x: int(x.replace('test', '').replace('.txt', '')))

        # Run tests
        total_tests = len(test_files) * len(self.search_methods)
        completed_tests = 0

        for test_file in test_files:
            test_number = test_file.replace('test', '').replace('.txt', '')
            print(f"\nRunning Test {test_number}...")
            
            for method in self.search_methods.keys():
                # Update progress
                completed_tests += 1
                progress = (completed_tests / total_tests) * 100
                print(f"Progress: {progress:.1f}% - Running {method.upper()} on Test {test_number}")
                
                result = self.runSingleTest(test_file, method)
                self.results[method].append(result)
                self.updateSummary(method, result)

    def runSingleTest(self, test_file, method):
        # Run a single test and return results
        result = {
            'test_name': test_file,
            'method': method,
            'status': 'PASSED',
            'error': None,
            'time_ms': 0,
            'nodes_explored': 0,
            'path_length': 0,
            'memory_mb': 0
        }

        try:
            # Get initial memory usage
            process = psutil.Process(os.getpid())
            memory_start = process.memory_info().rss / 1024  # Convert to KB
            
            # Capture start time
            start_time = time.perf_counter()
            
            # Read and parse test file
            lines = FileRead.readFile(os.path.join(self.test_cases_dir, test_file))
            config = FileRead.parseGridInfo(lines)
            
            # Create grid and run search
            grid = Grid(config['dimensions'], config['start'], config['goals'], config['walls'])
            search_class = self.search_methods[method][0]
            search_method = self.search_methods[method][1]
            
            # Initialize search (special case for beam search)
            if method == 'bs':
                search = search_class(grid, beam_width=2)
            else:
                search = search_class(grid)
            
            # Execute search
            found, path = getattr(search, search_method)()
            
            # Record results
            result['time_ms'] = (time.perf_counter() - start_time) * 1000
            result['nodes_explored'] = search.nodes_explored
            result['path_length'] = len(path) if found else 0
            
            # Calculate memory usage
            memory_end = process.memory_info().rss / 1024  # Convert to KB
            result['memory_mb'] = memory_end - memory_start

            if not found and any(goal in search.goals for goal in config['goals']):
                result['status'] = 'FAILED'
                result['error'] = 'No path found to valid goal'

        except Exception as e:
            result['status'] = 'FAILED'
            result['error'] = str(e)

        return result

    def updateSummary(self, method, result):
        # Update summary statistics for a method
        self.summary[method]['total_tests'] += 1
        
        if result['status'] == 'PASSED':
            self.summary[method]['passed'] += 1
        else:
            self.summary[method]['failed'] += 1
            self.summary[method]['failed_tests'].append(result['test_name'])

        # Update averages only if there are results
        results_for_method = [r for r in self.results[method] if r['time_ms'] > 0]
        if results_for_method:
            self.summary[method]['avg_time'] = mean(r['time_ms'] for r in results_for_method)
            self.summary[method]['avg_nodes'] = mean(r['nodes_explored'] for r in results_for_method)
            self.summary[method]['avg_memory'] = mean(r['memory_mb'] for r in results_for_method)
            path_lengths = [r['path_length'] for r in results_for_method if r['path_length'] > 0]
            if path_lengths:
                self.summary[method]['avg_path_length'] = mean(path_lengths)

    def generateReport(self):
        # Generate and print the test report
        print("\n" + "="*80)
        print("SEARCH ALGORITHM TEST REPORT")
        print("="*80)

        # Summary table data
        summary_data = []
        headers = ['Method', 'Total Tests', 'Passed', 'Failed', 'Avg Time (ms)', 
                    'Avg Nodes', 'Avg Path Length', 'Avg Memory (KB)']

        for method in self.search_methods.keys():
            summary = self.summary[method]
            summary_data.append([
                self.search_methods[method][2],  # Full method name
                summary['total_tests'],
                summary['passed'],
                summary['failed'],
                f"{summary['avg_time']:.2f}",
                f"{summary['avg_nodes']:.1f}",
                f"{summary['avg_path_length']:.1f}",
                f"{summary['avg_memory']:.2f}"
            ])

        # Print summary
        print("\nOverall Summary:")
        print(tabulate(summary_data, headers=headers, tablefmt='grid'))

        # Performance comparison data
        performance_data = []
        perf_headers = ['Method', 'Min Time (ms)', 'Max Time (ms)', 
                        'Min Nodes', 'Max Nodes', 'Min Memory (KB)', 'Max Memory (KB)']

        for method in self.search_methods.keys():
            results = [r for r in self.results[method] if r['time_ms'] > 0]
            if results:
                max_time = max(r['time_ms'] for r in results)
                min_time = min(r['time_ms'] for r in results)
                max_nodes = max(r['nodes_explored'] for r in results)
                min_nodes = min(r['nodes_explored'] for r in results)
                max_memory = max(r['memory_mb'] for r in results)
                min_memory = min(r['memory_mb'] for r in results)
                
                performance_data.append([
                    self.search_methods[method][2],
                    f"{min_time:.2f}",
                    f"{max_time:.2f}",
                    min_nodes,
                    max_nodes,
                    f"{min_memory:.2f}",
                    f"{max_memory:.2f}"
                ])

        # Print performance comparison
        print("\nPerformance Comparison:")
        print(tabulate(performance_data, headers=perf_headers, tablefmt='grid'))

        # Export tables to Excel
        self.exportToExcel(summary_data, performance_data, headers, perf_headers)

        # Print failures
        print("\nDetailed Failure Report:")
        print("-"*80)
        
        failures_found = False
        for method in self.search_methods.keys():
            failed_tests = self.summary[method]['failed_tests']
            if failed_tests:
                failures_found = True
                print(f"\n{self.search_methods[method][2]} failures:")
                for test in failed_tests:
                    failed_result = next(r for r in self.results[method] 
                                        if r['test_name'] == test)
                    print(f"  - Test {test}: {failed_result['error']}")

        if not failures_found:
            print("No failures reported for solved mazes!")
            print("Note: Tests 13-14 may be intentionally unsolvable for extreme difficulty.")

    def exportToExcel(self, summary_data, performance_data, summary_headers, perf_headers):
        # Export the results tables to an Excel file
        # Create Excel writer object
        excel_file = 'SearchResultsPerformance.xlsx'
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            # Convert summary data to DataFrame and write to Excel
            summary_df = pd.DataFrame(summary_data, columns=summary_headers)
            summary_df.to_excel(writer, sheet_name='Summary', index=False)

            # Convert performance data to DataFrame and write to Excel
            performance_df = pd.DataFrame(performance_data, columns=perf_headers)
            performance_df.to_excel(writer, sheet_name='Performance', index=False)

            # Auto-adjust columns width
            for sheet_name in writer.sheets:
                worksheet = writer.sheets[sheet_name]
                for idx, col in enumerate(worksheet.columns, 1):
                    max_length = 0
                    column = worksheet.column_dimensions[chr(64 + idx)]
                    
                    for cell in col:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = (max_length + 2)
                    column.width = adjusted_width

        print(f"\nResults exported to {excel_file}")