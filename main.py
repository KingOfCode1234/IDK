import os
import importlib.util
import json

# Load the JSON file
json_file_path = "plugins/config.json"
with open(json_file_path) as json_file:
    try:
        data = json.load(json_file)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON file: {e}")
        exit(1)

directory = "plugins"

# Load each module, instantiate a class, and call a method from it
for item in data:
    module_name = item["module"]
    module_path = os.path.join(directory, module_name + ".py")
    if not os.path.exists(module_path):
        print(f"Module {module_name} not found at {module_path}")
        continue
    
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    if "class" in item:
        class_name = item["class"]
        if not hasattr(module, class_name):
            print(f"Class {class_name} not found in module {module_name}")
            continue
        
        class_ = getattr(module, class_name)
        instance = class_(**item.get("args", {}))
        if hasattr(instance, "method_name"):
            result = instance.method_name("argument1", "argument2")
        else:
            print(f"Method method_name not found in class {class_name} of module {module_name}")
            continue
    else:
        function_name = item.get("function", "function_name")
        if not hasattr(module, function_name):
            print(f"Function {function_name} not found in module {module_name}")
            continue
        
        result = getattr(module, function_name)(**item.get("args", {}))
    
    print(f"Result from {module_name}: {result}")
      
