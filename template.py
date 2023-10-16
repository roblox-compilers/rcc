import os
import json

def dir_to_json(path):
    data = {}
    for root, dirs, files in os.walk(path):
        for file in files:
            data[os.path.join(root, file)] = open(os.path.join(root, file), "r").read()
    return (json.dumps(data))

def json_to_dir(injson):
    injson = json.loads(injson)
    # make folder `template`
    if os.path.exists("template"):
        os.system("rm -rf template")
    os.mkdir("template")
    
    
    for file in injson:
        # check if the folder it is in exists
        if not os.path.exists(os.path.dirname(file)):
            os.makedirs(os.path.dirname(file))
            
        open(file, "w").write(injson[file])

LIB = """-- Roblox Compiler Collection Library

local RCC = {}

function RCC.import(name)
    local Packages = game.ReplicatedStorage.Packages:GetChildren()
    for i, v in Packages do
        local author, packagename = v.Name:match("(.+)%.(.+)")
        if name == packagename then
            return require((v.src or v.lib or error(("[RCC] %s does not have a src or lib folder"):format(v.Name))).init)
        end
    end
end

return RCC"""
PYTHON = r"""{"template/default.project.json": "{\n  \"name\": \"rcc-template\",\n  \"tree\": {\n    \"$className\": \"DataModel\",\n\n    \"ReplicatedStorage\": {\n      \"Shared\": {\n        \"$path\": \"out/shared\"\n      }\n    },\n\n    \"ServerScriptService\": {\n      \"Server\": {\n        \"$path\": \"out/server\",\n        \"Packages\": {\n          \"$path\": \"include\"\n        }\n      }\n    },\n\n    \"StarterPlayer\": {\n      \"StarterPlayerScripts\": {\n        \"Client\": {\n          \"$path\": \"out/client\"\n        }\n      }\n    },\n\n    \"Workspace\": {\n      \"$properties\": {\n        \"FilteringEnabled\": true\n      },\n      \"Baseplate\": {\n        \"$className\": \"Part\",\n        \"$properties\": {\n          \"Anchored\": true,\n          \"Color\": [\n            0.38823,\n            0.37254,\n            0.38823\n          ],\n          \"Locked\": true,\n          \"Position\": [\n            0,\n            -10,\n            0\n          ],\n          \"Size\": [\n            512,\n            20,\n            512\n          ]\n        }\n      }\n    },\n    \"Lighting\": {\n      \"$properties\": {\n        \"Ambient\": [\n          0,\n          0,\n          0\n        ],\n        \"Brightness\": 2,\n        \"GlobalShadows\": true,\n        \"Outlines\": false,\n        \"Technology\": \"Voxel\"\n      }\n    },\n    \"SoundService\": {\n      \"$properties\": {\n        \"RespectFilteringEnabled\": true\n      }\n    }\n  }\n}", "template/.gitignore": "# Project place file\n/game.rbxlx\n\n# Roblox Studio lock files\n/*.rbxlx.lock\n/*.rbxl.lock\n\n# RCC files\n/out\n", "template/include/rcclib.lua": " """+LIB+r""" ", "template/src/server/init.server.py": "print(\"Hello world, from server!\")", "template/src/shared/Hello.py": "global returnVal\ndef returnVal():\n\tprint(\"Hello, world!\")\n", "template/src/client/init.client.py": "print(\"Hello world, from client!\")"}"""
CPP = r"""{"template/default.project.json": "{\n  \"name\": \"rcc-template\",\n  \"tree\": {\n    \"$className\": \"DataModel\",\n\n    \"ReplicatedStorage\": {\n      \"Shared\": {\n        \"$path\": \"out/shared\"\n      }\n    },\n\n    \"ServerScriptService\": {\n      \"Server\": {\n        \"$path\": \"out/server\",\n        \"Packages\": {\n          \"$path\": \"include\"\n        }\n      }\n    },\n\n    \"StarterPlayer\": {\n      \"StarterPlayerScripts\": {\n        \"Client\": {\n          \"$path\": \"out/client\"\n        }\n      }\n    },\n\n    \"Workspace\": {\n      \"$properties\": {\n        \"FilteringEnabled\": true\n      },\n      \"Baseplate\": {\n        \"$className\": \"Part\",\n        \"$properties\": {\n          \"Anchored\": true,\n          \"Color\": [\n            0.38823,\n            0.37254,\n            0.38823\n          ],\n          \"Locked\": true,\n          \"Position\": [\n            0,\n            -10,\n            0\n          ],\n          \"Size\": [\n            512,\n            20,\n            512\n          ]\n        }\n      }\n    },\n    \"Lighting\": {\n      \"$properties\": {\n        \"Ambient\": [\n          0,\n          0,\n          0\n        ],\n        \"Brightness\": 2,\n        \"GlobalShadows\": true,\n        \"Outlines\": false,\n        \"Technology\": \"Voxel\"\n      }\n    },\n    \"SoundService\": {\n      \"$properties\": {\n        \"RespectFilteringEnabled\": true\n      }\n    }\n  }\n}", "template/.gitignore": "# Project place file\n/game.rbxlx\n\n# Roblox Studio lock files\n/*.rbxlx.lock\n/*.rbxl.lock\n\n# RCC files\n/out\n", "template/include/rcclib.lua": " """+LIB+r""" ", "template/src/server/init.server.cpp": "#include <rbx.h>\n\nvoid main(){\n    print(\"Hello world, from server!\")\n}", "template/src/shared/Hello.cpp": "#include <rbx.h>\n\nextern int Hello()\n{\n    printf(\"Hello World!\");\n    return 1;\n}", "template/src/client/init.client.cpp": "#include <rbx.h>\n\nvoid main(){\n    print(\"Hello world, from client!\")\n}"}"""
C = r"""{"template/default.project.json": "{\n  \"name\": \"rcc-template\",\n  \"tree\": {\n    \"$className\": \"DataModel\",\n\n    \"ReplicatedStorage\": {\n      \"Shared\": {\n        \"$path\": \"out/shared\"\n      }\n    },\n\n    \"ServerScriptService\": {\n      \"Server\": {\n        \"$path\": \"out/server\",\n        \"Packages\": {\n          \"$path\": \"include\"\n        }\n      }\n    },\n\n    \"StarterPlayer\": {\n      \"StarterPlayerScripts\": {\n        \"Client\": {\n          \"$path\": \"out/client\"\n        }\n      }\n    },\n\n    \"Workspace\": {\n      \"$properties\": {\n        \"FilteringEnabled\": true\n      },\n      \"Baseplate\": {\n        \"$className\": \"Part\",\n        \"$properties\": {\n          \"Anchored\": true,\n          \"Color\": [\n            0.38823,\n            0.37254,\n            0.38823\n          ],\n          \"Locked\": true,\n          \"Position\": [\n            0,\n            -10,\n            0\n          ],\n          \"Size\": [\n            512,\n            20,\n            512\n          ]\n        }\n      }\n    },\n    \"Lighting\": {\n      \"$properties\": {\n        \"Ambient\": [\n          0,\n          0,\n          0\n        ],\n        \"Brightness\": 2,\n        \"GlobalShadows\": true,\n        \"Outlines\": false,\n        \"Technology\": \"Voxel\"\n      }\n    },\n    \"SoundService\": {\n      \"$properties\": {\n        \"RespectFilteringEnabled\": true\n      }\n    }\n  }\n}", "template/.gitignore": "# Project place file\n/game.rbxlx\n\n# Roblox Studio lock files\n/*.rbxlx.lock\n/*.rbxl.lock\n\n# RCC files\n/out\n", "template/include/rcclib.lua": " """+LIB+r""" ", "template/src/server/init.server.c": "#include <rbx.h>\n\nvoid main(){\n    print(\"Hello world, from server!\")\n}", "template/src/shared/Hello.c": "#include <rbx.h>\n\nextern int Hello()\n{\n    printf(\"Hello World!\");\n    return 1;\n}", "template/src/client/init.client.c": "#include <rbx.h>\n\nvoid main(){\n    print(\"Hello world, from client!\")\n}"}"""
CS = r"""{"template/default.project.json": "{\n  \"name\": \"rcc-template\",\n  \"tree\": {\n    \"$className\": \"DataModel\",\n\n    \"ReplicatedStorage\": {\n      \"Shared\": {\n        \"$path\": \"out/shared\"\n      }\n    },\n\n    \"ServerScriptService\": {\n      \"Server\": {\n        \"$path\": \"out/server\",\n        \"Packages\": {\n          \"$path\": \"include\"\n        }\n      }\n    },\n\n    \"StarterPlayer\": {\n      \"StarterPlayerScripts\": {\n        \"Client\": {\n          \"$path\": \"out/client\"\n        }\n      }\n    },\n\n    \"Workspace\": {\n      \"$properties\": {\n        \"FilteringEnabled\": true\n      },\n      \"Baseplate\": {\n        \"$className\": \"Part\",\n        \"$properties\": {\n          \"Anchored\": true,\n          \"Color\": [\n            0.38823,\n            0.37254,\n            0.38823\n          ],\n          \"Locked\": true,\n          \"Position\": [\n            0,\n            -10,\n            0\n          ],\n          \"Size\": [\n            512,\n            20,\n            512\n          ]\n        }\n      }\n    },\n    \"Lighting\": {\n      \"$properties\": {\n        \"Ambient\": [\n          0,\n          0,\n          0\n        ],\n        \"Brightness\": 2,\n        \"GlobalShadows\": true,\n        \"Outlines\": false,\n        \"Technology\": \"Voxel\"\n      }\n    },\n    \"SoundService\": {\n      \"$properties\": {\n        \"RespectFilteringEnabled\": true\n      }\n    }\n  }\n}", "template/.gitignore": "# Project place file\n/game.rbxlx\n\n# Roblox Studio lock files\n/*.rbxlx.lock\n/*.rbxl.lock\n\n# RCC files\n/out\n", "template/include/rcclib.lua": " """+LIB+r""" ", "template/src/server/init.server.cs": "using System;\n\nclass Client\n{\n    static void Main(string[] args)\n    {\n        Console.WriteLine(\"Hello world, from server!\");\n    }\n}", "template/src/shared/Hello.cs": "using System;\n\nclass Hello {\n\tstatic void Hello(){\n\t\tConsole.WriteLine(\"Hello world, from shared!\");\n\t}\n}", "template/src/client/init.client.cs": "using System;\n\nclass Client\n{\n    static void Main(string[] args)\n    {\n        Console.WriteLine(\"Hello world, from client!\");\n    }\n}"}"""
KT = r"""{"template/default.project.json": "{\n  \"name\": \"rcc-template\",\n  \"tree\": {\n    \"$className\": \"DataModel\",\n\n    \"ReplicatedStorage\": {\n      \"Shared\": {\n        \"$path\": \"out/shared\"\n      }\n    },\n\n    \"ServerScriptService\": {\n      \"Server\": {\n        \"$path\": \"out/server\",\n        \"Packages\": {\n          \"$path\": \"include\"\n        }\n      }\n    },\n\n    \"StarterPlayer\": {\n      \"StarterPlayerScripts\": {\n        \"Client\": {\n          \"$path\": \"out/client\"\n        }\n      }\n    },\n\n    \"Workspace\": {\n      \"$properties\": {\n        \"FilteringEnabled\": true\n      },\n      \"Baseplate\": {\n        \"$className\": \"Part\",\n        \"$properties\": {\n          \"Anchored\": true,\n          \"Color\": [\n            0.38823,\n            0.37254,\n            0.38823\n          ],\n          \"Locked\": true,\n          \"Position\": [\n            0,\n            -10,\n            0\n          ],\n          \"Size\": [\n            512,\n            20,\n            512\n          ]\n        }\n      }\n    },\n    \"Lighting\": {\n      \"$properties\": {\n        \"Ambient\": [\n          0,\n          0,\n          0\n        ],\n        \"Brightness\": 2,\n        \"GlobalShadows\": true,\n        \"Outlines\": false,\n        \"Technology\": \"Voxel\"\n      }\n    },\n    \"SoundService\": {\n      \"$properties\": {\n        \"RespectFilteringEnabled\": true\n      }\n    }\n  }\n}", "template/.gitignore": "# Project place file\n/game.rbxlx\n\n# Roblox Studio lock files\n/*.rbxlx.lock\n/*.rbxl.lock\n\n# RCC files\n/out\n", "template/include/rcclib.lua": " """+LIB+r""" ", "template/src/server/init.server.kt": "print(\"Hello world, from server!\")", "template/src/shared/Hello.kt": "global returnVal\ndef returnVal():\n\tprint(\"Hello, world!\")\n", "template/src/client/init.client.kt": "print(\"Hello world, from client!\")"}"""

def load(format):
    if format == "roblox-cs":
        json_to_dir(CS)
    elif format == "roblox-c (C)":
        json_to_dir(C)
    elif format == "roblox-c (C++)":
        json_to_dir(CPP)
    elif format == "roblox-py":
        json_to_dir(PYTHON)
    elif format == "roblox-kt":
        json_to_dir(KT)


