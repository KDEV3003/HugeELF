#!/usr/bin/env python3
import os

# 参数调节：越大 ELF 越大
MODULE_COUNT = 1000         # 模块数量
CLASSES_PER_MODULE = 50    # 每个模块的类数量
FUNCS_PER_CLASS = 20       # 每个类的成员函数数量
TEMPLATE_REPEAT = 40       # 每个模块的模板实例数量

os.makedirs("elf_bloat_proj/src", exist_ok=True)

# 生成 CMakeLists.txt
with open("elf_bloat_proj/CMakeLists.txt", "w") as f:
    f.write(f"""
cmake_minimum_required(VERSION 3.5)
project(huge_elf)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_FLAGS "-O0 -g3 -ggdb")

file(GLOB SRC_FILES src/*.cpp)
add_executable(huge_elf ${{SRC_FILES}})
""")

# 生成 main.cpp
with open("elf_bloat_proj/src/main.cpp", "w") as f:
    f.write('#include <iostream>\n')
    for i in range(MODULE_COUNT):
        f.write(f'void module_func_{i}();\n')
    f.write('int main() {\n')
    for i in range(MODULE_COUNT):
        f.write(f'    module_func_{i}();\n')
    f.write('    std::cout << "Done\\n";\n')
    f.write('    return 0;\n')
    f.write('}\n')

# 生成每个模块 cpp
for m in range(MODULE_COUNT):
    with open(f"elf_bloat_proj/src/module_{m:04}.cpp", "w") as f:
        f.write('#include <iostream>\n')
        f.write(f'namespace module_{m} {{\n')

        # 模板定义
        f.write('template<int N>\nstruct TemplateBlob {\n')
        f.write('    int data[N];\n')
        f.write('    TemplateBlob() { for(int i=0;i<N;++i) data[i] = i*N; }\n')
        f.write('    int sum() const { int s=0; for(int i=0;i<N;++i) s += data[i]; return s; }\n')
        f.write('};\n')

        # 多个类
        for c in range(CLASSES_PER_MODULE):
            f.write(f'struct Class_{c} {{\n')
            f.write(f'    virtual ~Class_{c}() {{}}\n')
            for fn in range(FUNCS_PER_CLASS):
                f.write(f'    virtual int func_{fn}(int x) {{ return x + {c} + {fn}; }}\n')
            f.write('};\n')

        f.write('} // namespace\n')

        # 模块入口
        f.write(f'void module_func_{m}() {{\n')
        f.write(f'    using namespace module_{m};\n')
        for t in range(TEMPLATE_REPEAT):
            f.write(f'    TemplateBlob<{10+t}> blob_{t};\n')
            f.write(f'    volatile int s_{t} = blob_{t}.sum();\n')
        for c in range(CLASSES_PER_MODULE):
            f.write(f'    Class_{c} obj_{c};\n')
            f.write(f'    volatile int r_{c} = obj_{c}.func_0({c});\n')
        f.write('}\n')

print("✅ 项目已生成，编译命令：")
print("""
cd elf_bloat_proj
mkdir build && cd build
cmake ..
cmake --build . -j$(nproc)
""")
