WRAPPER = """--// Compiled by Roblox Compiler Collection TextFile Compiler \\\\--

-- Definitions
True = true;
False = false;

-- Compiled:
return """
import json as jslib
import xml.etree.ElementTree as ET

class TextEng:
    def json(code):
        data = jslib.loads(code)
        def convert(obj):
            if isinstance(obj, dict):
                return "{" + ", ".join(f"[{convert(k)}] = {convert(v)}" for k, v in obj.items()) + "}"
            elif isinstance(obj, list):
                return "{" + ", ".join(convert(item) for item in obj) + "}"
            elif isinstance(obj, str):
                return f'"{obj}"'
            else:
                return str(obj)

        lua_str = convert(data)
        lua_str = lua_str.replace("]]", "]]..\"]]\"..[[")
        return WRAPPER + lua_str
    def xml(xml_str):
        root = ET.fromstring(xml_str)

        def convert(elem):
            if len(elem) == 0:
                return f'"{elem.text}"'
            else:
                return "{" + ", ".join(f"[{convert(child.tag)}] = {convert(child)}" for child in elem) + "}"

        lua_str = convert(root)
        lua_str = lua_str.replace("]]", "]]..\"]]\"..[[")
        
        return WRAPPER + lua_str
    def txt(code):
        code = code.replace("]]", "]]..\"]]\"..[[")
        return WRAPPER + f'[[{code}]]'