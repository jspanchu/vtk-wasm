# Building VTK

## Tools

We will use the Emscripten SDK to compile C++ for wasm architecture. NodeJS will be used as a cross compiling emulator. CMake and Ninja are required to
setup the project.

### Install requirements

First, clone VTK and checkout a release version.

```sh
git clone https://gitlab.kitware.com/vtk/vtk.git
```

Now, install NodeJS and EMSDK. Go to https://nodejs.org/en/download and follow the instructions for your platform.

::: code-group
```sh [macOS/Linux]
# Download and install fnm:
curl -o- https://fnm.vercel.app/install | bash
# Download and install Node.js
fnm install 24.0.1
fnm use 24.0.1

# Download and install EMSDK
git clone https://github.com/emscripten-core/emsdk.git
./emsdk/emsdk install 4.0.9
export PATH=$PWD/emsdk/upstream/bin:$PWD/emsdk/upstream/emscripten:$PATH
```
```sh [Windows]
# In Powershell
# Download and install fnm:
winget install Schniz.fnm
# Download and install Node.js
fnm install 24.0.1
fnm env --use-on-cd --shell power-shell | Out-String | Invoke-Expression
fnm use 24.0.1

git clone https://github.com/emscripten-core/emsdk.git
.\emsdk\emsdk install 4.0.9
$env:PATH="$PWD\emsdk\upstream\bin;$PWD\emsdk\upstream\emscripten;$env:PATH"
```
:::

Finally, download prebuilt webgpu static libraries and headers for `emdawnwebgpu`.

::: code-group
```sh [wasm32:macOS/Linux]
cd vtk
CMAKE_CONFIGURATION="wasm32" cmake -P ./.gitlab/ci/download_dawn.cmake
export emdawnwebgpu_dir="$PWD/.gitlab/dawn/lib/cmake/emdawnwebgpu"
```
```sh [wasm64:macOS/Linux]
cd vtk
CMAKE_CONFIGURATION="wasm64" cmake -P ./.gitlab/ci/download_dawn.cmake
export emdawnwebgpu_dir="$PWD/.gitlab/dawn/lib/cmake/emdawnwebgpu"
```
```sh [wasm32:Windows]
# In Powershell
cd vtk
$env:CMAKE_CONFIGURATION="wasm32"
cmake -P .\.gitlab\ci\download_dawn.cmake
$env:emdawnwebgpu_dir = "$PWD\.gitlab\dawn\lib\cmake\emdawnwebgpu" -replace '\\', '/'
```
```sh [wasm64:Windows]
# In Powershell
cd vtk
$env:CMAKE_CONFIGURATION="wasm64"
cmake -P .\.gitlab\ci\download_dawn.cmake
$env:emdawnwebgpu_dir = "$PWD\.gitlab\dawn\lib\cmake\emdawnwebgpu" -replace '\\', '/'
```
:::

## Building VTK

:::code-group
```sh [wasm32:macOS/Linux]
emcmake cmake \
-S . \
-B buildRelease \
-G "Ninja" \
-DCMAKE_BUILD_TYPE=Release \
-DBUILD_SHARED_LIBS:BOOL=OFF \
-DVTK_ENABLE_WEBGPU:BOOL=ON \
-Demdawnwebgpu_DIR="$emdawnwebgpu_dir"
cmake --build ./buildRelease
cmake --install ./buildRelease --prefix ./installRelease
```
```sh [wasm64:macOS/Linux]
emcmake cmake \
-S . \
-B buildRelease \
-G "Ninja" \
-DCMAKE_BUILD_TYPE=Release \
-DBUILD_SHARED_LIBS:BOOL=OFF \
-DVTK_ENABLE_WEBGPU:BOOL=ON \
-DVTK_WEBASSEMBLY_64_BIT:BOOL=ON \
-Demdawnwebgpu_DIR="$emdawnwebgpu_dir"
cmake --build ./buildRelease
cmake --install ./buildRelease --prefix ./installRelease
```
```sh [wasm32:Windows]
# In Powershell
emcmake cmake `
-S . `
-B buildRelease `
-G "Ninja" `
-DCMAKE_BUILD_TYPE=Release `
-DBUILD_SHARED_LIBS:BOOL=OFF `
-DVTK_ENABLE_WEBGPU:BOOL=ON `
-Demdawnwebgpu_DIR="$env:emdawnwebgpu_dir"
cmake --build .\buildRelease
cmake --install .\buildRelease --prefix .\installRelease
```
```sh [wasm64:Windows]
# In Powershell
emcmake cmake `
-S . `
-B buildRelease `
-G "Ninja" `
-DCMAKE_BUILD_TYPE=Release `
-DBUILD_SHARED_LIBS:BOOL=OFF `
-DVTK_ENABLE_WEBGPU:BOOL=ON `
-DVTK_WEBASSEMBLY_64_BIT:BOOL=ON `
-Demdawnwebgpu_DIR="$env:emdawnwebgpu_dir"
cmake --build .\buildRelease
cmake --install .\buildRelease --prefix .\installRelease
```
:::
