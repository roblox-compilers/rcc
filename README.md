# rcc
[![Windows & Ubuntu (Latest Build)](https://github.com/roblox-compilers/rcc/actions/workflows/compile.yml/badge.svg)](https://github.com/roblox-compilers/rcc/actions/workflows/compile.yml)
Interface to install, update and configurate *roblox-py*. *qts*, *roblox-ts*, *roblox-c*, *roblox-cs*, and *roblox-kt* that allows you to use all the compilers at once with Rojo.
***
## Usage
### `install`
Allows you to install a compiler like:
`rcc install rbxpy`
### `init`
Loads the interactive template creator
### `uninstall`
Allows you to uninstall a compiler like:
`rcc uninstall rbxpy`
### `uninstall`
Allows you to uninstall a compiler like:
`rcc uninstall rbxpy`
### `update`
Uninstalls and reinstalls the compiler (can also be done with rcc itself)
`rcc update rbxpy`
`rcc update rcc`
## Options
#### No options
If no options are provided it will compile `src` to `out`
### `-o`
Specifies the output directory, input directory does not need an option.
`rcc src -o out`

