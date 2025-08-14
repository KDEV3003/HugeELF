这里存放了HugeELF的代码，该项目使用Py脚本生成，通过运行该脚本，会生成一个名为 elf_bloat_proj的目录，进入之后使用以下命令开始编译：   

Usage:
```bash
cd elf_bloat_proj
mkdir build && cd build
cmake ..
cmake --build . -j$(nproc)
```

