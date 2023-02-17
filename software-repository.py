import re
import argparse
import os
import json
import subprocess
import time

def count_classes_and_methods(file_path, root_folder, encoding='utf-8'):
    method_string = '''@Test
    public void'''
    path = file_path.replace(root_folder,"")
    folders = os.path.split(path)[0].replace(".","")
    folders = folders[1:] if folders[0]==os.sep else folders
    folders = folders if folders[-1]==os.sep else folders+"/"
    folders = folders.replace(os.sep, ".")
    
    with open(file_path, 'r', encoding=encoding) as file:
        content = file.read()

    class_count = len(re.findall(r'public class\s+\w+', content))
    classes_names = []
    init_indices = {}
    end_indices = {}
    count = 0
    for match in re.finditer("public class ", content):
        if count == 0:
            init_indices[str(count)] = 0
        if count >= 1:
            init_indices[str(count)] = match.start()
            end_indices[str(count-1)] = match.start()
        count += 1

    end_indices[str(count-1)] = len(content)
    methods_names = []
    count = 0  
    for match in re.finditer("public class ", content):
        res = re.search(" extends", content[match.end():match.end()+50])
        class_name = content[match.end():match.end()+50].split(" ",1)[0].replace(" ","")
        classes_names.append(folders+class_name)

        init_ind = init_indices[str(count)]
        final_ind = end_indices[str(count)]
        methods_content = content[init_ind:final_ind]
        
        for match in re.finditer(method_string, methods_content):
            res = re.search("\(\)", methods_content[match.end():match.end()+100])
            method_name = methods_content[match.end():match.end()+100][0:res.start()].replace(" ","")
            methods_names.append(f"{folders}{class_name}:{method_name}")
        count += 1
    
    method_count = len(re.findall(method_string, content))
    return class_count, method_count, classes_names, methods_names


def process_git_repo(directory, root_folder):
    
    java_files = [f for f in os.listdir(directory) if f.endswith('.java')]

    result = subprocess.run(["git", "log","--pretty=format:\"%H\""], cwd=directory, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    commits = result.stdout.strip().split("\n")
    start_time = time.time()

    test_of_commits = []

    for commit in commits:
        files_found = []
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file.endswith(".java") and "Test" in file:
                     files_found.append(os.path.join(root, file))


        num_of_test_classes = 0
        num_of_test_methods = 0
        class_list = []
        method_list = []
        
        for file_path in files_found:
            if file_path.endswith('.java') and os.path.exists(file_path):
                full_file_path = file_path
                class_count, method_count, class_listi, method_listi = count_classes_and_methods(full_file_path, root_folder)
                num_of_test_classes += class_count
                num_of_test_methods += method_count
                class_list.extend(class_listi)
                method_list.extend(method_listi)
                #print(f"after num_of_test_classes={num_of_test_classes}, number of test methods: {num_of_test_methods}")

        test_of_commit = {
            "commit": commit,
            "num_of_test_classes": num_of_test_classes,
            "num_of_test_methods": num_of_test_methods,
            "list_of_test_classes": class_list,
            "list_of_test_methods": method_list,
        }
        test_of_commits.append(test_of_commit)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"elapsed time: {elapsed_time}, per commit {elapsed_time*10} ms")

    data = {
        "location": directory,
        "number_of_commits": len(commits),
        "test_of_commits": test_of_commits,
        "time_taken_per_commit": elapsed_time / len(commits)
    }

    with open("output.json", 'w') as f:
        json.dump(data, f, indent=4)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Count the number of classes and methods in Java files in a directory')
    parser.add_argument('--directory', type=str,
                        help='the directory containing the Java files')
    parser.add_argument('--root_folder', type=str, help='root', default = "./")
    
    args = parser.parse_args()
    folder = args.directory
    root_folder = args.root_folder
    if root_folder == './':
        root_folder = folder
    #folder = "./commons-lang/src/test"
    #root_folder = folder
    process_git_repo(folder, root_folder)
