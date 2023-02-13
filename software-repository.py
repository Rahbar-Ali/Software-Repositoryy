import re
import argparse
import os
import json
import subprocess


def count_classes_and_methods(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"ERROR: Could not open file {file_path}")
        return (0, 0, [], [])
    except Exception as e:
        print(f"ERROR: Exception occurred while reading file {file_path}: {e}")
        return (0, 0, [], [])

    class_count = len(re.findall(r'class\s+\w+', content))
    method_count = len(re.findall(r'@Test\s+\w+', content))
    class_list = re.findall(r'class\s+(\w+)', content)
    method_list = re.findall(r'@Test\s+(\w+)', content)

    #print(f"{file_path}: number of classes: {class_count}, number of methods: {method_count}")
    return (class_count, method_count, class_list, method_list)


def process_git_repo(directory):

    java_files = [f for f in os.listdir(directory) if f.endswith('.java')]

    result = subprocess.run(["git", "log", "--pretty=format:\"%H\""], cwd=directory,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    commits = result.stdout.strip().split("\n")
    data = {
        "location": directory,
        "number_of_commits": len(commits),
        "tests_of_commits": [],
    }

    for commit in commits:
        # subprocess.run(["git", "checkout", commit], check=True)
        files_found = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".java") and "Test" in file:
                    files_found.append(os.path.join(root, file))

        for file_path in files_found:
            if file_path.endswith('.java') and os.path.exists(file_path):
                full_file_path = file_path
                class_count, method_count, class_list, method_list = count_classes_and_methods(
                    full_file_path)
            data["tests_of_commits"].append({
                "commit": commit,
                "num_of_test_classes": class_count,
                "num_of_test_methods": method_count,
                "list_of_test_classes": class_list,
                "list_of_test_methods": method_list
            })

    with open("output.json", 'w') as f:
        json.dump(data, f, indent=4)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Count the number of classes and methods in Java files in a directory')
    parser.add_argument('directory', type=str,
                        help='the directory containing the Java files')
    args = parser.parse_args()
    process_git_repo(args.directory)
