# Build

```
emcmake cmake -G Ninja -S . -B build -DVTK_DIR=/path/to/where/vtk/wasm/was/built

cmake --build build
```

# Serve and test generated code

```
python3 -m http.server 8000
```

Open your browser to http://localhost:8000
