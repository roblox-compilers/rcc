 -- Roblox Compiler Collection Library

local RCC = {}

function RCC.import(name)
    local Packages = game.ReplicatedStorage.Packages:GetChildren()
    for i, v in Packages do
        local author, packagename = v.Name:match('(.+)%.(.+)')
        if name == packagename then
            return require((v.src or v.lib or error(('[RCC] %s does not have a src or lib folder'):format(v.Name))).init)
        end
    end
end

return RCC 